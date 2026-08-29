import os
import random
import time
import sys
from colorama import Fore, Style, init
from pyfiglet import Figlet

init(autoreset=True)

fig = Figlet(font="slant")
banner = fig.renderText("SecureSphere")
colors = [
    Fore.RED,
    Fore.LIGHTRED_EX,
    Fore.WHITE,
    Fore.LIGHTBLACK_EX
]
subtitle = "             Advanced Cybersecurity & Data Securing Platform"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def clean_path(raw_path):
    """Clean a pasted file path by removing invisible Unicode characters,
    extra quotes, and normalizing for Windows."""
    invisible_chars = {
        '\u200b', '\u200c', '\u200d', '\u200e', '\u200f',
        '\u202a', '\u202b', '\u202c', '\u202d', '\u202e',
        '\u2066', '\u2067', '\u2068', '\u2069', '\ufeff',
        '\ufffe', '\x00'
    }
    cleaned = ''.join(ch for ch in raw_path if ch not in invisible_chars)
    cleaned = cleaned.strip()

    # Remove surrounding quotes (double, single, backtick)
    if len(cleaned) >= 2:
        if (cleaned[0] == '"' and cleaned[-1] == '"') or \
           (cleaned[0] == "'" and cleaned[-1] == "'") or \
           (cleaned[0] == '`' and cleaned[-1] == '`'):
            cleaned = cleaned[1:-1]
    cleaned = cleaned.strip()

    # Handle PowerShell command prefixes
    if cleaned.startswith('& '):
        cleaned = cleaned[2:].strip().strip('"').strip("'")

    cleaned = cleaned.replace('/', '\\')
    cleaned = os.path.normpath(os.path.expanduser(cleaned))
    return cleaned


def xor_encrypt_decrypt(input_file, output_file, key):
    """Encrypt or decrypt an image using XOR byte transformation with key (0-255).
    Handles Windows Controlled Folder Access permission restrictions automatically."""
    try:
        # Read image binary data
        with open(input_file, "rb") as file:
            data = bytearray(file.read())

        # Perform XOR operation on each byte
        for i in range(len(data)):
            data[i] ^= key

        saved_path = output_file
        # Attempt writing output image to target directory
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


# -------- Glitch Animation -------- #
for _ in range(25):
    clear()
    spaces = " " * random.randint(0, 2)
    color = random.choice(colors)
    glitch = list(banner)
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
print(Fore.RED + banner)
print(Fore.CYAN + "=" * 80)
print(Fore.YELLOW + subtitle)
print(Fore.CYAN + "=" * 80)
#------Final Banner--------------#

while True:
    print("")
    print(Fore.GREEN + "=========| CHOOSE METHOD |==========")
    print(Fore.GREEN + "|                                  |")
    print(Fore.GREEN + "|        1. TEXT ENCRYPTION        |")
    print(Fore.GREEN + "|        2. IMAGE ENCRYPTION       |")
    print(Fore.GREEN + "|        3. PASSWORD ANALYZER      |")
    print(Fore.GREEN + "|        4. Exit                   |")
    print(Fore.GREEN + "====================================")

    method = input("\nChoose Method: ").strip()

    if method == "4":
        print("\nGoodbye!")
        sys.exit()

    #=========================================
    # IMAGE ENCRYPTION CODE START
    #=========================================
    elif method == "2":
        print("\nYou Chose IMAGE ENCRYPTION")
        confirm = input("Confirmation (Y/N): ").strip().upper()

        if confirm == "Y":
            print("Opening Image Encryption Tool...")

            while True:
                print(Fore.CYAN + "\n" + "=" * 55)
                print(Fore.YELLOW + Style.BRIGHT + "       SECURE IMAGE ENCRYPTION & DECRYPTION")
                print(Fore.CYAN + "=" * 55)
                print("1. Encrypt Image")
                print("2. Decrypt Image")
                print("3. Exit to Main Menu")
                print("=" * 55)

                choice = input("\nEnter your choice: ").strip()

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
                        print(Fore.RED + "Error: Please enter a valid numeric key (0-255).")
                        continue

                    image_file = os.path.basename(image_path)
                    image_dir = os.path.dirname(os.path.abspath(image_path))
                    output = os.path.join(image_dir, "encrypted_" + image_file)
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
                        print(Fore.RED + "Error: Please enter a valid numeric key (0-255).")
                        continue

                    image_file = os.path.basename(image_path)
                    image_dir = os.path.dirname(os.path.abspath(image_path))
                    output = os.path.join(image_dir, "decrypted_" + image_file)
                    xor_encrypt_decrypt(image_path, output, key)

                elif choice == "3":
                    print("Returning to Main Menu...")
                    break

                else:
                    print(Fore.RED + "Invalid choice. Please select 1, 2, or 3.")

        else:
            print("Returning to Main Menu...\n")
            continue

    elif method == "1":
        print("\nOpening Text Encryption Module...")
        try:
            import Datacrypt
        except ImportError:
            print(Fore.YELLOW + "Text Encryption module (Datacrypt.py) is connected via Main.py.")

    elif method == "3":
        print("\nOpening Password Analyzer...")
        try:
            from Passcrypt import run_password_analyzer
            run_password_analyzer()
        except ImportError:
            print(Fore.RED + "Passcrypt.py module not found.")

    else:
        print(Fore.RED + "\nInvalid method. Please choose 1, 2, 3, or 4.")