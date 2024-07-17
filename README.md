# Проект self_therapy
Ценность проекта -- психологическая поддержка в моменты острой необходимости и каждый день.
Карманный психолог, который знает тебя лучше всех. [Подробней](#функционал) о функционале.

## Содержание
- [Функционал](#функционал)
- [Технологии](#технологии)
- [Запуск проекта](#запуск-проекта)
- [Проектирование](#проектирование)
- [Реализация](#реализация)

## Функционал:
|Функция для пользователя | Что делает на программном уровне | Тип:базовая-расширенная | Примечание |
| ------------- |:------------------:| -----:|-----:|
|Начать общение с ботом | Добавляет чат с пользователем в базу, устанавливает базовые подсказки | Базовая | --- |
|Установить базовые подсказки | Скопировать в таблицу из предварительных настроек все строчки | Базовая | --- |
|Получить подсказку | Достать подсказку пользователя с определённым рейтингом или не скрытую| Базовая | --- |
|Добавить подсказку | Записать подсказку пользователя | Базовая | --- |
|Изменить подсказку | Отредактировать подсказку пользователя | Расширенная | --- |
|Удалить подсказку | Скрыть подсказку пользователя | Расширенная | --- |
|Оценить подсказку (насколько помогла) | Пересчёт поля рейтинга подсказки | Расширенная | --- |
|Достать все подсказки, даже скрытые, что-то вроде настройки | Достсть подсказки со всеми рейтингами | Расширенная | --- |
|1 | 2 | 3 | --- |
|1 | 2 | 3 | --- |

функционал:

- добавить строчку в журнал настроения 
- посммотреть журанл настроения за период
- редактировать строчку в журнале
- удалить строчку в журнале
- очистить весь журнал
- итог за день (кол-во)

- добавить строчку в журнал эмоций
- посмотреть журнал настроения за период
- редактировать строчку в журнале
- удалить строчку в журнале
- очистить весь журнал

- почитать про эмоции (получить список порциями)
- угадать эмоцию (это на будущее)

## Технологии:
Python + Django + API Telegram


## Запуск проекта:
- $ python -m venv venv
- $ source venv/Scripts/activate
- $ python -m pip install --upgrade pip
- $ pip install -r requirements.txt
- $ cd self_therapy
- $ python manage.py migrate
- $ python manage.py runserver


## Проектирование:

![Схема БД](https://github.com/belyashnikovatn/self_therapy/blob/main/self_help_project.png)  
This is a new paragraph.

### Задачи:
+ Установка, настройка 
+ Создать модели данных
+ Настроить бд
- Настроить админку
- Базовый функционал
- Предусмотреть независимость от апи телеграмма -- значит функции разнести по уровням

### Задачи со звёздочкой:
- Фикстуры для предварительных настроек
- Расширенный функционал
- Чтение, запись во все остальные 
- Шифрование id диалога (и вообще подумать про id юзера, может и стоить использовать только id чата)
- Добавить логирование
- Покрыть тестами

## Реализация:

Зачем я это делала? 
- Для личного использования;
- Для удобавства: всё это лежало в разных местах сотового или даже на бумаге, хотя составляло часть одного процесса;
- Прокачаться в обучении;
- Поучаствовать в вебинаре.


