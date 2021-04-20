import sqlite3
import traceback
import sys
from config import DB_FILENAME


class DBManager:
    def __init__(self, db_file=DB_FILENAME):
        try:
            self.sqlite_connection = sqlite3.connect(db_file, check_same_thread=False)
            print("База данных подключена к SQLite")
        except sqlite3.Error as error:
            print("Ошибка при подключении к SQLite", error)

    def __del__(self):
        if self.sqlite_connection:
            self.sqlite_connection.close()
            print("Соединение с SQLite закрыто")

    def getCursor(self):
        return self.sqlite_connection.cursor()

    def InsertClient(self, telegram_id, join_date, start_diet_date, diet_type_id=1):
        result = -1
        try:
            cursor = self.getCursor()
            insert_query = '''
                INSERT INTO clients 
                SELECT ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM clients WHERE telegram_id = ?
                );'''
            cursor.execute(insert_query, (
                str(telegram_id), str(join_date),
                str(start_diet_date), str(diet_type_id),
                str(telegram_id)
            ))
            self.sqlite_connection.commit()

            result = cursor.rowcount
            if result == 0:
                print("Поле telegram_id " + str(telegram_id) + " уже существует в таблице clients")
            else:
                print("Поле telegram_id " + str(telegram_id) + " успешно вставлена в таблицу clients")

            cursor.close()

        except sqlite3.Error as error:
            print("Не удалось вставить данные в таблицу clients")
            print("Класс исключения: ", error.__class__)
            print("Исключение", error.args)
            print("Подробности исключения SQLite: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            result = -1

        finally:
            return result

    def UpdateStartDietDate(self, telegram_id, start_diet_date):
        result = -1
        try:
            cursor = self.getCursor()
            update_query = '''UPDATE clients 
                              SET start_diet_date = ? 
                              WHERE telegram_id = ?;'''
            cursor.execute(update_query, (
                start_diet_date, telegram_id
            ))
            self.sqlite_connection.commit()

            result = cursor.rowcount
            if result == 0:
                print("Не удалось обновить поле start_diet_date "
                      "по telegram_id " + str(telegram_id) + " в таблице clients")
            else:
                print("Поле start_diet_date по telegram_id " + str(telegram_id) +
                      " успешно обновленно в таблице clients")

            cursor.close()

        except sqlite3.Error as error:
            print("Не удалось обновить данные в таблице clients")
            print("Класс исключения: ", error.__class__)
            print("Исключение", error.args)
            print("Подробности исключения SQLite: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            result = -1

        finally:
            return result

    def UpdateDietTypeId(self, telegram_id, diet_type_id):
        result = -1
        try:
            cursor = self.getCursor()

            update_query = '''UPDATE clients 
                              SET diet_type_id = ? 
                              WHERE telegram_id = ?;'''
            cursor.execute(update_query, (diet_type_id, telegram_id))
            self.sqlite_connection.commit()

            result = cursor.rowcount
            if result == 0:
                print("Не удалось обновить поле diet_type_id "
                      "по telegram_id " + str(telegram_id) + " в таблице clients")
            else:
                print("Поле diet_type_id по telegram_id " + str(telegram_id) +
                      " успешно обновленно в таблице clients")

            cursor.close()

        except sqlite3.Error as error:
            print("Не удалось обновить данные в таблице clients")
            print("Класс исключения: ", error.__class__)
            print("Исключение", error.args)
            print("Подробности исключения SQLite: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            result = -1

        finally:
            return result

    def SelectStartDietDate(self, telegram_id):
        result = -1
        try:
            cursor = self.getCursor()

            select_query = '''SELECT start_diet_date
                              FROM clients 
                              WHERE telegram_id = ?;'''
            cursor.execute(select_query, (telegram_id,))

            result = cursor.fetchall()[0][0]
            print("Поле start_diet_date в таблице clients по telegram_id " +
                  str(telegram_id) + " успешно получено: " + str(result))

            cursor.close()

        except sqlite3.Error as error:
            print("Не удалось получить данные в таблице clients")
            print("Класс исключения: ", error.__class__)
            print("Исключение", error.args)
            print("Подробности исключения SQLite: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            result = -1

        finally:
            return result

    def SelectDietTypeId(self, telegram_id):
        result = -1
        try:
            cursor = self.getCursor()

            select_query = '''SELECT diet_type_id
                              FROM clients 
                              WHERE telegram_id = ?;'''
            cursor.execute(select_query, (telegram_id,))

            result = cursor.fetchall()[0][0]
            print("Поле diet_type_id в таблице clients по telegram_id " +
                  str(telegram_id) + " успешно получено: " + str(result))

            cursor.close()

        except sqlite3.Error as error:
            print("Не удалось получить данные в таблице clients")
            print("Класс исключения: ", error.__class__)
            print("Исключение", error.args)
            print("Подробности исключения SQLite: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            result = -1

        finally:
            return result
