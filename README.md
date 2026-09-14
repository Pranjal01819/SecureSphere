

Readme · MD
<div align="center">
  🛡️ SecureSphere
 
**Advanced Cybersecurity & Data Securing Platform**
 
A terminal-based Python toolkit for text encryption, image encryption, and password security analysis — with a colorful CLI, ASCII banners, and a glitch-style startup animation.
 
![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
 
</div>
---
 
## 📖 Table of Contents
 
- [Features](#-features)
- [Demo](#-demo)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Security Notes](#-security-notes)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
---
 
## ✨ Features
 
### 🔐 Text Encryption
Encrypt and decrypt text using five different algorithms:
 
| Algorithm | Type | Key Required |
|---|---|---|
| **Caesar Cipher** | Classic shift cipher | Numeric shift |
| **Vigenère Cipher** | Polyalphabetic cipher | Alphabetic keyword |
| **XOR Cipher** | Byte-level XOR, Base64-encoded output | Numeric key (0–255) |
| **Base64** | Simple encoding/decoding | None |
| **Fernet (AES-based)** | Strong symmetric encryption | Auto-generated key |
 
### 🖼️ Image Encryption
Encrypt or decrypt image files using byte-level XOR transformation with a numeric key (0–255).
- Auto-detects and cleans pasted/drag-and-dropped file paths (quotes, invisible Unicode characters, PowerShell prefixes).
- Automatically falls back to saving in the project folder if Windows Controlled Folder Access blocks writing to the original location.
### 🔑 Password Analyzer & Generator
- **Analyze** — scores password strength out of 7 based on:
  - Length
  - Uppercase / lowercase / digit / special character variety
  - Repeated characters (e.g. `aaa`)
  - Sequential characters (e.g. `abc`, `123`)
  - Common password patterns (`password`, `123456`, `qwerty`, etc.)
  - Returns a visual strength bar (`█████░░`) plus detailed feedback
- **Generate** — creates strong random passwords of a chosen length, guaranteed to include uppercase, lowercase, digits, and special characters.
---
 
## 🎬 Demo
 
```
=========| CHOOSE METHOD |==========
|                                  |
|        1. TEXT ENCRYPTION        |
|        2. IMAGE ENCRYPTION       |
|        3. PASSWORD ANALYZER      |
|        4. Exit                   |
====================================
 
Choose Method: 3
 
You Chose PASSWORD ANALYZER
Confirmation (Y/N): Y
 
  Password Length : 18
  Strength Score  : 7/7
  Strength Level  : STRONG
  Strength Bar    : [███████]
 
  --- Detailed Feedback ---
  [+] Excellent length (16+ characters)
  [+] Contains uppercase letters
  [+] Contains lowercase letters
  [+] Contains digits
  [+] Contains special characters
```
 
---
 
## 📦 Requirements
 
- Python 3.7+
- Dependencies:
  - [`cryptography`](https://pypi.org/project/cryptography/) — Fernet (AES-based) encryption
  - [`colorama`](https://pypi.org/project/colorama/) — cross-platform colored terminal output
  - [`pyfiglet`](https://pypi.org/project/pyfiglet/) — ASCII art banner
## ⚙️ Installation
 
```bash
# Clone the repository
git clone <your-repo-url>
cd securesphere
 
# Install dependencies
pip install -r requirements.txt
```
 
Or install dependencies directly:
 
```bash
pip install cryptography colorama pyfiglet
```
 
<details>
<summary><strong>Optional: create a <code>requirements.txt</code></strong></summary>
```
cryptography
colorama
pyfiglet
```
 
</details>
---
 
## 🚀 Usage
 
Run the main script:
 
```bash
python Main.py
```
 
You'll see a glitch-animated banner, then the main menu. Each tool (Text Encryption, Image Encryption, Password Analyzer) opens its own sub-menu with its own banner and options, and you can return to the main menu at any time by exiting a sub-menu.
 
### Text Encryption
1. Choose `1` from the main menu, confirm with `Y`.
2. Pick an algorithm (Caesar, Vigenère, XOR, Base64, or Fernet).
3. Choose `E` to encrypt or `D` to decrypt.
4. Enter the required key / shift / keyword and your text.
> ⚠️ For **Fernet**, save the generated key immediately — it's required to decrypt the text later and is not stored anywhere.
 
### Image Encryption
1. Choose `2` from the main menu, confirm with `Y`.
2. Choose `1` to encrypt or `2` to decrypt an image.
3. Enter the image path (drag & drop supported) and a numeric key (0–255).
4. The output is saved alongside the original file, prefixed with `encrypted_` or `decrypted_`.
### Password Analyzer
1. Choose `3` from the main menu, confirm with `Y`.
2. Choose `1` to analyze a password's strength, or `2` to generate a new strong password.
---
 
## 🗂️ Project Structure
 
```
securesphere/
├── Main.py           # Entry point — menus, banners, and all tool logic
└── requirements.txt  # Python dependencies (optional, see above)
```
 
---
 
## 🔒 Security Notes
 
- **Caesar** and **Vigenère** ciphers are classical/educational ciphers — easily broken with frequency analysis. Do not use them for real-world sensitive data.
- **XOR** encryption (text or image) is only as strong as its key; a single-byte key (0–255) is trivially brute-forced. It's best treated as an obfuscation exercise, not real security.
- **Fernet** is the only cryptographically strong option here (AES 128 in CBC mode with HMAC authentication, via the `cryptography` library). Keep generated keys safe — losing a key means losing access to the encrypted data.
- This tool is intended for **learning and experimentation** with cryptographic concepts, not for protecting sensitive production data.
---
 
## 🛣️ Roadmap
 
Ideas for future improvements:
- [ ] Save/load encryption keys to/from file
- [ ] Support batch image encryption (whole folders)
- [ ] Add RSA (asymmetric) encryption option
- [ ] Export password analysis reports to file
- [ ] Command-line arguments for non-interactive/scripted use
## 🤝 Contributing
 
Contributions, issues, and feature requests are welcome. Feel free to fork the project and submit a pull request.
 
## 📄 License
 
This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and distribute it. Update this section if you'd prefer a different license.
 

