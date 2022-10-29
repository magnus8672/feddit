from config.reader import read

FILENAME = 'feddit.ini'


def getconfig():
    config = read(FILENAME)
    return dict(config['options'])

