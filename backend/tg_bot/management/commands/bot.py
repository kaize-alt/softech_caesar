import telebot 
from django.core.management.base import BaseCommand 
from django.utils.html import strip_tags 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton 
from backend.items.models import * 
from backend.users.models import * 
from softech import settings

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)  #SoftechConsult_bot

help = (
    "/start - Запуск бота \n"
    "/help - Получить информацию о боте\n"
    "/cart - Показать товары в корзине\n"
    "/order - Оформить заказ\n"
)


@bot.message_handler(commands=['start'])
def start(message):
    text = "Приветствую в магазине MiStore!"
    telegram_username = message.chat.username or "Не указан"
    
    user = CustomUser.objects.filter(telegram_username=telegram_username).first()
    
    if user:
        text += f"\nС возвращением, {user.telegram_username}!"
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Обратиться к специалисту", callback_data="contact")
        button2 = InlineKeyboardButton("Выбрать товар", callback_data="categories")
        markup.row(button1)
        markup.row(button2)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        text += "\nКажется, вы еще не зарегистрированы. Пожалуйста, предоставьте ваш номер телефона для регистрации."
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        phone_button = KeyboardButton("Отправить номер телефона", request_contact=True)
        markup.add(phone_button)
        bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        phone_number = message.contact.phone_number
        telegram_username = message.chat.username or "Не указан"
        
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user:
            bot.send_message(
                message.chat.id,
                f"Вы уже зарегистрированы! Ваш номер: {phone_number}"
            )
        else:
            CustomUser.objects.create_user(
                phone_number=phone_number,
                telegram_username=telegram_username
            )
            bot.send_message(
                message.chat.id,
                "Вы успешно зарегистрированы! Теперь вы можете пользоваться ботом."
            )
    else:
        bot.send_message(
            message.chat.id,
            "Не удалось получить номер телефона. Попробуйте еще раз."
        )




@bot.message_handler(commands=['help'])
def help(message):
    text = help
    bot.send_message(message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == "categories")
def category_list_get(call):
    parent_category_list = Category.objects.filter(parent_category__isnull=True)
    markup = InlineKeyboardMarkup()
    for category in parent_category_list:
        markup.add(
            InlineKeyboardButton(text=category.name,
                                       callback_data=f"subcategory_{category.id}")
        )
    bot.send_message(call.message.chat.id, "Список категорий", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("subcategory_"))
def subcategory_list_get(call):
    category_id = Category.objects.get(id=call.data.split('_')[1])
    subcategory_list = Category.objects.filter(parent_category=category_id)
    markup = InlineKeyboardMarkup()
    for sub_category in subcategory_list:
        markup.add(
            InlineKeyboardButton(text=sub_category.name,
                                       callback_data=f"items_{sub_category.id}")
        )
    bot.send_message(call.message.chat.id, "Список подкатегорий", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("items_"))
def items_list_get(call):
    subcategory_id = Category.objects.get(id=call.data.split('_')[1])
    items_list = Product.objects.filter(category=subcategory_id)
    if not items_list.exists():
         bot.send_message(call.message.chat.id, "Продукты не найдены.")
    else:
        markup = InlineKeyboardMarkup()
    for item in items_list:
        markup.add(
            InlineKeyboardButton(text=item.name,callback_data=f"productInfo_{item.id}")
        )
    bot.send_message(call.message.chat.id, "Список продуктов", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("productInfo"))
def product_info_get(call):
    product = Product.objects.filter(id=call.data.split("_")[1])
    text = f"{product[0].name}\n{strip_tags(product[0].description)}\n{product[0].price}"
    markup = InlineKeyboardMarkup()
    subcategory_id = product[0].category.id
    markup.add(
        InlineKeyboardButton(text="назад", callback_data=f"items_{subcategory_id}"),
        InlineKeyboardButton(text="добавить в корзину", callback_data=f"cart_{product[0].id}")
    )
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cart_"))
def cart(call):
    user = CustomUser.objects.get(username=call.from_user.username)
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        cart = Cart.objects.create(user=user)
    product = Product.objects.get(id=call.data.split("_")[1])
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.amount += 1
    cart_item.save()
    cart_item.total_price = cart_item.amount * product.price
    cart_item.save()
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Товары", callback_data=f"items_{product.category.id}"),
        InlineKeyboardButton(text="Оформить заказ", callback_data=f"order_{cart.id}"),
    )
    bot.send_message(call.message.chat.id, f"Товар {product.name} был успешно добавлен!:3", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def order(call):
    try:
        cart = Cart.objects.get(id=call.data.split("_")[1])
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            bot.send_message(call.message.chat.id, "Корзина пуста.")
            return
        
        item_list = [
            f"{item.product.name} x{item.amount} = {item.total_price}₽"
            for item in cart_items
        ]
        total_sum = sum(item.total_price for item in cart_items)
        text = "Ваши товары:\n" + "\n".join(item_list) + f"\nИтоговая сумма: {total_sum}₽"
        bot.send_message(call.message.chat.id, text)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка при обработке заказа.")
        print(e)



class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Запуск Telegram-бота..."))
        bot.infinity_polling(none_stop=True)



