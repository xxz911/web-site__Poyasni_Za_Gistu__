# web-site__Poyasni_Za_Gistu__(Alpha версия)
Релизной версии нет на GitHub
Фулстек заказ образовательного сайта по гистологии.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![version](https://img.shields.io/badge/Version-v.9.0(Alpha)-blue)
![Django](https://img.shields.io/badge/Django-v.4.1.4-info)

## О проекте
На сайте есть регистрация, профиль, посты, альбомы, статьи c разбивкой по категориям, поиск, комментарии и лайки, новостная лента.

## Функционал сайта:
1. Регистрация/Авторизация
  (Используется капча, Расширенная модель User, Для ввода даты рождения используется datetimepicker)
2. Главная страница(последний контент)
3. Посты
4. Альбомы (В Альбомах изображения показываются при помощи baguettebox)
5. Статьи
6. Голосование (Ajax запросы при голосовании)
7. Комментарии
8. Пагинация: Постов, Альбомов, Статей, Комментариев, Изображение в Альбомах
9. Страница профиля (Возможность редактировать данные)
10. Восстановление пароля на странице регистрации( отправка письма на почту)
11. Адаптивный сайт для планшетов и телефонов
12. Кастомный стиль админки
13. Для создания приветствия на Главной странице и Статей, используется редактор ckeditor
14. MySql БД
15. Есть Поиск: Постов, Альбомов, Статей
16. Разбивка на группы: Постов, Альбомов, Статей,
17. Комментарии проверяются Модератором, потом опубликовываются
18. Снятие с публикации на сайте и опубликовывание снова: Постов, Альбомов, Статьей
19. Адаптивные пути для сохраниения изображений
20. Миниатюры в админке на изображения
21. Методы для сокращения текста в админке
22. Использование Bootstrap

## Как установить и запустить сайт локально:
1. Скачайте репозиторий себе на компьютер.

2. Создайте виртуальное окружение и активируйте его.
Пример:
https://docs.python.org/3/library/venv.html

3. Перейдите директорию poyasnizagistu, там установите все необходимые зависимости и запустите сайт локально командами: 

```bash
  $ cd poyasnizagistu
  poyasnizagistu $ pip install -r requirements.txt
  
  poyasnizagistu $ python3 manage.py runserver
```

В терминале вы должны увидеть:
```bash
  Django version 4.1.4, using settings 'poyasnizagistu.settings'
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.
```

## Как использовать сайт:
Откройте свой браузер по адресу
```bash
http://127.0.0.1:8000
```
Вы должны увидеть:
<img src="https://github.com/xxz911/xxz911/blob/main/PoyasniZaGistu_main.jpeg"></img>

## Как использовать админку:
Откройте свой браузер по адресу
```bash
http://127.0.0.1:8000/admin/
```
Введите логин и пароль (логином и паролем является: xxz )
Вы должны увидеть:
<img src="https://github.com/xxz911/xxz911/blob/main/PoyasniZaGistu_admin.jpeg"></img>

Поздравляю! Сайт готов для локального использования
