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
    '''
    Returns the content of the configuration file (dictionnary json format)
    '''
    global configuration

    # If there is no config.json file, we write it
    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            file.write(json.dumps(configuration))

    with open(config_file, 'r') as file:
        configuration = json.load(file)
        return configuration

def Save(config_name, config_value):
    '''
    Saves a specific parameter into the configuration.
    ---------------
    Parameters:

    config_name: str
    The configuration parameter to write (example: operating_system)

    config_value: any
    The value of the given parameter (example: Linux)
    '''
    # TODO -> handle the config value
    configuration[config_name] = config_value
    with open(config_file, 'w') as file:
        file.write(json.dumps(configuration))