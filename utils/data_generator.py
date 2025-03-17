from faker import Faker

class DataGenerator:
    def init(self):
        self.fake = Faker()

    def generate_username(self):
        """Генерирует случайное имя пользователя"""
        return self.fake.user_name()

    def generate_password(self):
        """Генерирует случайный пароль"""
        return self.fake.password(length=8)

    def generate_email(self):
        """Генерирует случайный email"""
        return self.fake.email()

    def generate_full_name(self):
        """Генерирует полное имя"""
        return self.fake.name()

    def generate_address(self):
        """Генерирует случайный адрес"""
        return self.fake.address()

    def generate_phone_number(self):
        """Генерирует случайный номер телефона"""
        return self.fake.phone_number()

    def generate_product_name(self):
        """Генерирует случайное название товара"""
        return self.fake.word()

    def generate_random_data(self):
        """Генерирует случайный набор данных для теста"""
        data = {
            'username': self.generate_username(),
            'password': self.generate_password(),
            'email': self.generate_email(),
            'full_name': self.generate_full_name(),
            'address': self.generate_address(),
            'phone_number': self.generate_phone_number(),
            'product_name': self.generate_product_name()
        }
        return data
