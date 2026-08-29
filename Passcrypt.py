import os
import re
import random
import string
import sys
import time
from colorama import Fore, Style, init
from pyfiglet import Figlet

init(autoreset=True)


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


# ==============================
# Password Analyzer Functions
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


# ============================================================
#  PASSWORD ANALYZER MAIN PROGRAM
# ============================================================
def run_password_analyzer():
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

        choice = input("\nEnter your choice: ").strip()

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
                length = int(input("Enter desired password length (min 8): ").strip())
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
            print("Returning...")
            break

        else:
            print(Fore.RED + "Invalid choice.")


if __name__ == "__main__":
    run_password_analyzer()
