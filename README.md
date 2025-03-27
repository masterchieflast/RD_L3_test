# Документация проекта

Этот проект предоставляет API для работы с объектами сети. Ниже приведены инструкции по запуску, заполнению базы данных и примеры запросов к API.

---

## 1. Запуск проекта

Для сборки и запуска проекта используйте команду:
```
docker-compose up --build
```
---

## 2. Заполнение базы данных

Чтобы заполнить базу данных данными, запустите следующую команду внутри контейнера:
```
python manage.py shell < fill_db.py
```
---

## 3. Доступ к API

Пользователи могут получать доступ к API, используя специальный токен. Для получения токена выполните следующий запрос:
```
curl --location 'http://localhost:8000/api-token-auth/' \
--header 'Content-Type: application/json' \
--data '{"username": "root", "password": "1234"}'
```
---

## 4. Примеры запросов к API

### 4.1 Информация обо всех объектах сети
```
curl --location 'http://localhost:8000/api/network-objects/' \
--header 'Content-Type: application/json' \
--header 'Authorization: token 176c0e22fdb245613237c061236f280644af1afc' \
--header '4d97a294e7deacca242b34cf7d495c25d2313d4f;'
```
### 4.2 Информация об объектах определённой страны (фильтр по названию)
```
curl --location 'http://localhost:8000/api/network-objects/by_country/?country=%D0%91%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C' \
--header 'Content-Type: application/json' \
--header 'Authorization: token 176c0e22fdb245613237c061236f280644af1afc' \
--header '4d97a294e7deacca242b34cf7d495c25d2313d4f;'
```
### 4.3 Статистика объектов с задолженностью, превышающей среднюю задолженность всех объектов
```
curl --location 'http://localhost:8000/api/network-objects/above_average_debt' \
--header 'Content-Type: application/json' \
--header 'Authorization: token 176c0e22fdb245613237c061236f280644af1afc' \
--header '4d97a294e7deacca242b34cf7d495c25d2313d4f;'
```
### 4.4 Объекты сети, где можно встретить определенный продукт (фильтр по id продукта)
```
curl --location 'http://localhost:8000/api/network-objects/by_product/?product_id=46' \
--header 'Content-Type: application/json' \
--header 'Authorization: token your token' \
--header '4d97a294e7deacca242b34cf7d495c25d2313d4f;'
```
### 4.5 Доступ пользователя к своему объекту сети

Пользователь может получить информацию только о своём объекте сети:
```
curl --location 'http://localhost:8000/api/network-objects/id' \
--header 'Content-Type: application/json' \
--header 'Authorization: token 176c0e22fdb245613237c061236f280644af1afc' \
--header '4d97a294e7deacca242b34cf7d495c25d2313d4f;'
```
### 4.6 Генерация QR-кода с контактными данными и отправка на e-mail
```
curl --location --request POST 'http://localhost:8000/api/contact/id-contact/send_qr/' \
--header 'Content-Type: application/json' \
--header 'Authorization: token 176c0e22fdb245613237c061236f280644af1afc'```
