import io
import random
import qrcode
from decimal import Decimal
from celery import shared_task
from django.core.mail import EmailMessage
from network.models import NetworkObject, Contact


@shared_task
def increase_debt_task():
    objects = NetworkObject.objects.filter(supplier__isnull=False)
    for obj in objects:
        increment = Decimal(str(round(random.uniform(5, 500), 2)))
        obj.debt += increment
        obj.save(update_fields=['debt'])
    return f"Обновлено задолженности для {objects.count()} объектов."


@shared_task
def decrease_debt_task():
    objects = NetworkObject.objects.filter(supplier__isnull=False)
    for obj in objects:
        decrement = Decimal(str(round(random.uniform(100, 10000), 2)))
        new_debt = obj.debt - decrement
        obj.debt = new_debt if new_debt >= 0 else Decimal("0.00")
        obj.save(update_fields=['debt'])
    return f"Обновлено задолженности для {objects.count()} объектов."


@shared_task
def async_data_cleaning_task(object_ids):
    qs = NetworkObject.objects.filter(id__in=object_ids)
    cleaned_count = 0
    for obj in qs:
        obj.debt = Decimal("0.00")
        obj.save(update_fields=['debt'])
        cleaned_count += 1

    return f"Очистка данных завершена для {cleaned_count} объектов."


@shared_task
def send_qr_code_email(contact_id, user_email):
    try:
        contact = Contact.objects.get(id=contact_id)
        contact_data = (f"{contact.network_object.name}\n"
                        f"Email: {contact.email}\nA"
                        f"ddress: {contact.address}")

        qr = qrcode.make(contact_data)
        img_io = io.BytesIO()
        qr.save(img_io, format='PNG')
        img_io.seek(0)

        email = EmailMessage(
            subject="Ваш QR-код с контактными данными",
            body=f"Контактные данные для {contact.network_object.name} во вложении.",
            to=["denis16.05.2004@gmail.com", user_email],
        )
        email.attach("contact_qr.png", img_io.read(), "image/png")
        email.send()

        return f"QR-код отправлен на {contact.email}"

    except Contact.DoesNotExist:
        return f"Контакт с ID {contact_id} не найден"
