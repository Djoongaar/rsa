import math


class RSA:
    def __init__(self, public_key_path: str = None, secret_key_path: str = None):
        self.__public_key = None
        self.__public_key_int = None
        self.__secret_key = None
        self.__secret_key_int = None
        self.__euler = None
        self.__euler_int = None
        self.__module = None
        self.__module_int = None
        self.__block_size = None
        self.__get_keys(public_key_path, secret_key_path)

    def __get_keys(self, public_key_path, secret_key_path):
        if public_key_path:
            with open(public_key_path, 'r') as f:
                raw_data = f.read().split("/")
                self.__public_key = raw_data[0]
                self.__public_key_int = int(raw_data[0], 0)
                self.__module = raw_data[1]

        if secret_key_path:
            with open(secret_key_path, 'r') as f:
                raw_data = f.read().split("/")
                self.__secret_key = raw_data[0]
                self.__secret_key_int = int(raw_data[0], 0)
                self.__module = raw_data[1]

        if self.__module:
            self.__module_int = int(self.__module, 0)
            self.__block_size = int(math.log(self.__module_int, 2))

    @staticmethod
    def __read_file_as_binary(file_path: str) -> bytearray:
        with open(file_path, "rb") as file:
            open_text = bytearray(file.read())
        return open_text

    @staticmethod
    def __get_text_bin(open_text: bytearray):
        result_bits = bin(0)
        for i in range(len(open_text)):
            result_bits += bin(int.from_bytes(open_text[i*8:(i+1)*8], byteorder="big", signed=False))[2:]
        return result_bits

    def encrypt_block(self, block: bin) -> bin:
        block_integer = int(block, 2)

        block_encrypt = pow(block_integer, self.__public_key_int, self.__module_int)

        # Тут длинну блоков проверил - всё работает нормально
        # print("RAW: ", len(block))
        # print("ENC: ", len(bin(block_encrypt)) - 2)

        return bin(block_encrypt)

    def encrypt(self, path_to_file: str) -> bytearray:
        with open(path_to_file, mode="rb") as file:
            open_text = bytearray(file.read())

        print(len(open_text), type(open_text))

        open_text_bin = self.__get_text_bin(open_text)[2:]
        result_bytes = bytearray()

        for i in range(len(open_text_bin) // self.__block_size):
            block_bin = open_text_bin[i * self.__block_size: (i + 1) * self.__block_size]
            enc_block_bin = self.encrypt_block(block_bin)

            print(len(block_bin), type(block_bin))

            enc_block_int = int(enc_block_bin, 2)
            enc_block_bytes = int.to_bytes(enc_block_int, 128, byteorder="big", signed=False)

            print(len(enc_block_bytes), type(enc_block_bytes))

            result_bytes.extend(enc_block_bytes)

        return result_bytes

    def decrypt(self, path_to_file: str):
        encrypt_text = self.encrypt(path_to_file)

        result_bytes = bytearray()

        for i in range(len(encrypt_text) // 8):
            block = encrypt_text[i * self.__block_size: (i + 1) * self.__block_size]
            # print(block)

        return result_bytes

    def __str__(self):
        return {
            'public_key': self.__public_key,
            'public_key_int': self.__public_key_int,
            'secret_key': self.__secret_key,
            'secret_key_int': self.__secret_key_int,
            'module': self.__module,
            'module_int': self.__module_int,
            'block_size': self.__block_size
        }
