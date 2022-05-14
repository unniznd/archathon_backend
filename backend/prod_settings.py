import os

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ['archathonbackendserver.herokuapp.com']


DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'myFirstDatabase',
        'CLIENT': {
            'host': os.environ.get("HOST")
        }  
    }
}

