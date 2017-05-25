"""
Django settings for my_blog project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/

更新日志:
2017.05.25 增加发送邮件的配置信息
2017.03.28 新增 code_collect 这个 APP 及相应的 logger 信息
2017.03.24 新增 toolhub 这个 app
2016.10.28 在更新时间的时候遇到了这么个问题:
    RuntimeWarning: DateTimeField Article.update_time received a naive datetime ... while time zone support is active
    搜索得到解决方案: https://my.oschina.net/lyroge/blog/76298, 把 settings.USE_TZ 设置为 False 即可
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xu)@fc2^=xyttqp-=strs4au0x(ik)%#q*8+hai+l3m1b=*b%_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 部署脚本会修改这个变量
DOMAIN = "localhost"

ALLOWED_HOSTS = [DOMAIN]

# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',  # 一定要放在`django.contrib.admin`前面
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "articles",
    "django_cron",
    "gitbook_notes",
    "work_journal",
    "just_eating",
    "toolhub",
    "code_collect",
    "common_module",
]

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "articles", 'templates'),)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'  # TODO: 放到服务器上的时候需要更改这一项, 原来的时区为 UTC

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "../static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            # 日志格式
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        },
        "info": {
            'format': '[**] %(asctime)s [%(levelname)s]- %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "../../log/django_default.log"),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种 formatter 日志格式
        },
        "info": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "../../log/django_info.log"),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'info',  # 使用哪种 formatter 日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "../../log/django_error.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "../../log/django_request.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'my_blog.articles.views': {
            'handlers': ['default', 'error', "info"],
            'level': 'DEBUG',
            'propagate': True
        },
        'my_blog.work_journal.views': {
            'handlers': ['default', 'error', "info"],
            'level': 'DEBUG',
            'propagate': True
        },
        'my_blog.gitbooks.views': {
            'handlers': ['default', 'error', "info"],
            'level': 'DEBUG',
            'propagate': True
        },
        'my_blog.just_eating.views': {
            'handlers': ['default', 'error', "info"],
            'level': 'DEBUG',
            'propagate': True
        },
        'my_blog.toolhub.views': {
            'handlers': ['default', 'error', "info"],
            'level': 'DEBUG',
            'propagate': True
        },
        'my_blog.code_collect.views': {
            'handlers': ['default', 'error', "info"],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
UPDATE_TIME_LIMIT = 30

CRON_CLASSES = [
    "django_cron.cron.AutoUpdateNotes",
]

# 测试用
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# 生产环境使用
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = '490772448@qq.com'
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'watch0.top <490772448@qq.com>'
