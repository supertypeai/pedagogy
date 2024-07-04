import os
import sqlalchemy as sa

secretkey = os.environ.get('SECRET_KEY')
# database configuration
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT', '5432')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DATABASE')
dbendpoint = os.getenv('DB_ENDPOINT')

options = '-c search_path=dbo,pedagogy'
if dbendpoint is not None:
    options = options + f' endpoint={dbendpoint}'

dburl = sa.engine.URL.create(
    drivername='postgresql+psycopg',
    username=user,
    password=password,
    host=host,
    port=int(port),
    database=database,
    query={
        'sslmode': 'require',
        'options': options
    }
)

engine = sa.create_engine(dburl)

adminsemail = os.getenv('ADMINS_EMAIL').split(';')

# create the configuration class
class Config():
    SECRET_KEY = secretkey or 'l3arn2t3ach'
    SQLALCHEMY_DATABASE_URI = dburl
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    # 'mysql+pymysql://Samuel:tirab33@localhost/assistants'
    FLASK_DEBUG = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    # mail server configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = adminsemail
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 86400 # 24 hours = 86400

