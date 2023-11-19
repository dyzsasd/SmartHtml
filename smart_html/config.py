import os

from dotenv import load_dotenv


load_dotenv()

config = {
    "db": {
        "url": "mydatabase.db"
    },
    "engine": {
        "app_key": os.getenv('openai_key')
    }
}