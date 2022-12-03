import json
import platform
import logging

configuration = {}
config_file = "config.json"

#  region =====Config variables=====

variables_list = ['operating_system', 'docker_desktop', 'log_file', 'log_format', 'current_mode_index', 'modes', 'current_theme_index', 'themes']

configuration['operating_system'] = platform.system()
configuration['docker_desktop'] = ""
configuration['log_file'] = 'app.log'
configuration['log_format'] = "%(asctime)s | %(levelname)s - %(message)s"

# Education or challenge mode
configuration['current_mode_index'] = 0
configuration['modes'] = ['Education', 'Challenge']

# UI Themes
configuration['current_theme_index'] = 0 # Default theme
configuration['themes'] = []
theme1, theme2, theme3, theme4, theme5 = {}, {}, {}, {}, {}

# Default Theme
theme1['name'] = 'Default'
theme1['main_window_background_color'] = '#202266'
theme1['main_window_textbox_color'] = '#3D3F6E'
theme1['buttons_color'] = '#5D63A6'
theme1['disabled_buttons_color'] = '#7175A8'
theme1['child_window_background_color'] = '#282A69'
theme1['border_color'] = "#FFFFFF"
theme1['text_color'] = '#FFFFFF'
theme1['disabled_text_color'] = '#ADADAD'
theme1['text_font'] = 'Walbaum Display'
theme1['text_size'] = '12'
configuration['themes'].append(theme1)

# Dracula Theme
theme2['name'] = 'Dracula'
theme2['main_window_background_color'] = '#171515'
theme2['main_window_textbox_color'] = '#050505'
theme2['buttons_color'] = '#171010'
theme2['disabled_buttons_color'] = '#382626'
theme2['child_window_background_color'] = '#1F1D1D'
theme2['border_color'] = "#CF0000"
theme2['text_color'] = '#CF0000'
theme2['disabled_text_color'] = '#CF4A4A'
theme2['text_font'] = 'Walbaum Display'
theme2['text_size'] = '12'
configuration['themes'].append(theme2)

# Midnight Theme
theme3['name'] = 'Midnight'
theme3['main_window_background_color'] = '#000000'
theme3['main_window_textbox_color'] = '#000000'
theme3['buttons_color'] = '#040D36'
theme3['disabled_buttons_color'] = '#2E2F50'
theme3['child_window_background_color'] = '#01040F'
theme3['border_color'] = "#3F42D0"
theme3['text_color'] = '#3F42D0'
theme3['disabled_text_color'] = '#7779CF'
theme3['text_font'] = 'Walbaum Display'
theme3['text_size'] = '12'
configuration['themes'].append(theme3)

# Blinding light theme
theme4['name'] = 'Blinding Light'
theme4['main_window_background_color'] = '#FFFFFF'
theme4['main_window_textbox_color'] = '#FFFFFF'
theme4['buttons_color'] = '#F8EA46'
theme4['disabled_buttons_color'] = '#FDF69D'
theme4['child_window_background_color'] = '#FFFFFF'
theme4['border_color'] = "#F0D121"
theme4['text_color'] = '#DFBE04'
theme4['disabled_text_color'] = '#D5C463'
theme4['text_font'] = 'Walbaum Display'
theme4['text_size'] = '12'
configuration['themes'].append(theme4)

# Alien theme
theme5['name'] = 'Alien'
theme5['main_window_background_color'] = '#2B4C18'
theme5['main_window_textbox_color'] = '#000000'
theme5['buttons_color'] = '#293721'
theme5['disabled_buttons_color'] = '#708E60'
theme5['child_window_background_color'] = '#2B4C18'
theme5['border_color'] = "#5CFA03"
theme5['text_color'] = '#5CFA03'
theme5['disabled_text_color'] = '#BEFE9A'
theme5['text_font'] = 'Walbaum Display'
theme5['text_size'] = '12'
configuration['themes'].append(theme5)

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
    # TODO -> handle the config_value variable
    configuration = Load()
    configuration[config_name] = config_value
    try:
        with open(config_file, 'w') as file:
            file.write(json.dumps(configuration, indent=3))
            logger.info(f'Saved {config_value} into {config_name}.')
    except Exception as ex:
        logger.error(f'An error occured when attempting to open the file {config_file}: {ex}')

def Reset():
    '''
    Wipes the current configuration file to write a new default one.
    '''
    logger.info('Creating a new default configuration file')
    with open(config_file, 'w') as file:
            file.write(json.dumps(configuration, indent=3))


def GetTheme(configuration=None) -> dict:
    '''
    Returns the current theme of our application as a dictionnary.
    '''
    if configuration is None:
        configuration = Load()
    return configuration['themes'][configuration['current_theme_index']]


# endregion
            
if __name__ == "__main__":
    conf = Load()