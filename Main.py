import os
import random
import time
import base64
import sys
import re
import string
from cryptography.fernet import Fernet
from colorama import Fore, Style, init
from pyfiglet import Figlet

init(autoreset=True)


# ==============================
# Utility
# ==============================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


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
# Image XOR Encrypt/Decrypt
# ==============================
def xor_encrypt_decrypt(input_file, output_file, key):
    """Encrypt or decrypt an image using XOR byte transformation with key (0-255).
    Handles Windows Controlled Folder Access permission restrictions automatically."""
    try:
        with open(input_file, "rb") as file:
            data = bytearray(file.read())

        # XOR every byte
        for i in range(len(data)):
            data[i] ^= key

        saved_path = output_file
        try:
            with open(output_file, "wb") as file:
                file.write(data)
        except (PermissionError, OSError):
            # Fallback to local project workspace directory if Controlled Folder Access blocks writing
            fallback_filename = os.path.basename(output_file)
            fallback_path = os.path.abspath(fallback_filename)
            with open(fallback_path, "wb") as file:
                file.write(data)
            saved_path = fallback_path

            print(Fore.YELLOW + "\n[!] Notice: Windows Security / Controlled Folder Access blocked writing to the original folder.")
            print(Fore.YELLOW + f"    The file was successfully saved to your project folder instead:")
            print(Fore.CYAN + f"    --> {fallback_path}")

        print("\n" + Fore.GREEN + "Operation completed successfully!")
        print(Fore.WHITE + "Saved Path :", Fore.LIGHTGREEN_EX + saved_path)
        print(Fore.GREEN + "=====================")
        print(Fore.GREEN + "|   TASK COMPLETE   |")
        print(Fore.GREEN + "=====================")

    except FileNotFoundError:
        print(Fore.RED + "\nError: Image file not found.")
        print(Fore.RED + "Path checked:", input_file)
    except Exception as e:
        print(Fore.RED + f"\nError during image processing: {e}")


# ==============================
# Password Analyzer
# ==============================
def analyze_password(password):
    score = 0
    feedback = []

    # Length check
    length = len(password)
    if length >= 16:
        score += 3
        feedback.append(Fore.GREEN + "  [+] Excellent length (16+ characters)")
    elif length >= 12:
        score += 2
        feedback.append(Fore.GREEN + "  [+] Good length (12+ characters)")
    elif length >= 8:
        score += 1
        feedback.append(Fore.YELLOW + "  [~] Acceptable length (8+ characters)")
    else:
        feedback.append(Fore.RED + "  [-] Too short (less than 8 characters)")

    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append(Fore.GREEN + "  [+] Contains uppercase letters")
    else:
        feedback.append(Fore.RED + "  [-] Missing uppercase letters")

    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append(Fore.GREEN + "  [+] Contains lowercase letters")
    else:
        feedback.append(Fore.RED + "  [-] Missing lowercase letters")

    # Digit check
    if re.search(r'[0-9]', password):
        score += 1
        feedback.append(Fore.GREEN + "  [+] Contains digits")
    else:
        feedback.append(Fore.RED + "  [-] Missing digits")

    # Special character check
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        score += 1
        feedback.append(Fore.GREEN + "  [+] Contains special characters")
    else:
        feedback.append(Fore.RED + "  [-] Missing special characters")

    # Repeated characters check
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append(Fore.RED + "  [-] Contains repeated characters (e.g., aaa)")

    # Sequential characters check
    sequential = False
    for i in range(len(password) - 2):
        if (ord(password[i]) + 1 == ord(password[i + 1]) == ord(password[i + 2]) - 1):
            sequential = True
            break
    if sequential:
        score -= 1
        feedback.append(Fore.RED + "  [-] Contains sequential characters (e.g., abc, 123)")

    # Common patterns check
    common_patterns = ['password', '123456', 'qwerty', 'abc123', 'letmein',
                       'admin', 'welcome', 'monkey', 'dragon', 'master',
                       'login', 'princess', 'starwars', 'passw0rd']
    if password.lower() in common_patterns:
        score = 0
        feedback.append(Fore.RED + "  [-] This is a commonly used password!")

    # Score rating
    score = max(0, min(score, 7))
    if score >= 6:
        strength = Fore.GREEN + Style.BRIGHT + "STRONG"
        bar = Fore.GREEN + "█" * score + Fore.LIGHTBLACK_EX + "░" * (7 - score)
    elif score >= 4:
        strength = Fore.YELLOW + Style.BRIGHT + "MODERATE"
        bar = Fore.YELLOW + "█" * score + Fore.LIGHTBLACK_EX + "░" * (7 - score)
    elif score >= 2:
        strength = Fore.RED + Style.BRIGHT + "WEAK"
        bar = Fore.RED + "█" * score + Fore.LIGHTBLACK_EX + "░" * (7 - score)
    else:
        strength = Fore.RED + Style.BRIGHT + "VERY WEAK"
        bar = Fore.RED + "█" * max(score, 0) + Fore.LIGHTBLACK_EX + "░" * (7 - max(score, 0))

    return score, strength, bar, feedback


