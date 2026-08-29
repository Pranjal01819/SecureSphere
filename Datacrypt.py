# ==============================
#  TEXT ENCRYPTION Main Program
# ==============================


import os
import random
import time
import base64
import sys
from cryptography.fernet import Fernet
from colorama import Fore, Style, init
from pyfiglet import Figlet

init(autoreset=True)


# ==============================
# Caesar Cipher
# ==============================
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# ==============================
# Vigenere Cipher
# ==============================
def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return "".join(key)
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def vigenere_encrypt(text, key):
    key = generate_key(text, key)
    cipher = ""
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            shift = ord(key[i].lower()) - ord('a')
            base_char = ord('A') if char.isupper() else ord('a')
            cipher += chr((ord(char) - base_char + shift) % 26 + base_char)
        else:
            cipher += char
    return cipher


def vigenere_decrypt(cipher, key):
    key = generate_key(cipher, key)
    text = ""
    for i in range(len(cipher)):
        char = cipher[i]
        if char.isalpha():
            shift = ord(key[i].lower()) - ord('a')
            base_char = ord('A') if char.isupper() else ord('a')
            text += chr((ord(char) - base_char - shift) % 26 + base_char)
        else:
            text += char
    return text


# ==============================
# XOR Cipher
# ==============================
def xor_encrypt(text, key):
    encrypted = ''.join(chr(ord(c) ^ key) for c in text)
    return base64.b64encode(encrypted.encode()).decode()


def xor_decrypt(cipher, key):
    decoded = base64.b64decode(cipher).decode()
    return ''.join(chr(ord(c) ^ key) for c in decoded)


# ==============================
# Base64
# ==============================
def base64_encrypt(text):
    return base64.b64encode(text.encode()).decode()


def base64_decrypt(cipher):
    return base64.b64decode(cipher).decode()


# ==============================
# Fernet Encryption
# ==============================
def generate_fernet_key():
    return Fernet.generate_key()


def fernet_encrypt(text, key):
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()


def fernet_decrypt(cipher, key):
    f = Fernet(key)
    return f.decrypt(cipher.encode()).decode()


# ==============================
# Utility
# ==============================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_task_complete():
    print("")
    print(Fore.GREEN + "=====================")
    print(Fore.GREEN + "|   TASK COMPLETE   |")
    print(Fore.GREEN + "=====================")


# ============================================================
#  STARTUP — Glitch Animation & Banner
# ============================================================
fig = Figlet(font="slant")
main_banner = fig.renderText("SecureSphere")
colors = [
    Fore.RED,
    Fore.LIGHTRED_EX,
    Fore.WHITE,
    Fore.LIGHTBLACK_EX
]
subtitle = "             Advanced Cybersecurity & Data Securing Platform"

# -------- Glitch Animation -------- #
for _ in range(25):
    clear()
    spaces = " " * random.randint(0, 2)
    color = random.choice(colors)
    glitch = list(main_banner)
    for i in range(len(glitch)):
        if glitch[i] not in ['\n', ' '] and random.random() < 0.02:
            glitch[i] = random.choice("@#$%&01<>/\\|")
    glitch = "".join(glitch)
    print(color + spaces + glitch)
    print(Fore.CYAN + spaces + "=" * 80)
    print(Fore.YELLOW + spaces + subtitle)
    print(Fore.CYAN + spaces + "=" * 80)
    time.sleep(0.06)
clear()
print(Fore.RED + main_banner)
print(Fore.CYAN + "=" * 80)
print(Fore.YELLOW + subtitle)
print(Fore.CYAN + "=" * 80)
#------Final Banner--------------#


# ============================================================
#  TEXT ENCRYPTION MENU
# ============================================================
while True:
    datacrypt_banner = r'''
    ██████╗  █████╗ ████████╗ █████╗  ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
    ██║  ██║███████║   ██║   ███████║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║
    ██║  ██║██╔══██║   ██║   ██╔══██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║
    ██████╔╝██║  ██║   ██║   ██║  ██║╚██████╗██║  ██║   ██║   ██║        ██║
    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝
    '''
    print(Fore.GREEN + datacrypt_banner)
    print(Fore.CYAN + "=" * 75)
    print(Fore.YELLOW + "               Secure Text Encryption & Decryption Suite")
    print(Fore.CYAN + "=" * 75)
    print("\n======| CHOOSE ALGORITHM |=======")
    print("|        1. Caesar Cipher        |")
    print("|        2. Vigenere Cipher      |")
    print("|        3. XOR Cipher           |")
    print("|        4. Base64               |")
    print("|        5. Fernet (AES Based)   |")
    print("|        6. Exit                 |")
    print("==================================")

    choice = input("\nChoose Algorithm: ")

    if choice == "6":
        print("Goodbye!")
        sys.exit()

    action = input("Encrypt (E) or Decrypt (D): ").upper()

    if choice == "1":
        try:
            shift = int(input("Enter Shift Value: "))
        except ValueError:
            print(Fore.RED + "Error: Please enter a valid number.")
            continue
        text = input("Enter Text: ")

        if action == "E":
            print("\nEncrypted Text:")
            print(caesar_encrypt(text, shift))
            print_task_complete()
        else:
            print("\nDecrypted Text:")
            print(caesar_decrypt(text, shift))
            print_task_complete()

    elif choice == "2":
        key = input("Enter Keyword: ")
        text = input("Enter Text: ")

        if action == "E":
            print("\nEncrypted Text:")
            print(vigenere_encrypt(text, key))
            print_task_complete()
        else:
            print("\nDecrypted Text:")
            print(vigenere_decrypt(text, key))
            print_task_complete()

    elif choice == "3":
        try:
            key = int(input("Enter Numeric Key (0-255): "))
            if not 0 <= key <= 255:
                print(Fore.RED + "Error: Key must be between 0 and 255.")
                continue
        except ValueError:
            print(Fore.RED + "Error: Please enter a valid number.")
            continue
        text = input("Enter Text: ")

        if action == "E":
            print("\nEncrypted Text:")
            print(xor_encrypt(text, key))
            print_task_complete()
        else:
            print("\nDecrypted Text:")
            print(xor_decrypt(text, key))
            print_task_complete()

    elif choice == "4":
        text = input("Enter Text: ")

        if action == "E":
            print("\nEncoded Text:")
            print(base64_encrypt(text))
            print_task_complete()
        else:
            try:
                print("\nDecoded Text:")
                print(base64_decrypt(text))
                print_task_complete()
            except Exception:
                print(Fore.RED + "Error: Invalid Base64 input.")

    elif choice == "5":
        if action == "E":
            text = input("Enter Text: ")

            key = generate_fernet_key()

            print("\nGenerated Key (Save this):")
            print(key.decode())

            cipher = fernet_encrypt(text, key)

            print("\nEncrypted Text:")
            print(cipher)
            print_task_complete()

        else:
            key = input("Enter Saved Key: ").encode()
            cipher = input("Enter Encrypted Text: ")

            try:
                print("\nDecrypted Text:")
                print(fernet_decrypt(cipher, key))
                print_task_complete()
            except Exception:
                print(Fore.RED + "Error: Invalid key or encrypted text.")

    else:
        print("Invalid Choice")

#-----------Text Encryption Complete------------------#