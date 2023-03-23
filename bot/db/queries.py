# -*- coding: utf-8 -*-


class StationQuery:
    GET_CITY_DATA = "SELECT * FROM city WHERE id = ?"
    GET_CITY_METRO = "SELECT * FROM station WHERE city_id = ?"
    SEARCH_STATION = f"{GET_CITY_METRO} AND name LIKE ?"
    GET_ALL_DATA = "SELECT * FROM way WHERE city_id = ?"


class UserQuery:
    INSERT_USER = "INSERT INTO user (user_id, auth_date) VALUES (?, ?)"
    INSERT_CITY = "UPDATE user SET city_id = ? WHERE user_id = ?"
    GET_USER_DATA = "SELECT * FROM user WHERE user_id = ?"
    GET_USERS = "SELECT count(user_id) FROM user"
