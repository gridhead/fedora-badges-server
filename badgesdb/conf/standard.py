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

# The default configuration for service logging
logrconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[FBDB] %(asctime)s [%(levelname)s] %(message)s",
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
