def writer(content, filename, mode="r"):
    with open(filename, mode) as file:
        file.write(content)

