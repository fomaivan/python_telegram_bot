import sqlite3


def make_crypto_dict():
    arr = []
    with open("crypto_list.csv") as file:
        for line in file:
            arr.append(line.strip().split(','))

    first = [elem[0] for elem in arr]
    second = [elem[1] for elem in arr]
    return dict(zip(first, second))


class DataBase:
    def __init__(self, name_base):
        self.connect = sqlite3.connect(name_base, check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS crypto_list
                               (user_id INTEGER, name_crypto TEXT)""")
        self.connect.commit()
        self.crypto_dict = make_crypto_dict()

    def start_command(self, user_id):
        temp = self.cursor.execute("""SELECT user_id, name_crypto
                                              FROM crypto_list
                                              WHERE user_id = ? AND name_crypto = ?""",
                                              (user_id, "BTC"))
        if temp.fetchone() is None:
            self.cursor.execute("""INSERT INTO crypto_list (user_id, name_crypto) VALUES (?, ?);""",
                                               (user_id, 'BTC'))
            self.connect.commit()

    def add_name(self, user_id, name_crypto):
        if name_crypto not in self.crypto_dict:
            return None
        temp = self.cursor.execute("""SELECT user_id, name_crypto FROM crypto_list
                            WHERE user_id = ? AND name_crypto = ?""",
                            (user_id, name_crypto))
        if temp.fetchone() is not None:
            return False
        self.cursor.execute("""INSERT INTO crypto_list (user_id, name_crypto) VALUES (?, ?);""",
                               (user_id, name_crypto))
        self.connect.commit()
        return True

    def all_crypto(self, user_id):
        temp = self.cursor.execute(f"""SELECT * FROM crypto_list
                                        WHERE user_id = {user_id}""")
        result = list()
        for item in temp.fetchall():
            result.append(item[1])
        return result

    def del_crypto_name(self, user_id, name_crypto):
        temp = self.cursor.execute("""SELECT user_id, name_crypto FROM crypto_list
                                      WHERE user_id = ? AND name_crypto = ?""",
                                      (user_id, name_crypto))
        if temp.fetchone() is None:
            return False
        self.cursor.execute("""DELETE FROM crypto_list WHERE user_id = ?
                               AND name_crypto = ?""", (user_id, name_crypto))
        self.connect.commit()
        return True
