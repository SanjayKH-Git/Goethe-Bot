## Goethe-Bot

The Goethe Simulator is a Python-based project that utilizes Playwright for web automation and testing. 
This README provides instructions for setting up the project and activating the virtual environment.

**Requirements**

* Python 3.x (https://www.python.org/downloads/)
* Playwright (https://playwright.dev/)

clone the repository to your local machine:
```
git clone https://github.com/SanjayKH-Git/Goethe-Bot 
cd Goethe-Bot  # Change to the repository directory
```

**Create a Virtual Environment (Recommended)**

A virtual environment isolates project dependencies from your system-wide Python installation. Here's how to create one using `venv`:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows
```

**Installing Plawright**
```bash
pip install playwright
playwright install
```

**Running Script**
```bash
python goethe_bot.py
```

**> Keep the CSV File in same folder**

**> Input the proper CSV File Name or File path**

