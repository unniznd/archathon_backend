import os

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'myFirstDatabase',
        'CLIENT': {
            'host': os.environ.get("HOST")
        }  
    }
}

