from faker import Faker

class DataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_username(self):
        """Генерирует случайное имя пользователя"""
        return self.fake.user_name()

    def generate_password(self):
        """Генерирует случайный пароль"""
        return self.fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
