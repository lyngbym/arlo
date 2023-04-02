from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
basestation = os.getenv('BASESTATION')
camera_1 = os.getenv('CAMERA_1')