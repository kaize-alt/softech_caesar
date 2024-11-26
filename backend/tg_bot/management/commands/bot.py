import telebot 
from django.core.management.base import BaseCommand 
from django.utils.html import strip_tags 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton 
from backend.catalog.models import * 
from backend.users.models import CustomUser 
from cart.models import Cart, CartItem 
from softech import settings

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)  #SoftechConsult_bot

help = (
    "/start - Запуск бота \n"
    "/help - Получить информацию о боте"
)



@bot.message_handler(commands=['start'])
def start(message):
    text = "Приветствую в магазине MiStore!"
    username = message.from_user.username
    fisrt_name = message.from_user.first_name

    tg_user, _ = CustomUser.objects.get_or_create(username=username, telegram_username=username, first_name=fisrt_name)

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Обратиться к специалисту", callback_data="contact")
    button2 = InlineKeyboardButton("Выбрать товар", callback_data="categories")
    markup.add(button1, button2)

    bot.send_message(message.chat.id, text, reply_markup=markup)




@bot.message_handler(commands=['help'])
def help(message):
    text = help
    bot.send_message(message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == "categories")
def category_list_get(call):
    category_list = Category.objects.all()
    markup = InlineKeyboardMarkup()
    for category in category_list:
        markup.add(
            InlineKeyboardButton(text=category.name,
                                       callback_data=f"subcategory_{category.id}")
        )
    bot.send_message(call.message.chat.id, "Список категорий", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("subcategory_"))
def subcategory_list_get(call):
    category_id = Category.objects.get(id=call.data.split('_')[1])
    subcategory_list = SubCategory.objects.filter(category=category_id)
    markup = InlineKeyboardMarkup()
    for sub_category in subcategory_list:
        markup.add(
            InlineKeyboardButton(text=sub_category.name,
                                       callback_data=f"items_{sub_category.id}")
        )
    bot.send_message(call.message.chat.id, "Список подкатегорий", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("items_"))
def items_list_get(call):
    subcategory_id = SubCategory.objects.get(id=call.data.split('_')[1])
    items_list = Product.objects.filter(subcategory=subcategory_id)
    markup = InlineKeyboardMarkup()
    for item in items_list:
        markup.add(
            InlineKeyboardButton(text=item.name,
                                       callback_data=f"productInfo_{item.id}")
        )
    bot.send_message(call.message.chat.id, "Список продуктов", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("productInfo"))
def product_info_get(call):
    product = Product.objects.filter(id=call.data.split("_")[1])
    text = f"{product[0].name}\n{strip_tags(product[0].description)}\n{product[0].price}"
    markup = InlineKeyboardMarkup()
    subcategory_id = product[0].subcategory.id
    markup.add(
        InlineKeyboardButton(text="назад", callback_data=f"items_{subcategory_id}"),
        InlineKeyboardButton(text="добавить в корзину", callback_data=f"cart_{product[0].id}")
    )
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cart_"))
def cart(call):
    user = CustomUser.objects.get(username=call.from_user.username)
    cart, _ = Cart.objects.get_or_create(user=user)
    product = Product.objects.get(id=call.data.split("_")[1])
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.amount += 1
    cart_item.save()
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Товары", callback_data=f"items_{product.subcategory.id}"),
        InlineKeyboardButton(text="Оформить заказ", callback_data=f"order_{cart.id}"),
    )
    bot.send_message(call.message.chat.id, f"Товар {product.name} был успешно добавлен!:3", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def order(call):
    # cart = Cart.objects.filter(id=call.data.split("_")[1])
    cart_item = CartItem.objects.filter(cart=call.data.split("_")[1])
    item_list = []
    for item in cart_item:
        item_list.append(item)
        print(item)
    text = f"Ваш товар в корзине:" + '\n' + '\n'.join(item_list) + ' -' + 
    bot.send_message(call.message.chat.id, text)
    print(item_list)


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Запуск Telegram-бота..."))
        bot.infinity_polling(none_stop=True)



