from itertools import cycle
import base64


def encrypt_message(message, shared_key):
    encrypted_message = ""
    for c in message:
        encrypted_message += chr(ord(c) + shared_key)
    return encrypted_message


def decrypt_message(encrypted_message, shared_key):

    # decrypted_message = ""
    # for c in encrypted_message:
    #     decrypted_message += chr(ord(c) - shared_key)
    # return decrypted_message

    decryptedMessage = "".join(
        chr(ord(c) ^ ord(k)) for c, k in zip(encrypted_message, cycle(shared_key))
    )
    return decryptedMessage
