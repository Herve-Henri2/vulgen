import json
import platform
import logging

configuration = {}
config_file = "config.json"

#  region =====Config variables=====

variables_list = ['operating_system', 'docker_desktop', 'log_file', 'log_format', 'main_window_background_color', 'main_window_textbox_color',
                  'buttons_color', 'disabled_buttons_color', 'child_window_background_color','text_color', 'disabled_text_color', 'text_font', 'text_size']

configuration['operating_system'] = platform.system()
configuration['docker_desktop'] = ""
configuration['log_file'] = 'app.log'
configuration['log_format'] = "%(asctime)s | %(levelname)s - %(message)s"
# Default graphical variables
configuration['main_window_background_color'] = '#202266'
configuration['main_window_textbox_color'] = '#3D3F6E'
configuration['buttons_color'] = '#5D63A6'
configuration['disabled_buttons_color'] = "#7175A8"
configuration['child_window_background_color'] = '#282A69'
configuration['text_color'] = '#FFFFFF'
configuration['disabled_text_color'] = '#ADADAD'
configuration['text_font'] = 'Consolas'
configuration['text_size'] = '12'
#logger

logging.basicConfig(filename=configuration['log_file'], level=logging.INFO, format=configuration['log_format'])
logger = logging.getLogger()

# endregion

# region =====Config methods=====

def CheckForMissingFields(func):
    '''
    Decorating function that will automatically add the new configuration fields you implemented in the code.
    '''
    global configuration
    
    def wrapper(*args, **kwargs):
        config_json = func(*args, **kwargs)
        if config_json is not None:
            for variable in variables_list:
                if variable not in config_json:
                    config_json[variable] = configuration[variable]
                    Save(variable, configuration[variable])
        return config_json
    return wrapper

# Load and Save the configuration
@CheckForMissingFields
def Load() -> dict:
    '''
    Returns the content of the configuration file (dictionnary json format)
    '''
    try: 
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError as ex:
        logger.error(ex)
        Reset()
        return configuration
    except json.decoder.JSONDecodeError as ex: 
        logger.error(ex)
        Reset()
        return configuration

def Save(config_name : str, config_value):
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
    logger.info('Creating a new default configuration file')
    with open(config_file, 'w') as file:
            file.write(json.dumps(configuration))

# endregion
            
