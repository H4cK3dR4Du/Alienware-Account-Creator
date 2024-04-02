import random, string, datetime

from bs4 import BeautifulSoup

class Utils:
    def __init__(self) -> None:
        pass

    def _password(self) -> str:
        length = random.randint(12, 14)
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def _username(self) -> str:
        user = "H4cK3dR4Du"
        numbers = ''.join(random.choices(string.digits, k=8))
        return user + numbers
    
    def _time() -> str:
        return "{:%H:%M:%S}".format(datetime.datetime.now())