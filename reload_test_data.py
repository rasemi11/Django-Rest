import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

c.execute("DELETE FROM car_api_app_carbrand")
c.execute("DELETE FROM car_api_app_carmodel")
c.execute("DELETE FROM car_api_app_usercar")
c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='car_api_app_carbrand';")
c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='car_api_app_carmodel';")
c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='car_api_app_usercar';")


c.execute("INSERT INTO car_api_app_carbrand "
          "(name, created_at, deleted_at)"
          "VALUES('Dacia', 'NOW', NULL), "
          "('VW', 'NOW', NULL),"
          "('Alfa', 'NOW', NULL),"
          "('Renault', 'NOW', NULL)")
conn.commit()

c.execute("INSERT INTO car_api_app_carmodel "
          "(name, created_at, deleted_at, car_brand_id) "
          "VALUES('Logan', 'NOW', NULL,  1),('Docker', 'NOW', NULL, 1),"
          "('Polo', 'NOW', NULL, 2),"
          "('Pasat', 'NOW', NULL, 2),"
          "('Golf', 'NOW', NULL, 2),"
          "('156', 'NOW', NULL, 3),"
          "('133', 'NOW', NULL, 3),"
          "('Clio', 'NOW', NULL, 4),"
          "('Megane', 'NOW', NULL, 4)")
conn.commit()

c.execute("INSERT INTO car_api_app_usercar"
          "(created_at, deleted_at, car_model_id, user_id, first_reg, odometer) "
          "VALUES('NOW', NULL, 1, 1, 'NOW', 'test odo'),"
          "('NOW', NULL, 2, 1, 'NOW', 'test odo'),"
          "('NOW', NULL, 3, 1, 'NOW', 'test odo')")
conn.commit()

conn.close()
