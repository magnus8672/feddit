class MissingFilenameException(Exception):
    def __str__(self):
        return "You must indicate an existing config filename"

