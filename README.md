# Система Учёта Специалистов

Проект представляет собой веб-приложение для автоматизированного учёта сотрудников компании. Реализован на Django и предназначен для отслеживания профилей сотрудников, рабочего графика, посещаемости и отчётности.

## Возможности

- Регистрация и аутентификация пользователей
- Профиль сотрудника: имя, должность, отдел, фото
- График работы: создание и просмотр смен
- Учёт рабочего времени и событий (начало, конец, перерыв)
- Месячные отчёты по отработанным часам
- Просмотр и редактирование профиля и расписания
- Админ-панель Django

## Технологии

- Python 3.x
- Django 4.x
- SQLite/PostgreSQL
- HTML/CSS (Django Templates)
- Bootstrap (опционально)
- Логирование (модуль `logging`)
- Авторизация через Django

## Структура проекта

```
project/
├── app/
│   ├── forms.py
│   ├── models.py
│   ├── views.py 
│   ├── etc..    
│   └── templates/
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── work_hours.html
│       ├── schedule.html
│       ├── reports.html
│       ├── edit_profile.html
│       ├── edit_schedule.html
│       └── attendance_log.html
├── manage.py
└── README.md
```

## Скриншоты

### Аунтефикация
![Скриншот страницы аунтефикации](https://github.com/Ryota77777/ModuleAppDataBase1/blob/main/templates/auth.png?raw=true)

### Главная страница
![Скриншот главной страницы](https://github.com/Ryota77777/ModuleAppDataBase1/blob/main/templates/mainy.png?raw=true)

### Профиль
![Скриншот профиля](https://github.com/Ryota77777/ModuleAppDataBase1/blob/main/templates/profile.png?raw=true)

### Расписание
![Скриншот расписания](https://github.com/Ryota77777/ModuleAppDataBase1/blob/main/templates/schedule.png?raw=true)

### Журнал
![Скриншот журнала](https://github.com/Ryota77777/ModuleAppDataBase1/blob/main/templates/journal.png?raw=true)

```

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Ryota77777/ModuleAppDataBase1.git
cd ModuleAppDataBase1
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Примените миграции и создайте суперпользователя:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Запустите сервер:

```bash
python manage.py runserver
```

6. Откройте в браузере:

```
http://127.0.0.1:8000/
```

## Авторизация и Роли

- Авторизация по логину и паролю
- Автоматическое создание профиля при регистрации
- Проверка профиля перед входом

## Примечания

- Учёт часов происходит автоматически при добавлении события "конец" смены
- Поддерживается добавление смен вручную
- Все шаблоны можно адаптировать под Bootstrap или Tailwind

## Лицензия

MIT License

---
