import configparser


def read(filename):
    validate_filename(filename)
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def validate_filename(filename):
    if not filename:
        raise Exception
