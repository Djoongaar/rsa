import math


class RSA:
    def __init__(self, public_key_path: str = None, secret_key_path: str = None):
        self.__public_key = None
        self.public_key_int = None
        self.__secret_key = None
        self.secret_key_int = None
        self.__euler = None
        self.__euler_int = None
        self.__module = None
        self.module_int = None
        self.__block_size = None
        self.__block_size_full = None
        self.__get_keys(public_key_path, secret_key_path)

    def __get_keys(self, public_key_path, secret_key_path):
        if public_key_path:
            with open(public_key_path, 'r') as f:
                raw_data = f.read().split("/")
                self.__public_key = raw_data[0]
                self.public_key_int = int(raw_data[0], 0)
                self.__module = raw_data[1]

        if secret_key_path:
            with open(secret_key_path, 'r') as f:
                raw_data = f.read().split("/")
                self.__secret_key = raw_data[0]
                self.secret_key_int = int(raw_data[0], 0)
                self.__module = raw_data[1]

        if self.__module:
            self.module_int = int(self.__module, 0)
            self.__block_size = math.floor(math.log(self.module_int, 2))
            self.__block_size_full = math.ceil(math.log(self.module_int, 2))

    @staticmethod
    def __read_file_as_binary(file_path: str) -> bytearray:
        with open(file_path, "rb") as file:
            open_text = bytearray(file.read())
        return open_text

    @staticmethod
    def __get_text_bin(open_text: bytearray) -> str:
        return bin(int.from_bytes(open_text, byteorder="big", signed=False))

    def encrypt_block(self, block: str) -> str:
        block_integer = int(block, 2)

        block_encrypt_int = pow(block_integer, self.public_key_int, self.module_int)
        block_encrypt_bin = bin(block_encrypt_int)[2:].zfill(self.__block_size_full)

        return block_encrypt_bin

    def decrypt_block(self, block: str) -> str:
        block_integer = int(block, 2)

        block_decrypt_int = pow(block_integer, self.secret_key_int, self.module_int)
        block_decrypt_bin = bin(block_decrypt_int)[2:].zfill(self.__block_size)
        return block_decrypt_bin

    def encrypt(self, path_to_file: str) -> bytearray:
        with open(path_to_file, mode="rb") as file:
            open_text = bytearray(file.read())

        open_text_bin = self.__get_text_bin(open_text)
        result_bin = ""

        blocks_count = math.ceil(len(open_text_bin) / self.__block_size)

        for i in range(1, blocks_count + 1):
            start = -(i * self.__block_size)
            end = -(i * self.__block_size - self.__block_size)

            if not end:
                end = None

            block_bin = open_text_bin[start: end]

            enc_block_bin = self.encrypt_block(block_bin)

            result_bin = enc_block_bin + result_bin

        result_int = int(result_bin, 2)

        result_bytes = bytearray(int.to_bytes(result_int, length=512, byteorder="big", signed=False))

        with open("encrypted.txt", "wb") as file:
            file.write(result_bytes)

        return result_bytes

    def decrypt(self, path_to_file: str):
        with open(path_to_file, "rb") as file:
            cipher_text = bytearray(file.read())

        cipher_text_bin = self.__get_text_bin(cipher_text)

        result_bin = ""

        blocks_count = math.ceil(len(cipher_text_bin) / self.__block_size_full)

        for i in range(1, blocks_count + 1):
            start = -(i * self.__block_size_full)
            end = -(i * self.__block_size_full - self.__block_size_full)

            if not end:
                end = None

            block_bin = cipher_text_bin[start: end]
            decr_block_bin = self.decrypt_block(block_bin)

            result_bin = decr_block_bin + result_bin

        result_int = int(result_bin, 2)
        result_bytes = bytearray(int.to_bytes(result_int, length=512, byteorder="big", signed=False))

        with open("decrypted.txt", "wb") as file:
            file.write(result_bytes)

        return result_bytes

    def __str__(self):
        return {
            'public_key': self.__public_key,
            'public_key_int': self.public_key_int,
            'secret_key': self.__secret_key,
            'secret_key_int': self.secret_key_int,
            'module': self.__module,
            'module_int': self.module_int,
            'block_size': self.__block_size,
            'block_size_full': self.__block_size_full
        }
