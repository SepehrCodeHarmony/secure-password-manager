from cryptography.fernet import Fernet
import bcrypt
import base64

def encrypt_pass(genpassword, gensalt):

    with open('bins/peper', 'rb') as file:
        peper = file.read()

    password_1 = gensalt + peper + genpassword
    
    with open('bins/key', 'rb') as file:
        password = file.read()

    with open('bins/salt', 'rb') as file:
        salt = file.read()

    key = bcrypt.kdf(
                            password= password,
                            salt= salt,
                            desired_key_bytes=32,
                            rounds= 50)

    final_key = base64.urlsafe_b64encode(key)

    f = Fernet(final_key)
    token = f.encrypt(password_1)

    return token

def decrypt_pass(token, gensalt):

    with open('bins/peper', 'rb') as file:
        peper = file.read()

    with open('bins/key', 'rb') as file:
        password = file.read()

    with open('bins/salt', 'rb') as file:
        salt = file.read()

    key  =bcrypt.kdf(
                            password= password,
                            salt= salt,
                            desired_key_bytes=32,
                            rounds= 50)

    final_key = base64.urlsafe_b64encode(key)

    f = Fernet(final_key)
    decrypted_password = f.decrypt(token).decode()


    l = len(gensalt.decode()) + len(peper)
    decrypted_password = decrypted_password[l:]

    return decrypted_password