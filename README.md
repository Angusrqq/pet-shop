<h1 align="center">pet-shop</h1>

<p align="center">A very basic online store for pet stuff</p>

# Stack
 - Python 3.13
 - Django 6.0

# Setup

## Clone the repository
    git clone https://github.com/Angusrqq/pet-shop.git

## Install dependencies
### pip
>```
>pip install -r requiremets.txt
>```

### uv
>```
>uv sync
>```

## Environment variables
create a `.env` file in project root
```
DJANGO_SECRET_KEY=your_key
```

## Django setup

> [!IMPORTANT]
> `manage.py` is inside `petShop/backend`.

### Migrations
```
python manage.py migrate
```
> [!NOTE]
> you can create a superuser by
> ```
> python manage.py createsuperuser
> ```

### Running the server
```
python manage.py runserver
```
> [!NOTE]
> If you want static & media files to be served by django while not in debug, instead you can use
> ```
>python manage.py runserver --insecure
> ```

# Screenshots

## Light theme
![main page light](screenshots/light/main.png)

![about page light](screenshots/light/about.png)

![catalog page light](screenshots/light/catalog.png)

![delivery page light](screenshots/light/delivery.png)

![account page light](screenshots/light/account.png)

![change password page light](screenshots/light/change-password.png)

![cart(empty) page light](screenshots/light/empty-cart.png)

![cart page light](screenshots/light/cart.png)

![checkout page light](screenshots/light/checkout.png)

![register page light](screenshots/light/register.png)

![login page light](screenshots/light/login.png)

![orders page light](screenshots/light/orders.png)

![order page light](screenshots/light/order.png)

![product page light](screenshots/light/product.png)



## Dark theme
![main page dark](screenshots/dark/main.png)

![about page dark](screenshots/dark/about.png)

![catalog page dark](screenshots/dark/catalog.png)

![delivery page dark](screenshots/dark/delivery.png)

![account page dark](screenshots/dark/account.png)

![change password page dark](screenshots/dark/change-password.png)

![cart(empty) page dark](screenshots/dark/empty-cart.png)

![cart page dark](screenshots/dark/cart.png)

![checkout page dark](screenshots/dark/checkout.png)

![register page dark](screenshots/dark/register.png)

![login page dark](screenshots/dark/login.png)

![orders page dark](screenshots/dark/orders.png)

![order page dark](screenshots/dark/order.png)

![product page dark](screenshots/dark/product.png)
