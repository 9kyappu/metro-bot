# -*- coding: utf-8 -*-

from pyrogram import Client, filters
from pyrogram.filters import regex as regex_filter
from pyrogram.types import (
    CallbackQuery, Message,
    InlineKeyboardButton, InlineKeyboardMarkup
)

from utils.dijkstra_algorithm import dijkstra_algorithm
from utils.dijkstra_algorithm import Graph
from core.app import APP, METRO_CONTROLLER, STATE_MANAGER, USER_CONTROLLER
from utils.state_manager import StateNotFound, StateDataNotFound
from static.keyboards import Keyboards
from static.msgs import UserCommand


@APP.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    auth_date = message.date.date()
    await USER_CONTROLLER.create_user(user_id=user_id, date=auth_date, )
    city_id = await USER_CONTROLLER.search_city(user_id=user_id, )
    if city_id is None:
        await message.reply(
            text=UserCommand.START_CITY_TEXT.format(first_name=message.from_user.first_name),
            reply_markup=Keyboards.CITY_KEYBOARD
        )
    else:
        await message.reply(
            text=UserCommand.START_TEXT.format(first_name=message.from_user.first_name),
            reply_markup=Keyboards.MENU_KEYBOARD
            )


@APP.on_callback_query(regex_filter("menu"))
async def products_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(
        UserCommand.MENU_TEXT,
        reply_markup=Keyboards.MENU_KEYBOARD
    )


@APP.on_callback_query(regex_filter(r"set_city:\d+"))
async def set_city_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    city_id = callback_query.data.split(":")[1]
    city_name = await METRO_CONTROLLER.get_city_name(city_id)
    await USER_CONTROLLER.set_city(city_id=city_id, user_id=user_id)
    await APP.send_message(
        chat_id=user_id,
        text=UserCommand.CITY_TEXT.format(name=city_name)
    )
    await callback_query.message.edit(
        text=UserCommand.START_TEXT.format(first_name=callback_query.from_user.first_name),
        reply_markup=Keyboards.MENU_KEYBOARD
        )


@APP.on_callback_query(regex_filter("help"))
async def help_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(
        UserCommand.HELP_TEXT,
        reply_markup=Keyboards.HELP_KEYBOARD
    )


@APP.on_callback_query(regex_filter("change_city"))
async def change_city_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(
        UserCommand.CITY_CHOICE_TEXT,
        reply_markup=Keyboards.CITY_KEYBOARD
    )


@APP.on_callback_query(regex_filter("way"))
async def way_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    city_id = await USER_CONTROLLER.search_city(user_id=user_id, )

    STATE_MANAGER.create_state(
        state_id=user_id,
        state_data={"city": city_id}
    )
    await callback_query.message.delete()

    await APP.send_message(
        chat_id=user_id,
        text=UserCommand.FIRST_WAY_TEXT
    )


@APP.on_message(filters.text)
async def search_station(client: Client, message: Message):
    user_id = message.from_user.id

    try:
        city_id = STATE_MANAGER.get_state_data(
            state_id=user_id,
            state_data_name="city"
        )
    except (StateNotFound, StateDataNotFound):
        pass  # TODO сделать исключение
        await message.delete()
        return

    text = message.text.lower()

    searched_stations = await METRO_CONTROLLER.search_stations(text=text, city_id=city_id)

    if searched_stations == []:
        await message.reply(
            text=UserCommand.STATION_NOT_FOUND_TEXT.format(text=text)
        )
        await message.delete()
        return

    await message.reply(
        text="Найденные станции:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=station.name.title(),
                    callback_data=f"set_station:{city_id}:{station.station_id}"
                )] for station in searched_stations
            ]
        )
    )
    await message.delete()


@APP.on_callback_query(regex_filter(r"set_station:\d+:\d+"))  # set_station:{city_id}:{station_id}
async def set_station_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    first_station = ""

    _, city_id, station_id = callback_query.data.split(":")

    station_name = await METRO_CONTROLLER.get_station_name(
        station_id=int(station_id),
        city_id=city_id
    )

    try:
        first_station = STATE_MANAGER.get_state_data(
            state_id=user_id,
            state_data_name="first_station"
        )
    except StateNotFound:
        pass  # TODO сделать исключение
        return
    except StateDataNotFound:
        STATE_MANAGER.set_state_data(
            state_id=user_id,
            state_name="first_station",
            state_data=station_id
        )

        await callback_query.message.delete()

        await APP.send_message(
            chat_id=user_id,
            text=UserCommand.SECOND_WAY_TEXT
        )
        return

    STATE_MANAGER.del_state(state_id=user_id)

    first_station_name = await METRO_CONTROLLER.get_station_name(
        station_id=int(first_station),
        city_id=city_id
    )
    first_station_name = first_station_name.title()
    second_station_name = station_name.title()
    await callback_query.message.delete()

    nodes = []
    all_data = []

    pizda = await METRO_CONTROLLER.get_nodes(city_id=city_id)
    for row in pizda:
        nodes.append((row[2]).title())

    init_graph = {}
    for node in nodes:
        init_graph[node] = {}

    all_data = await METRO_CONTROLLER.get_all_data(city_id=city_id)
    for row in all_data:
        init_graph[row[2].title()][row[3].title()] = row[4]

    graph = Graph(nodes, init_graph)
    previous_nodes, shortest_path = dijkstra_algorithm(
        graph=graph, start_node=first_station_name
    )

    path = []
    point = second_station_name
    while point != first_station_name:
        path.append(point)
        point = previous_nodes[point]
    path.append(first_station_name)

    example = (
        "Найден лучший маршрут в {} минут.\n".format(shortest_path[second_station_name]) +
        " → ".join(reversed(path))
        )

    if first_station_name != second_station_name:
        await APP.send_message(
            chat_id=user_id,
            text=example
        )

        await APP.send_message(
            chat_id=user_id,
            text=UserCommand.END_TEXT,
            reply_markup=Keyboards.END_KEYBOARD
        )
    elif first_station_name == second_station_name:
        await APP.send_message(
            chat_id=user_id,
            text=UserCommand.EXCEPTION_TEXT,
            reply_markup=Keyboards.ERROR_KEYBOARD
        )
