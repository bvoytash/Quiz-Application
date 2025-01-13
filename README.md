# Quiz-App

Django Framework Project
# Live at: https://quiz-application-u54x.onrender.com

# Steps to Clone and Run the Project

## Requirements
- **Python 3.10**: [Download Python 3.10](https://www.python.org/downloads/release/python-3100/)


## 1. Clone the Repository and Navigate to the Folder
```
git clone https://github.com/bvoytash/Quiz-Application.git && cd ./Quiz-Application/
```

## 2. Create a Virtual Environment
- **Linux and macOS**:
    ```
    python3 -m venv .venv
    ```
- **Windows**:
    ```
    python -m venv .venv
    ```

## 3. Activate the Virtual Environment
**Assuming you are using Bash:**
- **Linux and macOS**:
    ```
    source .venv/bin/activate
    ```
- **Windows**:
    ```
    source .venv/Scripts/activate
    ```

## 4. Install Dependencies
```
pip install -r requirements.txt
```

## 5. Migrate to do a tables
```
python manage.py migrate
```

## 6. Run Server
```
python manage.py runserver
```
