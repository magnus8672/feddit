from config.reader import read

FILENAME = 'feddit.ini'


def get_config():
    config = read(FILENAME)
    return dict(config['options'])