def generate_strong_password(length=16):
    """Generate a random strong password."""
    if length < 8:
        length = 8
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    # Ensure at least one of each type
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()_+-="),
    ]
    password += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(password)
    return ''.join(password)


# ==============================
# Task Complete Banner
# ==============================
def print_task_complete():
    print("")
    print(Fore.GREEN + "=====================")
    print(Fore.GREEN + "|   TASK COMPLETE   |")
    print(Fore.GREEN + "=====================")


# ==============================
# Path Cleaning Utility
# ==============================
def clean_path(raw_path):
    """Clean a pasted file path by removing invisible Unicode characters,
    extra quotes, and normalizing for Windows."""
    # Step 1: Remove invisible/control Unicode characters
    # (zero-width spaces, LTR/RTL marks, BOM, etc.)
    invisible_chars = {
        '\u200b',  # zero-width space
        '\u200c',  # zero-width non-joiner
        '\u200d',  # zero-width joiner
        '\u200e',  # left-to-right mark
        '\u200f',  # right-to-left mark
        '\u202a',  # left-to-right embedding
        '\u202b',  # right-to-left embedding
        '\u202c',  # pop directional formatting
        '\u202d',  # left-to-right override
        '\u202e',  # right-to-left override
        '\u2066',  # left-to-right isolate
        '\u2067',  # right-to-left isolate
        '\u2068',  # first strong isolate
        '\u2069',  # pop directional isolate
        '\ufeff',  # byte order mark (BOM)
        '\ufffe',  # reversed BOM
        '\x00',    # null byte
    }
    cleaned = ''.join(ch for ch in raw_path if ch not in invisible_chars)

    # Step 2: Strip whitespace and various quote styles
    cleaned = cleaned.strip()
    # Remove surrounding quotes (single, double, or backtick)
    if len(cleaned) >= 2:
        if (cleaned[0] == '"' and cleaned[-1] == '"') or \
           (cleaned[0] == "'" and cleaned[-1] == "'") or \
           (cleaned[0] == '`' and cleaned[-1] == '`'):
            cleaned = cleaned[1:-1]
    cleaned = cleaned.strip()

    # Step 3: Handle PowerShell prefix (& 'path' or & "path")
    if cleaned.startswith('& '):
        cleaned = cleaned[2:].strip().strip('"').strip("'")

    # Step 4: Normalize path separators and resolve
    cleaned = cleaned.replace('/', '\\')
    cleaned = os.path.normpath(os.path.expanduser(cleaned))

    return cleaned


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
    # Random horizontal jitter
    spaces = " " * random.randint(0, 2)
    # Random color flicker
    color = random.choice(colors)
    # Randomly replace a few characters to simulate glitch
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
#  MAIN MENU LOOP
# ============================================================
while True:
    print("")
    print(Fore.GREEN + "=========| CHOOSE METHOD |==========")
    print(Fore.GREEN + "|                                  |")
    print(Fore.GREEN + "|        1. TEXT ENCRYPTION        |")
    print(Fore.GREEN + "|        2. IMAGE ENCRYPTION       |")
    print(Fore.GREEN + "|        3. PASSWORD ANALYZER      |")
    print(Fore.GREEN + "|        4. Exit                   |")
    print(Fore.GREEN + "====================================")

    method = input("\nChoose Method: ")

    if method == "4":
        print("\nGoodbye!")
        sys.exit()

    # =============================
    # TEXT ENCRYPTION
    # =============================
    elif method == "1":
        print("\nYou Chose TEXT ENCRYPTION")

        confirm = input("Confirmation (Y/N): ").upper()

        if confirm == "Y":
            print("Opening Text Encryption Tool...")

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
                    print("Returning to Main Menu...")
                    break

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
                    if not key.isalpha():
                        print(Fore.RED + "Error: Keyword must contain only letters.")
                        continue
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

        elif confirm == "N":
            print("Returning to Main Menu...\n")
            continue

        else:
            print("Invalid choice! Returning to Main Menu...\n")
            continue
    #-----------Text Encryption Complete------------------#

    # =========================================
    # IMAGE ENCRYPTION
    # =========================================
    elif method == "2":
        print("\nYou Chose IMAGE ENCRYPTION")
        confirm = input("Confirmation (Y/N): ").upper()

        if confirm == "Y":
            print("Opening Image Encryption Tool...")

            while True:
                imagecrypt_banner = r'''
                ██╗███╗   ███╗ █████╗  ██████╗ ███████╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
                ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
                ██║██╔████╔██║███████║██║  ███╗█████╗  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║
                ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║
                ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗╚██████╗██║  ██║   ██║   ██║        ██║
                ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝
                '''

                print(Fore.GREEN + imagecrypt_banner)
                print(Fore.CYAN + "=" * 90)
                print(Fore.YELLOW + Style.BRIGHT + "              Secure Image Encryption & Decryption Suite")
                print(Fore.CYAN + "=" * 90)
                print("\n========== IMAGE ENCRYPTION TOOL ==========")
                print("|                                           |")
                print("|              1. Encrypt Image             |")
                print("|              2. Decrypt Image             |")
                print("|              3. Exit                      |")
                print("|                                           |")
                print("=============================================")

                choice = input("\nEnter your choice: ")

                if choice == "1":
                    raw_input = input("Enter image path (or drag & drop): ")
                    image_path = clean_path(raw_input)

                    if not os.path.isfile(image_path):
                        print(Fore.RED + "\nError: Image file not found!")
                        print(Fore.YELLOW + "  You entered : " + raw_input)
                        print(Fore.YELLOW + "  Resolved to : " + image_path)
                        if os.path.isdir(image_path):
                            print(Fore.YELLOW + "  Note: This is a directory, not a file.")
                        print(Fore.CYAN + "  Tip: Right-click the file > 'Copy as path', then paste here.")
                        continue

                    try:
                        key = int(input("Enter numeric key (0-255): ").strip())
                        if not 0 <= key <= 255:
                            print(Fore.RED + "Error: Key must be between 0 and 255.")
                            continue
                    except ValueError:
                        print(Fore.RED + "Error: Please enter a valid number.")
                        continue

                    image_dir = os.path.dirname(os.path.abspath(image_path))
                    output = os.path.join(image_dir, "encrypted_" + os.path.basename(image_path))
                    xor_encrypt_decrypt(image_path, output, key)

                elif choice == "2":
                    raw_input = input("Enter encrypted image path (or drag & drop): ")
                    image_path = clean_path(raw_input)

                    if not os.path.isfile(image_path):
                        print(Fore.RED + "\nError: Encrypted image file not found!")
                        print(Fore.YELLOW + "  You entered : " + raw_input)
                        print(Fore.YELLOW + "  Resolved to : " + image_path)
                        if os.path.isdir(image_path):
                            print(Fore.YELLOW + "  Note: This is a directory, not a file.")
                        print(Fore.CYAN + "  Tip: Right-click the file > 'Copy as path', then paste here.")
                        continue

                    try:
                        key = int(input("Enter numeric key (0-255): ").strip())
                        if not 0 <= key <= 255:
                            print(Fore.RED + "Error: Key must be between 0 and 255.")
                            continue
                    except ValueError:
                        print(Fore.RED + "Error: Please enter a valid number.")
                        continue

                    image_dir = os.path.dirname(os.path.abspath(image_path))
                    output = os.path.join(image_dir, "decrypted_" + os.path.basename(image_path))
                    xor_encrypt_decrypt(image_path, output, key)

                elif choice == "3":
                    print("Returning to Main Menu...")
                    break

                else:
                    print("Invalid choice.")
        else:
            print("Returning to Main Menu...\n")
            continue
    # =======================================
    # IMAGE ENCRYPTION COMPLETE
    # =======================================

    # =========================================
    # PASSWORD ANALYZER
    # =========================================
    elif method == "3":
        print("\nYou Chose PASSWORD ANALYZER")
        confirm = input("Confirmation (Y/N): ").upper()

        if confirm == "Y":
            print("Opening Password Analyzer...")

            while True:
                passanalyzer_banner = r'''
                ██████╗  █████╗ ███████╗███████╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗
                ██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══███╔╝██╔════╝██╔══██╗
                ██████╔╝███████║███████╗███████╗    ███████║██╔██╗ ██║███████║██║   ╚████╔╝   ███╔╝ █████╗  ██████╔╝
                ██╔═══╝ ██╔══██║╚════██║╚════██║    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝   ███╔╝  ██╔══╝  ██╔══██╗
                ██║     ██║  ██║███████║███████║    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████╗███████╗██║  ██║
                ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
                '''

                print(Fore.MAGENTA + passanalyzer_banner)
                print(Fore.CYAN + "=" * 75)
                print(Fore.YELLOW + Style.BRIGHT + "              Password Strength Analyzer & Generator")
                print(Fore.CYAN + "=" * 75)
                print("\n========== PASSWORD ANALYZER ==========")
                print("|                                      |")
                print("|     1. Analyze Password Strength     |")
                print("|     2. Generate Strong Password      |")
                print("|     3. Exit                          |")
                print("|                                      |")
                print("========================================")

                choice = input("\nEnter your choice: ")

                if choice == "1":
                    password = input("Enter password to analyze: ")

                    if not password:
                        print(Fore.RED + "Error: Password cannot be empty.")
                        continue

                    score, strength, bar, feedback = analyze_password(password)

                    print("\n" + Fore.CYAN + "=" * 45)
                    print(Fore.YELLOW + Style.BRIGHT + "       PASSWORD ANALYSIS REPORT")
                    print(Fore.CYAN + "=" * 45)
                    print(f"\n  Password Length : {len(password)}")
                    print(f"  Strength Score  : {score}/7")
                    print(f"  Strength Level  : {strength}")
                    print(f"  Strength Bar    : [{bar}" + Fore.RESET + "]")
                    print(Fore.CYAN + "\n  --- Detailed Feedback ---")
                    for line in feedback:
                        print(line)
                    print_task_complete()

                elif choice == "2":
                    try:
                        length = int(input("Enter desired password length (min 8): "))
                    except ValueError:
                        length = 16
                        print(Fore.YELLOW + "Using default length: 16")

                    generated = generate_strong_password(length)
                    print(f"\n  Generated Password: {Fore.GREEN + Style.BRIGHT}{generated}")

                    # Also show analysis of the generated password
                    score, strength, bar, feedback = analyze_password(generated)
                    print(f"  Strength Score   : {score}/7")
                    print(f"  Strength Level   : {strength}")
                    print_task_complete()

                elif choice == "3":
                    print("Returning to Main Menu...")
                    break

                else:
                    print("Invalid choice.")

        else:
            print("Returning to Main Menu...\n")
            continue

    else:
        print("\nInvalid option! Please try again.\n")
