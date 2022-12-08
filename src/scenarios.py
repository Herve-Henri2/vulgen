import platform
import os
import shutil # for recursive removal of folder
import json
from application import *


# This file is used to work around the scenarios database declared as scenario_db in the file application.py
# The representation we have choosen for the project is the following :
#   scenarios_db is a dictionnary with strings as keys
#       -> key 'total' : int
#       -> key 'scenarios_names' : list of strings
#       -> key 'total_types' : int
#       -> key 'types' : list of strings
#       -> key 'scenarios' : dictionnary that associates a string (name of the scenario) with a Scenario object


# Defining the main paths
scenarios_folder_path = os.path.realpath(os.path.dirname(__file__)) + f"{sep}..{sep}Scenarios"
global_json_path = scenarios_folder_path + f"{sep}scenarios.json"


# region =====Container Class=====

class Container:
    def __init__(self, image_name="", dockerfile="", is_main=False, requires_it=False, networks : list[str] = [], ports : dict[str,str] = {}, operating_system=""):
        self.image_name = image_name
        self.dockerfile = dockerfile
        self.is_main = is_main
        self.requires_it = requires_it
        self.networks = networks
        self.ports = ports
        self.operating_system = operating_system
    
    def __str__(self):
        return self.__dict__

# endregion

# region =====Scenario Class=====

class Scenario:
    
    # /!\ Whenever you add a new field to the scenario object, make sure you update all the fields in __init__, __str__, CreateDefault() and Parse()
    def __init__(self, name="", CVE="", difficulty="", type="", sources : list[str] = [], description="", goal="", solution="", containers : dict[str, Container] = {}):
        self.name = name
        self.CVE = CVE
        self.difficulty = difficulty # /5, 5/5 being the most difficult
        self.type = type
        self.sources = sources
        self.description = description
        self.goal = goal
        self.solution = solution
        self.containers = containers

    def __str__(self):
        return self.__dict__

# endregion


def Load() -> dict:
    '''
    Returns the scenarios database as a python dictionnary.
    '''
    if not os.path.exists(scenarios_folder_path):
        os.mkdir(scenarios_folder_path)
    if not os.path.exists(global_json_path):
        with open(global_json_path, 'w') as file:
            default_global_scenario_data = {"total":0, "scenarios_names":[], "total_types":0, "types":[], "avg_difficulty":0.0}
            file.write(json.dumps(default_global_scenario_data, indent=3))
    
    # We first instantiate our database dictionnary and parse into it our scenarios.json file
    scenarios_db = dict()    
    with open(global_json_path, 'r') as file:
        scenarios_db = json.load(file)
    scenarios_db['scenarios'] = dict[str, Scenario]()
    
    to_exclude = ['scenarios.json']
    scenarios_list = [folder for folder in os.listdir(scenarios_folder_path) if folder not in to_exclude]
    # We then complete our variable with all the existing scenarios
    for scenario_name in scenarios_list:
        folder_path = scenarios_folder_path + f"{sep}{scenario_name}"
        retrieveScenarioDataFromFolder(folder_path, scenarios_db)
    
    return scenarios_db

def retrieveScenarioDataFromFolder(folder_path : str, scenarios_db : dict):
    '''
    Instantiate a scenario in the database from the data in the specified folder
    '''
    json_path = folder_path + f"{sep}scenario_data.json"
    readme_path = folder_path + f"{sep}README.md"
    
    
    scenario_json_data = dict()
    try:
        with open(json_path, 'r') as file:
            scenario_json_data = json.load(file)
    except Exception as ex:
        logger.error(f'Error while trying to retrieve the scenario data from {folder_path}: {ex}')
        
    scenarios_db['scenarios'][scenario_json_data['name']] = Parse(scenario_json_data, readme_path)


def Save(scenario : Scenario):
    '''
    Saves the data from a given Scenario object into the scenarios folder, updating all that is necessary.
    '''
    scenarios_db = Load()
    scenarios_db['scenarios'][scenario.name] = scenario
    
    # Update global scenarios.json
    scenarios_db['total'] = len(scenarios_db['scenarios'])
    scenarios_db['scenarios_names'] = list(scenarios_db['scenarios'].keys())
    scenarios_db['types'] = list(GetAllTypes(scenarios_db))
    scenarios_db['total_types'] = len(scenarios_db['types'])
    scenarios_db['avg_difficulty'] = GetAverageDifficulty(scenarios_db)
    with open(global_json_path, 'w') as file:
        global_scenarios_data = {k:v for k,v in scenarios_db.items() if k != 'scenarios'}
        file.write(json.dumps(global_scenarios_data, indent=3))
    
    # Update specific scenario data
    scenario_folder_path = scenarios_folder_path + f"{sep}{scenario.name}"
    if not os.path.exists(scenario_folder_path):
        os.mkdir(scenario_folder_path)        
    
    json_path = scenario_folder_path + f"{sep}scenario_data.json"
    with open(json_path, 'w') as file:
        scenario_data = dict()        
        to_exclude = ["description", "goal", "solution"]
        for attribute_name in scenario.__dict__:
            if attribute_name not in to_exclude:
                if getattr(scenario, attribute_name) == "":
                    setattr(scenario, attribute_name, "N/A")
                scenario_data[attribute_name] = getattr(scenario, attribute_name)
                
        containers = [container.__dict__ for container in scenario.containers.values()]
        for container in containers:
            for key in container:
                if container[key] == "":
                    container[key] = "N/A"
        scenario_data["containers"] = containers
        
        file.write(json.dumps(scenario_data, indent=3))
    
    readme_path = scenario_folder_path + f"{sep}README.md"
    with open(readme_path, 'w') as file:
        content = generateReadmeContent(scenario)
        file.write(content)

