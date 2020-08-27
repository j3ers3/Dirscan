import random
from string import ascii_lowercase, digits

def randomString(length=8):
    """
    生成随机字母串
    """
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])


def randomDigits(length=8):
    """
    生成随机数字串
    """
    return ''.join([random.choice(digits) for _ in range(length)])


def randomMD5(length=10, hex=True):
    """
    生成随机MD5键值对
    """
    plain = randomDigits(length)
    m = hashlib.md5()
    m.update(plain)
    cipher = m.hexdigest() if hex else m.hexdigest()[8:-8]
    return [plain, cipher]
