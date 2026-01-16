

python -m pip install -r requirements.txt

# Project Setup (Windows CMD)

This project uses Python dependencies listed in `requirements.txt`. Follow the steps below to install everything on **Windows using Command Prompt (CMD)**.

## Prerequisites
- **Python 3** installed (recommended: 3.10+)
- **pip** available (usually included with Python)

Verify your installation:
```bat
python --version
pip --version
```

## Installation (Windows CMD)

### 1) Open CMD in the project folder

1. Open File Explorer
2. Navigate to the folder that contains requirements.txt
3. Click the address bar, type cmd, and press Enter

Confirm you are in the correct folder:

```bat
dir
```

### 2) Create a virtual environment
```bat
python -m venv .venv
```

### 3) Activate the virtual environment
```bat
.venv\Scripts\activate
```
After activation, you should see (.venv) at the start of the command line.

### 4) Install dependencies from requirements.txt
```bat
pip install -r requirements.txt
```

### 5) Run the project
```bat
python src/main.py
```