def GetAllTypes(scenario_db : dict) -> set[str]:
    '''
    Return all distinct types currently in the scenarios database
    '''
    types = set[str]()
    for scenario in scenario_db['scenarios'].values():
        types.add(scenario.type)
    if "" in types:
        types.remove("")
    return types

def GetAverageDifficulty(scenarios_db : dict) -> float:
    '''
    Returns the average difficulty level of all the scenarios
    '''
    result = 0
    s_number = 0
    for scenario in scenarios_db['scenarios'].values():        
        if len(scenario.difficulty) != 0:
            s_number += 1
            result += int(scenario.difficulty)
    result = float(result/s_number)
    return result


def generateReadmeContent(scenario : Scenario) -> str:
    '''
    Returns a string formated like a scenario README.md file
    '''
    content = ""
    # Description
    content += encaseInBalise("Description", "h2") + '\n'
    for desc in scenario.description.split('\n'):
        content += encaseInBalise(desc, "p") + '\n'
    # Goal
    content += '\n' + encaseInBalise("Goal", "h2") + '\n'
    for goal in scenario.goal.split('\n'):
        content += encaseInBalise(goal, "p") + '\n'
    # Solution
    content += '\n' + encaseInBalise("Solution", "h2") + '\n'
    content += "<details>" + '\n'
    content += "    " + encaseInBalise("Spoilers! (click to expand)", "summary") + '\n'
    for sol in scenario.solution.split('\n'):
        content += "    " + encaseInBalise(sol, "p") + '\n'
    content += "</details>" + '\n'
    
    return content
    

def encaseInBalise(text : str, balise :str) -> str:
    '''
    Returns a string formated in the following way: <balise>text</balise>
    '''
    return f"<{balise}>{text}</{balise}>"


def Remove(scenario_name : str):
    '''
    Removes the folder associated with the specified scenario.
    '''
    scenario_folder_path = scenarios_folder_path + f"{sep}{scenario_name}"
    try:
        logger.info(f'Removing the scenario: {scenario_name}')
        shutil.rmtree(scenario_folder_path)
    except Exception as ex:
        logger.error(f'Error while trying to remove the scenario {scenario_name}: {ex}')


def LoadScenario(name : str) -> Scenario:
    '''
    Returns the Scenario object asociated with the given name 
    '''
    scenarios_db = Load()
    return scenarios_db['scenarios'][name]


def Parse(scenario_json_data : dict, readme_path = "") -> Scenario:
    '''
    Instantiates a Scenario object from a given scenario dictionnary.
    ---------------
    Parameters:

    scenario_json_data: The dictionnary we are going to read to instantiate the scenario
    readme_path: Path of the README.md file in order to recover description, goal and solution data
    '''
    for key in scenario_json_data:
        if scenario_json_data[key] == "N/A":
            scenario_json_data[key] = ""
    
    scenario = Scenario()    
    to_exclude = ["description", "goal", "solution", "containers"]
    for attribute_name in scenario.__dict__:
        if attribute_name not in to_exclude:
            try:
                setattr(scenario, attribute_name, scenario_json_data[attribute_name])
            except Exception as ex:
                logger.error(f'Error while parsing the scenario: {ex}')
    
    desc = ""; goal = ""; sol = ""
    if len(readme_path) != 0:
        desc, goal, sol = ParseReadme(readme_path)
        scenario.description = desc; scenario.goal = goal; scenario.solution = sol
    
    containers = dict[str,Container]()
    for container_data in scenario_json_data['containers']:
        for key in container_data:
            if container_data[key] == "N/A":
                container_data[key] = ""
        
        container = Container()
        for attribute_name in container.__dict__:
            try:
                setattr(container, attribute_name, container_data[attribute_name])
            except Exception as ex:
                logger.error(f'Error while parsing the container: {ex}')
        
        containers[container.image_name] = container
    scenario.containers = containers

    return scenario

def ParseReadme(readme_file_path : str) -> tuple[str, str, str]:
    '''
    Return a scenario description, goal and solution from a README.md file
    '''
    desc = ""; goal = ""; sol = ""
    
    try:
        readme = open(readme_file_path, 'r')
        buffer = readme.read()
        readme.close()
        
        h2split = buffer.split('<h2>')
        h2split.remove('')
        for index,split in enumerate(h2split):
            split_buffer = ""
            lastPIndex = 0
            noMoreParagraphs = False
            while not noMoreParagraphs:
                pStartIndex = split.find('<p>', lastPIndex)
                pEndIndex = split.find('</p>', lastPIndex)
                if pStartIndex == -1 or pEndIndex == -1:
                    noMoreParagraphs = True
                else:
                    split_buffer += split[pStartIndex + 3 : pEndIndex] + '\n'
                    lastPIndex = pEndIndex + 4
            
            if index == 0:
                desc += split_buffer[:-1]
            elif index == 1:
                goal += split_buffer[:-1]
            elif index == 2:
                sol += split_buffer[:-1]
            index += 1
    except Exception as ex:
        logger.error(f'An error occured while trying to parse {readme_file_path}: {ex}')
    
    return (desc, goal, sol)


if __name__ == "__main__":
    #test_saving_scenarios()
    #test_retrieving_scenario()
    scen = Load()
    print(json.dumps(scen, indent=3))