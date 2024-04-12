class KeyGenerator:
    """
    Класс генерирует пару ключей для зашифрования / расшифрования
    (public_key / secret_key) и другие связанные с ними элементы:
    self.p - Большое простое число p
    self.q - Большое простое число q, но такое что |p-q| - тоже большое
    self.module - Модуль алгоритма
    self.euler - Значение фугкции Эйлера
    """
    def __init__(self):
        self.p = self.get_p()
        self.q = self.get_q()
        self.module = self.p * self.q
        self.euler = (self.p - 1) * (self.q - 1)
        self.public_key = self.get_public_key()
        self.secret_key = self.get_secret_key()

    @staticmethod
    def get_p():
        return 0

    @staticmethod
    def get_q():
        return 0

    def get_public_key(self):
        """
        Выбирает взаимнопростое число с self.euler и записывает его в файл
        """
        return 0

    def get_secret_key(self):
        """
        Вычисляет обратное значение от self.public_key, то есть чтобы
        self.public_key * self.secret_key = 1 (по модулю self.euler)
        """
        return 0
