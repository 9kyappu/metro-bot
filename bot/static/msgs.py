# -*- coding: utf-8 -*-


class UserCommand:
    START_TEXT = (
        "  Привет, <i>{first_name}</i> 👋\n\n"
        "С помощью этого бота вы сможете проложить себе маршрут в <b>🚄 метро!</b>\n\n"
        "Все маршруты и карта метро вашего города <i>прямо в 📱 телеграме!</i>"
    )

    START_CITY_TEXT = (
        "  Привет, <i>{first_name}</i> 👋\n\n"
        "С помощью этого бота вы сможете проложить себе маршрут в <b>🚄 метро!</b>\n\n"
        "Все маршруты и карта метро вашего города <i>прямо в 📱 телеграме!</i>\n\n"
        "<b>Для начала давай определимся с твоим городом:</b>"
    )

    MENU_TEXT = (
        "<b>Добро пожаловать</b> в главное меню 👋\n\n"
        "<i>Всё метро в одном чате 😉</i>"
    )

    CITY_CHOICE_TEXT = "Выберете свой город:"

    CITY_TEXT = " Выбран город: {name}"

    FIRST_WAY_TEXT = (
        "Введите название отправной станции:\n"
        "<i>(Вы можете ввести первые буквы начала названия)</i>"
    )

    SECOND_WAY_TEXT = "Введите название конечной станции:"

    STATION_NOT_FOUND_TEXT = 'По поиску "{text}" ничего не найдено!'

    CITY_ERROR_TEXT = "Выберете город заново, произошла ошибка!"

    STATION_ERROR_TEXT = "Произошла ошибка, попробуйте заново!"

    END_TEXT = "<b>Куда дальше? 👀</b>"

    HELP_TEXT = "🧾 Помощь"

    EXCEPTION_TEXT = "Кажется, вы уже приехали 🙃"
