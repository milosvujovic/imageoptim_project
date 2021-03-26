from cryptography.fernet import Fernet
key = Fernet.generate_key()
id = 1
f = Fernet(key)
token = f.encrypt(str(id).encode())
token = str(token, 'utf-8')
print(token)

token = token.encode()
print(type(token))
value = f.decrypt(token)
print(value)
