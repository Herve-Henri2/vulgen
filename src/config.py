import json
import os
import platform

configuration = {}
config_file = "config.json"

# Config variables

variables_list = ['operating_system', 'docker_desktop', 'main_window_background_color', 'main_window_textbox_color',
                  'main_window_buttons_color', 'options_window_background_color','text_color', 'text_font', 'text_size']

configuration['operating_system'] = platform.system()
configuration['docker_desktop'] = ""
# Default graphical variables
configuration['main_window_background_color'] = '#202266'
configuration['main_window_textbox_color'] = '#3D3F6E'
configuration['main_window_buttons_color'] = '#5D63A6'
configuration['options_window_background_color'] = '#282A69'
configuration['text_color'] = '#FFFFFF'
configuration['text_font'] = 'Consolas'
configuration['text_size'] = '12'

# Config methods

def CheckForMissingFields(func):
    '''
    Decorating function that will automatically add the new configuration fields you implemented in the code.
    '''
    global configuration
    
    def wrapper(*args, **kwargs):
        config_json = func(*args, **kwargs)
        for variable in variables_list:
            if variable not in config_json:
                config_json[variable] = configuration[variable]
                Save(variable, configuration[variable])
        return config_json
    return wrapper

# Load and Save the configuration
@CheckForMissingFields
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
        config = json.load(file)
        return config

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

def Reset():
    '''
    Wipes the current configuration file to write a new default one.
    '''
    with open(config_file, 'w') as file:
            file.write(json.dumps(configuration))



            
