# SecureSphere Installation Guide

## Requirements

- Python 3.9 or newer
- Git

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/Pranjal01819/SecureSphere.git
```

### 2. Enter the project directory

```powershell
cd SecureSphere
```

### 3. Install required dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run SecureSphere

```powershell
python Main.py
```

## Quick Installation

You can run these commands one by one:

```powershell
git clone https://github.com/Pranjal01819/SecureSphere.git
cd SecureSphere
python -m pip install -r requirements.txt
python Main.py
```

## Update SecureSphere

If you already cloned the repository:

```powershell
cd SecureSphere
git pull
python -m pip install -r requirements.txt
python Main.py
```

## Troubleshooting

Check your Python installation:

```powershell
python --version
```

Check pip:

```powershell
python -m pip --version
```

If `python` is not recognized, install Python and make sure **Add Python to PATH** is enabled during installation.
