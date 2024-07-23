import os, json, sys

src_path = sys.path[0]

def get_settings():
    file = os.path.realpath("src/assets/settings.json")
    file = open(file, "r")
    contents = json.loads(file.read())
    file.close()
    return contents

def update_settings(updated_content):
    file = os.path.realpath("src/assets/settings.json")
    file = open(file, "r+")
    file.seek(0)
    json.dump(updated_content, file, indent=4)
    file.truncate()
    file.close()