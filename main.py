import pymysql
from config import host, user, password, db_name


try:
    connection = pymysql.connect(
        host = host,
        port = 3306,
        user = user,
        password = password,
        database = db_name,
        cursorclass = pymysql.cursors.DictCursor
    )
    print('successfully connected...')
    print('#' * 20)

    try:

        # create table
        # with connection.cursor() as cursor:
        #     create_table_query = "CREATE TABLE `users`(id int AUTO_INCREMENT," \
        #                          " name varchar(32)," \
        #                          " password varchar(32)," \
        #                          " email varchar(32), PRIMARY KEY(id));"
        #     cursor.execute(create_table_query)
        #     print('Table created successfully')

        #insert data
        # with connection.cursor() as cursor:
        #     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Anna', 'qwerty', 'mail@gmail.com');"
        #     cursor.execute(insert_query)
        #     connection.commit()

        # insert data
        # with connection.cursor() as cursor:
        #     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Victor', 'qwerty2', 'mail22@gmail.com');"
        #     cursor.execute(insert_query)
        #     connection.commit()

        # # insert data
        # with connection.cursor() as cursor:
        #     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Andrey', 'qwerty3', 'mail33@gmail.com');"
        #     cursor.execute(insert_query)
        #     connection.commit()

        # update data
        # with connection.cursor() as cursor:
        #     update_query = "UPDATE `users` SET password = 'xxxXXX' WHERE name = 'Andrey';"
        #     cursor.execute(update_query)
        #     connection.commit()

        # # delete data
        # with connection.cursor() as cursor:
        #     delete_query = "DELETE FROM `users` WHERE id = 5;"
        #     cursor.execute(delete_query)
        #     connection.commit()

        # drop table
        with connection.cursor() as cursor:
            drop_table_query = "DROP TABLE `users`;"
            cursor.execute(drop_table_query)

        # select all data from table
        with connection.cursor() as cursor:
            select_all_raws = "SELECT * FROM `users`;"
            cursor.execute(select_all_raws)

            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print("#" * 20)

    finally:
        connection.close()

except Exception as ex:
    print("connection refused...")
    print(ex)




# class UserStore():
#     def __init__(self, user_name, contribution, debt=0):
#         self.contribution = contribution
#         self.debt = debt
#         self.user_name = user_name


#     def create_user(user_mane):
#         return None

# UserStore.name('Sergey')




# class MoneyBox:
#     def __init__(self, capacity, bank=0):
#         self.capacity = capacity
#         self.bank = bank

#     def can_add(self, v):
#         if self.capacity - self.bank >= v:
#             print('True' + ' Можно положить еще ' + str(self.capacity - self.bank) + ' монет')
#             return True
#         else:
#             print('False ' + ' Столько монет не войдёт, можно положить ещё ' + str(self.capacity - self.bank) + ' монет')
#             return False
#         # True, если можно добавить v монет, False иначе
# ''' Оптмизация из комментов'''
# return self.capacity - self.bank >= v

#     def add(self, v):
#         if self.can_add(v):
#             self.bank += v
#         else:
#             print('Не леззет. Можно положить только ' + str(self.capacity - self.bank))

#     def info(self):
#         print('В копилке ' + str(self.bank) + ' монет. Можно положить ещё ' + str(self.capacity - self.bank))
#         # положить v монет в копилку

# myMoneyBox = MoneyBox(10,1)
# myMoneyBox.info()


# class Buffer:
#     def __init__(self):
#         self.data = []
#
#     def add(self, *a):
#         self.data += a
#         while len(self.data) > 4:
#             print(sum(self.data[:5]))
#             self.data = self.data[5:]
#             del(self.data[:5]) # del работает быстрее, чем срез по списку
#
#     def get_current_part(self):
#         return(self.data)

# buf = Buffer()

# class Loggable:
#     def log(self, msg):
#         print(str(time.ctime()) + ": " + str(msg))



    # def get_values(k):
#     global status
#     for i in dictionary[k]:
#         if i == prnt:
#             status = True
#         else:
#             get_values(i)
#     return status


# >>> class EquipArmour:
# ...     def __call__ (self, param):
# ...         if param == 1:
# ...             self.armourEquipped = 52
# ...         else:
# ...             self.armourEquipped = -34
# ... 
# >>> equiparmour = EquipArmour()
# >>> result = equiparmour(1)
# >>> if equiparmour.armourEquipped == 34:
# ...     'say hello'