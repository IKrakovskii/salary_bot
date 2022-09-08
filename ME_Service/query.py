import sqlite3


class Data:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def is_subscribe(self, id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `id` = ?", (id,)).fetchall()

    def add_user(self, id, name, phone, address, mail):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`id`, `name`, `phone`, `address`, `mail`) VALUES (?, ?, ?, ?, ?)",
                (id, name, phone, address, mail,))

    def get_type_by_name(self, type):
        with self.connection:
            return self.cursor.execute("SELECT `id` FROM `type`WHERE `name` = ?", (type,)).fetchall()

    def get_type(self):
        with self.connection:
            return self.cursor.execute("SELECT `name` FROM `type`").fetchall()

    def get_products_by_name_and_type(self, id_type, name):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `products` WHERE (`type` = ? AND `name_product` = ?)",
                                       (id_type, name,)).fetchall()

    def update_name(self, tg_id, new_name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `id` = ?",
                                       (new_name, tg_id,))

    def update_phone(self, tg_id, new_phone):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `phone` = ? WHERE `id` = ?", (new_phone, tg_id,))

    def update_address(self, tg_id, new_address):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `address` = ? WHERE `id` = ?", (new_address, tg_id,))

    def update_mail(self, tg_id, new_mail):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `mail` = ? WHERE `id` = ?", (new_mail, tg_id,))

    def get_products_by_type_id(self, type_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `products` WHERE `type` = ?", (type_id,)).fetchall()

    def get_product(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `products`").fetchall()
