import io


def fake_file(content):
    return io.StringIO(content)


def fake_ini_file(content=""):
    section_name = 'options'
    fake_section = f"[{section_name}]\n{content}"
    return fake_file(fake_section)

