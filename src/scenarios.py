import platform
import os
import json


scenarios = {}
sep = '/' if platform.system() == "Linux" else '\\'
scenarios_folder_path = src_folder_path = os.path.realpath(os.path.dirname(__file__)) + f"{sep}..{sep}scenarios"

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

    # TODO implement creating scenarios folder and/or file if they don't exist
    #if not os.path.exists(scenarios_file):
    #    with open(scenarios_file, 'w') as file:
    #        file.write(json.dumps(scenarios, indent=3))
    #    CreateDefault()
    
    _scenarios = dict()
    
    global_json_path = scenarios_folder_path + f"{sep}scenarios.json"
    with open(global_json_path, 'r') as file:
        _scenarios = json.load(file)
    _scenarios['scenarios'] = dict[str, Scenario]()
    
    to_exclude = ('scenarios.json', 'metasploitable2')
    scenarios_list = [folder for folder in os.listdir(scenarios_folder_path) if folder not in to_exclude]
    for scenario_name in scenarios_list:
        folder_path = scenarios_folder_path + f"{sep}{scenario_name}"
        retrieveScenarioDataFromFolder(folder_path, _scenarios)
    
    return _scenarios

def retrieveScenarioDataFromFolder(folder_path : str, scenarios_dict : dict):
    json_path = folder_path + f"{sep}scenario_data.json"
    readme_path = folder_path + f"{sep}README.md"
    
    _json = dict()
    with open(json_path, 'r') as file:
        _json = json.load(file)
    
    scenarios_dict['scenarios'][_json['name']] = Parse(_json, readme_path)


def Save(Scenario : Scenario):
    '''
    Saves a given Scenario object into the database file, updating all the necessary fields.
    '''
    scenarios = Load()    
    scenarios['scenarios'][Scenario.name] = Scenario
    
    # Update global scenarios.json
    scenarios['total'] = len(scenarios['scenarios'])
    scenarios['scenarios_names'] = list(scenarios['scenarios'].keys())
    scenarios['types'] = list(GetAllTypes(scenarios['scenarios']))
    scenarios['total_types'] = len(scenarios['types'])
    global_json_path = scenarios_folder_path + f"{sep}scenarios.json"
    with open(global_json_path, 'w') as file:
        global_scenarios_data = {k:v for k,v in scenarios.items() if k != 'scenarios'}
        file.write(json.dumps(global_scenarios_data, indent=3))
    
    # Update specific scenario data
    # TODO

def GetAllTypes(s_dict : dict[str, Scenario]):
    types = set()
    for scenario in s_dict.values():
        types.add(scenario.type)
    return types


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

def LoadScenario(name : str) -> Scenario:
    scenarios = Load()
    return scenarios['scenarios'][name]


def ParseReadme(readme_file_path : str):
    desc = ""; goal = ""; sol = ""
    
    readme = open(readme_file_path, 'r')
    buffer = readme.read()
    readme.close()
    
    h2split = buffer.split('<h2>')
    h2split.remove('')    
    index = 0
    for split in h2split:
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
            desc += split_buffer
        elif index == 1:
            goal += split_buffer
        elif index == 2:
            sol += split_buffer
        index += 1
    
    return (desc, goal, sol)


if __name__ == "__main__":
    #test_saving_scenarios()
    #test_retrieving_scenario()
    scen = Load()
    print(json.dumps(scen, indent=3))