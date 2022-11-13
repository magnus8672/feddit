import os

from filesystem.file import delete


def files(route):
    return os.listdir(route)


def clean(route):
    for file in files(route):
        file_route = route + file
        delete(file_route)
