from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")
rm_host = os.getenv("RM_HOST")
rm_port = os.getenv("RM_PORT")
rm_user=os.getenv("RM_USER")
rm_password = os.getenv("RM_PASSWORD")
rm_db_user = os.getenv("DB_USER")
rm_db_password = os.getenv("DB_PASSWORD")
rm_db_host = os.getenv("DB_HOST")
rm_db_port = os.getenv("DB_PORT")
rm_db_name = os.getenv("DB_DATABASE")
