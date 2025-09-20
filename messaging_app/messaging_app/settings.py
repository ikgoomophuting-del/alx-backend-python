django-admin startproject messaging_app
cd messaging_app

pip install djangorestframework

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    INSTALLED_APPS = [
    ...
    'rest_framework',
    'chats',
]


    # Third-party
    'rest_framework',

    # Local apps
    'chats',
]
