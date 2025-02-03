from django.db import models


class MainBanner(models.Model):
    background_image = models.ImageField("Фоновая картинка", upload_to="mainbanner")
    title = models.CharField("Заголовок", max_length=255)
    text = models.TextField("Текст")
    button_link = models.URLField("Ссылка кнопки", max_length=255, null=True, blank=True)
    order = models.PositiveIntegerField("Порядок", default=1)

    class Meta:
        verbose_name = "Баннер для главной страницы"
        verbose_name_plural = "Баннеры для главной страницы"
        ordering = ("order",)

    def __str__(self):
        return self.title


class AddsBlock(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    image = models.ImageField("Картинка", upload_to="adds_block")
    image_mobile = models.ImageField("Мобильная картинка", upload_to="adds_block")
    order = models.PositiveIntegerField("Порядок", default=1)

    class Meta:
        verbose_name = "Рекламный блок"
        verbose_name_plural = "Рекламные блоки"
        ordering = ("order",)

    def __str__(self):
        return self.title


class Introduction(models.Model):
    icon = models.ImageField("Иконка компании", upload_to="introduction")
    text = models.CharField("Описание компании", max_length=255)
    btn_link = models.URLField("Кнопка подробнее", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return self.text


class Videos(models.Model):
    video = models.FileField("Видео", upload_to="videos")
    title = models.CharField("Название", max_length=255)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return self.title


class MainSettings(models.Model):
    privacy_policy = models.FileField("Политика конфиденциальности", upload_to="settings", null=True, blank=True)

    class Meta:
        verbose_name = "Основная настройка"
        verbose_name_plural = "Основные настройки"
