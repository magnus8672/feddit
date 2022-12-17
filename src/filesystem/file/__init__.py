import os


def writer(content, filename, mode="r"):
    with open(filename, mode) as file:
        file.write(content)


def delete(file):
    os.remove(file)

