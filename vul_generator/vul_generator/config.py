import json
import os
import platform

configuration = {}
config_file = "config.json"

# Config variables
configuration['operating_system'] = platform.system()
configuration['docker_desktop'] = ""

# Load and Save the configuration
def Load():

    global configuration
    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            file.write(json.dumps(configuration))

    with open(config_file, 'r') as file:
        configuration = json.load(file)
        return configuration

def Save(config_name, config_value):
    # TODO -> handle the config value
    configuration[config_name] = config_value
    with open(config_file, 'w') as file:
        file.write(json.dumps(configuration))