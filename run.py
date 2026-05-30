#!/usr/bin/env python3
import subprocess
import sys
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    from dotenv import load_dotenv
    load_dotenv(".env")
    load_dotenv(".env.example")
    sys.exit(subprocess.call([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501"]))
