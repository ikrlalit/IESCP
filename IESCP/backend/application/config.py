DB="sqlite:///app_db.sqlite3"
Key = "sdkfjslkdjkAREDXC34df"
UPLOAD_FOLDER = "./static/"


class LocalConfig():
    from datetime import timedelta
    
    SQLALCHEMY_DATABASE_URI=DB
    UPLOAD_FOLDER = UPLOAD_FOLDER
    WTF_CSRF_ENABLED=False
    # CELERY_BROKER_URL = "redis://localhost:6379/0"
    # CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    JWT_SECRET_KEY='SDfasdwqerThf34sSSCRdSewqxXse'
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=5) 
    CACHE_TYPE= 'RedisCache'
    CACHE_REDIS_URL= 'redis://localhost:6379/3'
    CACHE_DEFAULT_TIMEOUT= 300
    CACHE_KEY_PREFIX='iescpcacheprefix'



