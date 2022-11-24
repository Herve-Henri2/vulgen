import platform
import os
import json


scenarios = {}
sep = '/' if platform.system() == "Linux" else '\\'
scenarios_folder_path = src_folder_path = os.path.realpath(os.path.dirname(__file__)) + f"{sep}..{sep}scenarios"
global_json_path = scenarios_folder_path + f"{sep}scenarios.json"

# A few default variables
scenarios['total'] = 0
scenarios['scenarios_names'] = list()
scenarios['scenarios'] = dict()
scenarios['total_types'] = 0
scenarios['types'] = list()

# region =====Scenario Class=====

class Scenario:
    
    # /!\ Whenever you add a new field to the scenario object, make sure you update all the fields in __init__, __str__, CreateDefault() and Parse()
    def __init__(self, name=None, description=None, goal=None, solution=None, images=None, CVE=None, difficulty=None, type=None, sources=None):
        self.name = name
        self.description = description
        self.goal = goal
        self.solution = solution
        self.images = images
        self.cve = CVE
        self.difficulty = difficulty # /5, 5/5 being the most difficult
        self.type = type
        self.sources = sources

    def __str__(self):
        scenario = {}
        scenario['name'] = self.name
        scenario['description'] = self.description
        scenario['goal'] = self.goal
        scenario['solution'] = self.solution
        scenario['images'] = self.images
        scenario['CVE'] = self.cve
        scenario['difficulty'] = self.difficulty
        scenario['type'] = self.type
        scenario['sources'] = self.sources
        return scenario

# endregion
    

def Load() -> dict:
    '''
    Returns the scenarios database as a python dictionnary.
    '''
    global scenarios

    if not os.path.exists(scenarios_folder_path):
        os.mkdir(scenarios_folder_path)
    if not os.path.exists(global_json_path):
        with open(global_json_path, 'w') as file:
            default_global_scenario_data = {"total":0, "scenarios_names":[], "total_types":0, "types":[]}
            file.write(json.dumps(default_global_scenario_data, indent=3))
    
    
    _scenarios = dict()    
    with open(global_json_path, 'r') as file:
        _scenarios = json.load(file)
    _scenarios['scenarios'] = dict[str, Scenario]()
    
    to_exclude = ['scenarios.json']
    scenarios_list = [folder for folder in os.listdir(scenarios_folder_path) if folder not in to_exclude]
    for scenario_name in scenarios_list:
        folder_path = scenarios_folder_path + f"{sep}{scenario_name}"
        retrieveScenarioDataFromFolder(folder_path, _scenarios)
    
    return _scenarios

def retrieveScenarioDataFromFolder(folder_path : str, scenarios_dict : dict):
    '''
    Instantiate a scenario in the database from the data in the specified folder
    '''
    json_path = folder_path + f"{sep}scenario_data.json"
    readme_path = folder_path + f"{sep}README.md"
    
    _json = dict()
    with open(json_path, 'r') as file:
        _json = json.load(file)
    
    scenarios_dict['scenarios'][_json['name']] = Parse(_json, readme_path)


def Save(scenario : Scenario):
    '''
    Saves a given Scenario object into the database file, updating all the necessary fields.
    '''
    scenarios = Load()    
    scenarios['scenarios'][scenario.name] = scenario
    
    # Update global scenarios.json
    scenarios['total'] = len(scenarios['scenarios'])
    scenarios['scenarios_names'] = list(scenarios['scenarios'].keys())
    scenarios['types'] = list(GetAllTypes(scenarios['scenarios']))
    scenarios['total_types'] = len(scenarios['types'])
    with open(global_json_path, 'w') as file:
        global_scenarios_data = {k:v for k,v in scenarios.items() if k != 'scenarios'}
        file.write(json.dumps(global_scenarios_data, indent=3))
    
    # Update specific scenario data
    scenario_folder_path = scenarios_folder_path + f"{sep}{scenario.name}"
    if not os.path.exists(scenario_folder_path):
        os.mkdir(scenario_folder_path)        
    
    json_path = scenario_folder_path + f"{sep}scenario_data.json"
    with open(json_path, 'w') as file:
        scenario_data = {"name":scenario.name, "images":scenario.images, "CVE":scenario.cve, "difficulty":scenario.difficulty, "type":scenario.type, "sources":scenario.sources}
        file.write(json.dumps(scenario_data, indent=3))
    
    readme_path = scenario_folder_path + f"{sep}README.md"
    with open(readme_path, 'w') as file:
        content = generateReadmeContent(scenario)
        file.write(content)    

def GetAllTypes(s_dict : dict[str, Scenario]):
    '''
    Return all distinct types currently in the scenarios database
    '''
    types = set()
    for scenario in s_dict.values():
        types.add(scenario.type)
    return types

def generateReadmeContent(scenario : Scenario):
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
    

def encaseInBalise(text : str, balise :str):
    return f"<{balise}>{text}</{balise}>"

def LoadScenario(name : str) -> Scenario:
    '''
    Returns the Scenario object asociated with the given name 
    '''
    scenarios = Load()
    return scenarios['scenarios'][name]

def Parse(_json : dict, readme_path = "") -> Scenario:
    '''
    Instantiates a Scenario object from a json string.
    ---------------
    Parameters:

    _json: The dictionnary we are going to read to instantiate the scenario.
    '''
    name = _json['name']
    images = _json['images']
    cve = _json['CVE']
    diff = _json['difficulty']
    type = _json['type']
    sources = _json['sources']
    
    desc = ""; goal = ""; sol = ""
    if readme_path != "":
        desc, goal, sol = ParseReadme(readme_path)

    scen = Scenario(name, desc, goal, sol, images, cve, diff, type, sources)
    return scen

def ParseReadme(readme_file_path : str):
    '''
    Return a scenario description, goal and solution from a README.md file
    '''
    desc = ""; goal = ""; sol = ""
    
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
    
    return (desc, goal, sol)


if __name__ == "__main__":
    #test_saving_scenarios()
    #test_retrieving_scenario()
    scen = Load()
    print(json.dumps(scen, indent=3))