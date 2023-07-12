# Reference
# https://github.com/CentOS/ansible-role-duffy/blob/master/defaults/main.yml

# The location of the database
database = ""

# The database URL schema using synchronous processing
jsyncurl = ""

# The database URL schema using asynchronous processing
asyncurl = ""

# The port on which the database service is hosted
dtbsport = "5432"

# The username for the database user
username = ""

# The password for the database user
password = ""

# The location of serving the application service
servhost = "0.0.0.0"

# The port on which the application service is hosted
servport = 8080

# Automatically reload if the code is changed
cgreload = True

# The default configuration for service logging
logrconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[FPBS] %(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}

# The default configuration for WSGI logging

wsgiconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[FPBS] %(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "[FPBS] %(asctime)s [%(levelname)s] %(client_addr)s - '%(request_line)s' %(status_code)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
