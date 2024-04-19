import math


class RSA:
    def __init__(self, public_key_path: str = None, secret_key_path: str = None):
        self.__public_key = None
        self.__secret_key = None
        self.__euler = None
        self.__module = None
        self.__block_size = None
        self.__get_keys(public_key_path, secret_key_path)

    def __get_keys(self, public_key_path, secret_key_path):
        if public_key_path:
            with open(public_key_path, 'r') as f:
                self.__public_key = int(f.read().split("/")[0], 0)
                self.__module = int(f.read().split("/")[1], 0)

        if secret_key_path:
            with open(secret_key_path, 'r') as f:
                self.__secret_key = int(f.read().split("/")[0], 0)
                self.__module = int(f.read().split("/")[1], 0)

        if self.__module:
            self.__block_size = int(math.log(self.__module, 2))

    def __encrypt_block(self, block: bin):
        block_integer = int(block, 2)
        block_encrypt = pow(block_integer, self.__public_key, self.__module)
        # Padding with zeros till byte size
        bytes_count = (((self.__block_size + 1) // 8) + 1) * 8
        return bin(block_encrypt)[2:].zfill(bytes_count)

    def __str__(self):
        return self.__public_key, self.__secret_key, self.__module, self.__block_size
