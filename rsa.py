class RSA:
    def __init__(self, public_key_path: str = None, private_key_path: str = None):
        self.__public_key = self.__get_public_key(public_key_path)
        self.__secret_key = self.__get_secret_key(public_key_path)
        self.__euler = None
        self.__block_length = None

    @staticmethod
    def __get_public_key(public_key_path):
        with open(public_key_path, 'r') as f:
            return f.read()

    @staticmethod
    def __get_secret_key(secret_key_path):
        with open(secret_key_path, 'r') as f:
            return f.read()


