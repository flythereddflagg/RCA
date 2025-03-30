import configparser

test_file_path = "./assets/test.conf"

with open(test_file_path) as f:
    text = f.read()
    config = configparser.ConfigParser()
    print(text)

print("conf1: ", config.read(test_file_path))
print("conf2: ", {s:dict(config.items(s)) for s in config.sections()})
print("conf3: ", config._sections)