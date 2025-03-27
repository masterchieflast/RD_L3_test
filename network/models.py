from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class NetworkObject(models.Model):
    name = models.CharField("Название", max_length=100)
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик"
    )
    HIERARCHY = (
        (0, "Завод"),
        (1, "Дистрибьютор"),
        (2, "Дилерский центр"),
        (3, "Крупная розничная сеть"),
        (4, "Индивидуальный предприниматель"),
    )
    hierarchy = models.PositiveSmallIntegerField("Иерархическая структура", choices=HIERARCHY, default=0)

    level = models.PositiveSmallIntegerField("Уровень", default=0, editable=False)

    debt = models.DecimalField("Задолженность", max_digits=12, decimal_places=2, default=0.00)

    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    def clean(self):
        if self.supplier:
            new_level = self.supplier.level + 1
            if new_level > 4:
                # raise ValidationError("Нельзя создать уровень выше 4")
                new_level = 4
            self.level = new_level
            if self.supplier.hierarchy >= self.hierarchy:
                raise ValidationError("Поставщик должен быть выше в иерархии.")

            self.level = new_level
        else:
            self.level = 0

        if self.hierarchy == 0 and self.supplier:
            raise ValidationError("Завод не может иметь поставщика.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Address(models.Model):
    country = models.CharField("Страна", max_length=50)
    city = models.CharField("Город", max_length=50)
    street = models.CharField("Улица", max_length=50)
    house_number = models.CharField("Номер дома", max_length=10)

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"


class Contact(models.Model):
    network_object = models.ForeignKey(
        NetworkObject,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Звено сети"
    )
    email = models.EmailField("Электронная почта")
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        verbose_name="Адрес"
    )

    def __str__(self):
        return f"Контакт {self.email} для {self.network_object.name}"


class Product(models.Model):
    network_object = models.ManyToManyField(
        NetworkObject,
        related_name='products',
        verbose_name="Звено сети"
    )
    name = models.CharField("Название продукта", max_length=100)
    model = models.CharField("Модель", max_length=100)
    release_date = models.DateField("Дата выхода на рынок")

    def __str__(self):
        return f"{self.name} ({self.model})"


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Пользователь"
    )
    network_object = models.ForeignKey(
        NetworkObject,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name="Звено сети"
    )
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    position = models.CharField("Должность", max_length=100)
    active = models.BooleanField("Активный", default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"
