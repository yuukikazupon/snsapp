import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'q8ncy_!bq(@#he8v$bj2lk=@xya7juivc)wba!trp649^2(8w$'

ATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'keijiban',
        'USER':'',
        'PASSWORD':'',
        'HOST':'',
        'PORT':''
    }
}

DEBUG = True
