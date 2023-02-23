# -*- coding: utf-8 -*-

import sqlite3

db = sqlite3.connect("metro.db")
c = db.cursor()
# c.execute("CREATE TABLE station (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, city_id INTEGER NOT NULL, name TEXT NOT NULL, FOREIGN KEY (city_id)  REFERENCES city (id))")
# c.execute("CREATE TABLE city (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL)")
# c.execute("CREATE TABLE way (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, city_id INTEGER NOT NULL, station1 TEXT NOT NULL, station2 TEXT NOT NULL, move_time INTEGER NOT NULL)")

# c.executemany("INSERT INTO station(city_id, name) VALUES (1, ?)",  (nodes))
c.execute("INSERT INTO user VALUES (762633572, NULL, '2019-01-12')")
# c.execute("SELECT * FROM user")
# c.executemany("INSERT INTO denis(city_id, name) VALUES (1, ?)",  (nodes))
# c.executemany("INSERT INTO way(city_id, station1, station2, move_time) VALUES (1, ?, ?, ?)",  (station1, station2, way))
# c.execute("CREATE TABLE user (user_id INTEGER PRIMARY KEY NOT NULL, city_id INTEGER, auth_date TEXT NOT NULL, FOREIGN KEY (city_id)  REFERENCES city (id))")
db.commit()
db.close()
