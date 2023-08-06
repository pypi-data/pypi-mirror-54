import os


def read(path_to_file):
    with open(path_to_file, 'r') as f:
        return f.read()


def write(content, path_to_file):
    # create all missing folders, including intermediate ones
    os.makedirs(os.path.dirname(path_to_file), exist_ok=True)

    with open(path_to_file, 'w') as f:
        f.write(content)
