from cryptography.fernet import Fernet
def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()

def encrypt(message):
    key = load_key()
    f = Fernet(key)
    code = f.encrypt(message)
    return code
def decrypt(message):
    key = load_key()
    f = Fernet(key)
    code = f.decrypt(message)
    return code

code = encrypt("hello")
print(code)
print(decrypt(code))
#message = 10.5
#message = str(message)
#message = message.encode()
#key = load_key()
#f = Fernet(key)
#code = f.encrypt(message)
#code = str(code, 'utf-8')
# print(code)
# print(type(code))

#token = code.encode("utf-8")
#value = f.decrypt(token)
#value = str(value, 'utf-8')
#print(value)
