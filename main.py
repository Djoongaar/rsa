import math
import random

from sympy import randprime


class KeyGenerator:
    """
    Класс генерирует пару ключей для зашифрования / расшифрования
    (public_key / secret_key) и другие связанные с ними элементы:
    self.p - Большое простое число p
    self.q - Большое простое число q, но такое что |p-q| - тоже большое
    self.module - Модуль алгоритма
    self.euler - Значение фугкции Эйлера
    """
    sieve = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
        107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
        227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
        349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
        467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
        613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
        751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883,
        887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
    ]

    def __init__(self, p_size: int, q_size: int, prefix: str = "rsa"):
        self.__p = self.get_primary_num(p_size)
        self.__q = self.get_primary_num(q_size)
        self.__module = self.__p * self.__q
        self.__euler = (self.__p - 1) * (self.__q - 1)
        self.__public_key = self.__get_public_key(p_size + q_size)
        self.__secret_key = self.__get_secret_key()
        self.__write_keys(prefix)

    @staticmethod
    def get_primary_num(n: int) -> int:
        """ Возвращает простое число заданной длины (в битах) """

        while True:
            num = randprime(2 ** (n - 1), 2 ** n - 1)
            # Берем только числа со старшим битом 1
            # иначе будет не верная разрядность
            if num >> n - 1 != 1:
                break
            # Проверяем простоту числа по решету Эратосфена
            for i in KeyGenerator.sieve:
                if num % i == 0:
                    break
            # Запускаем тест Ферма
            if KeyGenerator.test_fermat(num, n, 3):
                return num

    @staticmethod
    def get_random_with_size(n: int) -> int:
        """ Возвращает число взаимнопростое с заданным """

        while True:
            num = random.randrange(2 ** (n - 1), 2 ** n - 1)
            # Берем только числа со старшим битом 1
            # иначе будет не верная разрядность
            if num >> n - 1 == 1:
                return num

    @staticmethod
    def test_fermat(num: int, n: int, iterations: int) -> bool:
        """
        Проверка на простоту числа
        :param num: Число для проверки
        :param n: Модуль алгоритма
        :param iterations: Количество итераций тестирования
        :return:
        """
        for i in range(iterations):
            a = random.randrange(2, num - 1)
            r = pow(a, num-1, n)
            if r != 1:
                return False
        return True

    def __euclidean(self) -> int:
        """
        Расширенный алгоритм Евклида
        :return: Число обратное числу e
        """
        d = 0
        x1 = 0
        x2 = 1
        y1 = 1
        temp_phi = self.__euler
        e = self.__public_key

        while e > 0:
            temp1 = temp_phi // e
            temp2 = temp_phi - temp1 * e
            temp_phi = e
            e = temp2

            x = x2 - temp1 * x1
            y = d - temp1 * y1

            x2 = x1
            x1 = x
            d = y1
            y1 = y

        if temp_phi == 1:
            return d + self.__euler

    def __get_public_key(self, key_size) -> int:
        """ Выбирает взаимнопростое число с self.euler и записывает его в файл """
        e = self.get_random_with_size(key_size)
        g = math.gcd(e, self.__euler)
        while g != 1:
            e = self.get_random_with_size(key_size)
            g = math.gcd(e, self.__euler)
        return e

    def __get_secret_key(self) -> int:
        """
        Вычисляет обратное значение от self.public_key, то есть чтобы
        self.public_key * self.secret_key = 1 (по модулю self.euler)
        """
        return self.__euclidean()

    def __write_keys(self, prefix: str) -> None:
        public_key_path = "{}.pub".format(prefix)
        secret_key_path = "{}.secret".format(prefix)

        public_key = hex(self.__public_key)
        secret_key = hex(self.__secret_key)

        with open(public_key_path, "w") as public_key_file:
            public_key_file.write(public_key)

        with open(secret_key_path, "w") as secret_key_file:
            secret_key_file.write(secret_key)
