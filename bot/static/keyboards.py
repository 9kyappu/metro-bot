# -*- coding: utf-8 -*-

from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup
)


class Keyboards:
    MENU_KEYBOARD = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛤️ Поиск маршрута",
                    callback_data="way"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗺️ Карта метро",
                    callback_data="metro_map"
                ),
                InlineKeyboardButton(
                    text="🧾 Помощь",
                    callback_data="help"
                )
            ]
        ]
    )

    CITY_KEYBOARD = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌧 Санкт-Петербург",
                    callback_data="set_city:1"
                ),
                InlineKeyboardButton(
                    text="🏙 Москва",
                    callback_data="set_city:2"
                )
            ]
        ]
    )  # TODO: генерация клавы при старте из бд (city_name | city_id)

    WAY_KEYBOARD = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Выберете вашу станцию:",
                    callback_data="WAY_KEYBOARD"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↩ В меню",
                    callback_data="menu"
                )
            ]
        ]
    )

    END_KEYBOARD = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗺️ Карта метро",
                    callback_data="metro_map"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↩ В меню",
                    callback_data="menu"
                )
            ]
        ]
    )

    ERROR_KEYBOARD = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="↩ В меню",
                    callback_data="menu"
                )]
            ]
        )

    HELP_KEYBOARD = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 Администратор",
                    url="https://t.me/rarseniy"
                ),
                InlineKeyboardButton(
                    text="🔃 Смена города",
                    callback_data="change_city"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↩ В меню",
                    callback_data="menu"
                )
            ]
        ]
    )
