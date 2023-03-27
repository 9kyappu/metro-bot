# -*- coding: utf-8 -*-

from pyrogram import Client, filters
from pyrogram.filters import regex as regex_filter
from pyrogram.types import (
    CallbackQuery, Message,
    InlineKeyboardButton, InlineKeyboardMarkup
)

from utils.dijkstra_algorithm import dijkstra_algorithm
from utils.dijkstra_algorithm import Graph
from core import SPB_MAP, MOSCOW_MAP
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


@APP.on_message(filters.command("users"))
async def users_command(client: Client, message: Message):
    count_of_users = await USER_CONTROLLER.users_count()
    await message.reply(
        text=UserCommand.USER_TEXT.format(count=count_of_users)
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
        pass
        return

    text = message.text.lower()

    searched_stations = await METRO_CONTROLLER.search_stations(text=text, city_id=city_id)

    line_ids = []
    for station_line_id in searched_stations:
        line_ids.append(station_line_id.line_id)

    line_names = []
    for line_id in line_ids:
        line_names.append(await METRO_CONTROLLER.get_line_name(line_id=str(line_id)))

    if searched_stations == []:
        await message.reply(
            text=UserCommand.STATION_NOT_FOUND_TEXT.format(text=text)
        )
        return

    await message.reply(
        text="Найденные станции:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"{station.name.title()} ({line_name[0]})",
                    callback_data=f"set_station:{city_id}:{station.station_id}"
                )] for station, line_name in zip(searched_stations, line_names)
            ]
        )
    )


@APP.on_callback_query(regex_filter(r"set_station:\d+:\d+"))  # set_station:{city_id}:{station_id}
async def set_station_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    _, city_id, station_id = callback_query.data.split(":")

    second_station_data = await METRO_CONTROLLER.get_station_data(
        station_id=int(station_id),
        city_id=city_id
    )
    second_station_id = second_station_data.station_id

    try:
        first_station_id = STATE_MANAGER.get_state_data(
            state_id=user_id,
            state_data_name="first_station"
        )
    except StateNotFound:
        await APP.send_message(
            chat_id=user_id,
            text=UserCommand.STATION_ERROR_TEXT,
            reply_markup=Keyboards.ERROR_KEYBOARD
        )
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

    await callback_query.message.delete()

    first_station_id = int(first_station_id)
    nodes = []

    all_nodes = await METRO_CONTROLLER.get_nodes(city_id=city_id)
    for row in all_nodes:
        nodes.append(row[0])

    init_graph = {}
    for node in nodes:
        init_graph[node] = {}

    all_data = await METRO_CONTROLLER.get_all_data(city_id=city_id)
    for row in all_data:
        init_graph[row[2]][row[3]] = row[4]

    graph = Graph(nodes, init_graph)

    previous_nodes, shortest_path = dijkstra_algorithm(
        graph=graph, start_node=first_station_id
    )

    result = []
    path = []
    node = second_station_id
    try:
        while node != first_station_id:
            path.append(node)
            node = previous_nodes[node]
        path.append(first_station_id)
    except (KeyError):
        await APP.send_message(
            chat_id=user_id,
            text=UserCommand.STATION_ERROR_TEXT,
            reply_markup=Keyboards.ERROR_KEYBOARD
        )
    last_station_name = None
    last_line_id = None
    for station_id in path:
        station = await METRO_CONTROLLER.get_station_data(station_id, city_id)
        if last_line_id != station.line_id:
            result.append(last_station_name)
            result.append(station.name.title())
            last_line_id = station.line_id
        last_station_name = station.name.title()

    last_station = await METRO_CONTROLLER.get_station_data(path[-1], city_id)
    result.append(last_station.name.title())

    route_text = ""
    for idx, station in enumerate(result[:0:-1]):
        route_text += "%s\n%s\n" % (
            station,
            "🚶" if (idx + 1) % 2 == 0 else "⬇️"
        )

    route_time = shortest_path[second_station_id]//60

    example = (
        f"Найден лучший маршрут в {route_time} минут\n\n"
        f"{route_text[:-2]}\n\n"
        " 🚶 <i>означает пересадку</i>"
    )

    if first_station_id != second_station_id:
        await APP.send_message(
            chat_id=user_id,
            text=example
        )

        await APP.send_message(
            chat_id=user_id,
            text=UserCommand.END_TEXT,
            reply_markup=Keyboards.END_KEYBOARD
        )
    elif first_station_id == second_station_id:
        await APP.send_message(
            chat_id=user_id,
            text=UserCommand.EXCEPTION_TEXT,
            reply_markup=Keyboards.ERROR_KEYBOARD
        )


@APP.on_callback_query(regex_filter("metro_map"))
async def metro_map_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    city_id = await USER_CONTROLLER.search_city(user_id=user_id, )
    await callback_query.edit_message_text(
        text="Хорошей поездки! ❤"
    )
    if city_id == 1:
        await APP.send_photo(
            chat_id=user_id,
            photo=SPB_MAP
        )
    elif city_id == 2:
        await APP.send_photo(
            chat_id=user_id,
            photo=MOSCOW_MAP
        )
    await APP.send_message(
        chat_id=user_id,
        text=UserCommand.MENU_TEXT,
        reply_markup=Keyboards.MENU_KEYBOARD
    )
