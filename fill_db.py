import random
from decimal import Decimal

from faker import Faker
from django.contrib.auth.models import User
from network.models import NetworkObject, Product, Contact, Address, Employee

faker = Faker("ru_RU")


def create_network_objects():
    suppliers = []
    for _ in range(10):
        supplier = random.choice(suppliers) if suppliers else None
        if supplier:
            while supplier.hierarchy == 4:
                supplier = random.choice(suppliers)
        obj = NetworkObject.objects.create(
            name=faker.company(),
            supplier=supplier,
            hierarchy=(0 if not supplier else supplier.hierarchy + random.randint(1, 4 - supplier.hierarchy)),
            debt=Decimal(random.uniform(1000, 50000)).quantize(Decimal('0.01'))
        )
        obj.save()
        suppliers.append(obj)
    print("[+] Добавлены объекты сети")


def create_addresses():
    addresses = []
    countries_cis = ['Россия', 'Украина', 'Беларусь', 'Казахстан', 'Армения']
    for _ in range(20):
        address = Address.objects.create(
            country=random.choice(countries_cis),
            city=faker.city(),
            street=faker.street_name(),
            house_number=faker.building_number()
        )
        addresses.append(address)
    print("[+] Добавлены адреса")
    return addresses


def create_contacts(addresses):
    network_objects = list(NetworkObject.objects.all())
    for i in range(len(addresses)):
        network_object = random.choice(network_objects)
        address = addresses[i]
        Contact.objects.create(
            network_object=network_object,
            email=faker.email(),
            address=address
        )
    print("[+] Добавлены контакты")


def create_products():
    network_objects = list(NetworkObject.objects.all())
    for _ in range(15):
        product = Product.objects.create(
            name=faker.word().capitalize(),
            model=faker.bothify(text="Model-####"),
            release_date=faker.date_between(start_date="-5y", end_date="today")
        )
        product.network_object.set(random.sample(network_objects, k=random.randint(1, 5)))
    print("[+] Добавлены продукты")


def create_employees():
    network_objects = list(NetworkObject.objects.all())
    for _ in range(10):
        user = User.objects.create_user(username=faker.user_name(), password="testpass")
        Employee.objects.create(
            user=user,
            network_object=random.choice(network_objects),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            position=faker.job(),
            active=random.choice([True, False])
        )
    print("[+] Добавлены сотрудники")


def populate_database():
    print("[*] Заполняем базу тестовыми данными...")
    create_network_objects()
    addresses = create_addresses()
    create_contacts(addresses)
    create_products()
    create_employees()
    print("[✔] Готово!")


populate_database()
