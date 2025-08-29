import os
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv()

# Base directory
basedir = Path(__file__).parent

class Config:
    # Admin SQLite Database Configuration
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir / "instance" / "admin_data.db"}'
    
    # MySQL Admin Configuration (for client operations) — read only from .env
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_ADMIN_USER = os.getenv('MYSQL_ADMIN_USER')
    MYSQL_ADMIN_PASSWORD = os.getenv('MYSQL_ADMIN_PASSWORD')
    
    MYSQL_CLIENT_URI = (
        f"mysql+pymysql://{MYSQL_ADMIN_USER}:{MYSQL_ADMIN_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/"
    )
    
    SQLALCHEMY_BINDS = {
        'admin': SQLALCHEMY_DATABASE_URI,
        'client': MYSQL_CLIENT_URI
    }
    
    # File Storage Configuration
    REPORT_FOLDER = str(basedir / 'reports')
    UPLOAD_FOLDER = str(basedir / 'Uploads')
    ENTERPRISE_FOLDER = str(basedir / 'Uploads' / 'enterprises')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # PostgreSQL Configuration
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_ADMIN_USER = os.getenv('POSTGRES_ADMIN_USER')
    POSTGRES_ADMIN_PASSWORD = os.getenv('POSTGRES_ADMIN_PASSWORD')
    POSTGRES_URI = (
        f"postgresql://{POSTGRES_ADMIN_USER}:{POSTGRES_ADMIN_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}"
    )
    
    # SQL Server Configuration
    SQLSERVER_HOST = os.getenv('SQLSERVER_HOST')
    SQLSERVER_INSTANCE = os.getenv('SQLSERVER_INSTANCE', '')
    SQLSERVER_PORT = os.getenv('SQLSERVER_PORT', '1433')
    SQLSERVER_ADMIN_USER = os.getenv('SQLSERVER_ADMIN_USER')
    SQLSERVER_ADMIN_PASSWORD = os.getenv('SQLSERVER_ADMIN_PASSWORD')
    
    if SQLSERVER_INSTANCE:
        SQLSERVER_URI = (
            f"mssql+pyodbc://{SQLSERVER_ADMIN_USER}:{SQLSERVER_ADMIN_PASSWORD}@"
            f"{SQLSERVER_HOST}\\{SQLSERVER_INSTANCE}?driver=ODBC+Driver+17+for+SQL+Server"
        )
    else:
        SQLSERVER_URI = (
            f"mssql+pyodbc://{SQLSERVER_ADMIN_USER}:{SQLSERVER_ADMIN_PASSWORD}@"
            f"{SQLSERVER_HOST}:{SQLSERVER_PORT}?driver=ODBC+Driver+17+for+SQL+Server"
        )
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_API_VERSION_GPT_4 = os.getenv("AZURE_API_VERSION_GPT_4")
    AZURE_OPENAI_GPT_4_TURBO_MODEL = os.getenv("AZURE_OPENAI_GPT_4_TURBO_MODEL")
    AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

    @staticmethod
    def init_app(app):
        """Initialize app-specific configurations and ensure directories exist."""
        for folder in [app.config['REPORT_FOLDER'], 
                      app.config['UPLOAD_FOLDER'],
                      app.config['ENTERPRISE_FOLDER']]:
            os.makedirs(folder, exist_ok=True)

        # Load DB configs dynamically from JSON files if needed
        for db_type in ['mysql', 'postgres', 'sqlserver']:
            config_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{db_type}_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    for key, value in config.items():
                        app.config[f"{db_type.upper()}_{key.upper()}"] = value
