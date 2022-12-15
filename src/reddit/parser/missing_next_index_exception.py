class MissingNextIndexException(Exception):
    def __str__(self):
        return "Next index must not be an empty or none value"

