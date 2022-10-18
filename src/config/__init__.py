import reader

FILENAME = 'feddit.ini'


def getconfig():
    config = reader.read(FILENAME)
    return dict(config['options'])

