# -*- coding: utf-8 -*-

import sqlite3

db = sqlite3.connect("spb.db")
c = db.cursor()
# c.execute("CREATE TABLE station (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, city_id INTEGER NOT NULL, name TEXT NOT NULL, FOREIGN KEY (city_id)  REFERENCES city (id))")
# c.execute("CREATE TABLE city (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL)")
# c.execute("CREATE TABLE way (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, city_id INTEGER NOT NULL, station1 TEXT NOT NULL, station2 TEXT NOT NULL, move_time INTEGER NOT NULL)")
# res = c.execute("SELECT station1, station2, move_time FROM way")


# res = c.execute("SELECT * FROM way")
# data = res.fetchall()
# for row in data:
#     data.append(row)

            # db = sqlite3.connect('metro.db')
            # c = db.cursor()

            # spisok = []
            # nodes = []

            # result = c.execute("SELECT * FROM station")
            # spisok = result.fetchall()
            # for row1 in spisok:
            #     nodes.append(row1[2].title())

            # init_graph = {}
            # for node in nodes:
            #     init_graph[node] = {}


            # data = []

            # res = c.execute("SELECT * FROM way")
            # data = res.fetchall()

            # for row in data:
            #     init_graph[row[2].title()][row[3].title()] = row[4]

            # print(init_graph)

            # db.close()

# для переноса первоначального кода
        # db = sqlite3.connect("metro.db")
        # c = db.cursor()

        # for station1, station_dict in init_graph.items():
        #     try:
        #         for station2, move_time in station_dict.items():
        #             c.execute(
        #                 "INSERT INTO way(city_id, station1, station2, move_time) VALUES (?, ?, ?, ?)", (
        #                     1, station1.lower(), station2.lower(), move_time
        #                 )
        #             )
        #     except IndexError:
        #         pass

        # db.commit()
        # db.close()

station1 = []
station2 = []
for i in range(0, 76):
    res = c.execute("SELECT station1, station2, move_time FROM way")
    station1.append((res.fetchall()[i])[0])
for i in range(0, 76):
    res = c.execute("SELECT station1, station2, move_time FROM way")
    station2.append((res.fetchall()[i])[1])

station2_id = []
station1_id = []
for hui, penis in zip(station1, station2):
    row = c.execute("SELECT id FROM station WHERE name LIKE ?", (hui, ))
    station1_id.append(row.fetchone()[0] + 366)
    row2 = c.execute("SELECT id FROM station WHERE name LIKE ?", (penis, ))
    station2_id.append(row2.fetchone()[0] + 366)

move_time = []
for i in range(0, 76):
    res = c.execute("SELECT station1, station2, move_time FROM way")
    move_time.append((res.fetchall()[i])[2] * 60)

graph = {}
for s1, s2, mt in zip(station1_id, station2_id, move_time):
    print(s1, s2, mt)
# res = c.execute("SELECT * FROM station")
# stations_list = res.fetchall()

# stations = []
# for station in stations_list:
#     stations.append(station[2])


# line_id = [[25], [25], [25], [22], [25], [21], [25], [23], [23], [22], [23], [21], [23], [24], [23], [22], [24], [22], [21], [22], [21], [21],
#            [21], [24], [24], [24], [25], [25], [25], [25], [24], [24], [24], [23], [23], [23], [22], [22], [22], [22], [22], [22], [22], [21],
#            [21], [21], [21], [21], [21], [21], [21], [25], [25], [25], [25], [25], [25], [23], [23], [23], [23], [22], [22], [22], [22], [22],
#            [22], [21], [21], [21], [21], [21]]

# line_id = [25, 25, 25, 22, 25, 21, 25, 23, 23, 22, 23, 21, 23, 24, 23, 22, 24, 22, 21, 22, 21, 21,
#            21, 24, 24, 24, 25, 25, 25, 25, 24, 24, 24, 23, 23, 23, 22, 22, 22, 22, 22, 22, 22, 21,
#            21, 21, 21, 21, 21, 21, 21, 25, 25, 25, 25, 25, 25, 23, 23, 23, 23, 22, 22, 22, 22, 22,
#            22, 21, 21, 21, 21, 21]

# c.executemany("INSERT INTO station(city_id, name) VALUES (1, ?)",  (nodes))
# c.execute("INSERT INTO user VALUES (762633572, NULL, '2019-01-12')")
# c.execute("SELECT * FROM user")
# c.executemany("INSERT INTO denis(city_id, name) VALUES (1, ?)",  (nodes))
# c.executemany("INSERT INTO way(city_id, station1, station2, move_time) VALUES (1, ?, ?, ?)",  (station1, station2, way))
# c.execute("CREATE TABLE user (user_id INTEGER PRIMARY KEY NOT NULL, city_id INTEGER, auth_date TEXT NOT NULL, FOREIGN KEY (city_id)  REFERENCES city (id))")
# graph = {}
# for line, nodes in zip(line_id, stations):
#     graph = {line: nodes}
#     print(graph[0])

db.commit()
db.close()

db = sqlite3.connect("metro.db")
c = db.cursor()

# for line, nodes in zip(line_id, stations):
#     graph = {line: nodes}
    # print(graph)

# c.executemany(
#     "INSERT INTO way(city_id, station1, station2, move_time) VALUES (1, ?, ?, ?)",  (zip(station1_id, station2_id, move_time))
# )

# c.executemany("INSERT INTO station(city_id, line_id, name) VALUES (1, ?, ?)",  (line, nodes ))
db.commit()
db.close()
