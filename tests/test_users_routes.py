from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
uri = os.getenv("MONGODB_URI")