import platform
import os
import json


# This file is used to work around the scenarios database declared as scenario_db in the file application.py
# The representation we have choosen for the project is the following :
#   scenarios_db is a dictionnary with strings as keys
#       -> key 'total' : int
#       -> key 'scenarios_names' : list of strings
#       -> key 'total_types' : int
#       -> key 'types' : list of strings
#       -> key 'scenarios' : dictionnary that associates a string (name of the scenario) with a Scenario object


# Defining the main paths
sep = '/' if platform.system() == "Linux" else '\\'
scenarios_folder_path = src_folder_path = os.path.realpath(os.path.dirname(__file__)) + f"{sep}..{sep}scenarios"
global_json_path = scenarios_folder_path + f"{sep}scenarios.json"


# region =====Image Class=====

class Image:
    def __init__(self, name="", dockerfile="", is_main=False, ports : dict[str,str] = {}, os=""):
        self.name = name
        self.dockerfile = dockerfile
        self.is_main = is_main
        self.ports = ports
        self.os = os
    
    def toDict(self):
        return {"name": self.name, "dockerfile": self.dockerfile, "is_main": self.is_main, "ports": self.ports, "operating_system": self.os}
    
    def __str__(self):
        image = {}
        image['name'] = self.name
        image['dockerfile'] = self.dockerfile
        image['is_main'] = self.is_main
        image['ports'] = self.ports
        image['os'] = self.os
        return image

# endregion

# region =====Scenario Class=====

class Scenario:
    
    # /!\ Whenever you add a new field to the scenario object, make sure you update all the fields in __init__, __str__, CreateDefault() and Parse()
    def __init__(self, name="", CVE="", difficulty="", type="", sources : list[str] = [], description="", goal="", solution="", images : dict[str, Image] = {}):
        self.name = name
        self.cve = CVE
        self.difficulty = difficulty # /5, 5/5 being the most difficult
        self.type = type
        self.sources = sources
        self.description = description
        self.goal = goal
        self.solution = solution
        self.images = images

    def __str__(self):
        scenario = {}
        scenario['name'] = self.name
        scenario['CVE'] = self.cve
        scenario['difficulty'] = self.difficulty
        scenario['type'] = self.type
        scenario['sources'] = self.sources
        scenario['description'] = self.description
        scenario['goal'] = self.goal
        scenario['solution'] = self.solution
        scenario['images'] = self.images
        return scenario

# endregion


def Load() -> dict:
    '''
    Returns the scenarios database as a python dictionnary.
    '''
    if not os.path.exists(scenarios_folder_path):
        os.mkdir(scenarios_folder_path)
    if not os.path.exists(global_json_path):
        with open(global_json_path, 'w') as file:
            default_global_scenario_data = {"total":0, "scenarios_names":[], "total_types":0, "types":[]}
            file.write(json.dumps(default_global_scenario_data, indent=3))
    
    
    scenarios_db = dict()    
    with open(global_json_path, 'r') as file:
        scenarios_db = json.load(file)
    scenarios_db['scenarios'] = dict[str, Scenario]()
    
    to_exclude = ['scenarios.json']
    scenarios_list = [folder for folder in os.listdir(scenarios_folder_path) if folder not in to_exclude]
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
    with open(json_path, 'r') as file:
        scenario_json_data = json.load(file)
    
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
    with open(global_json_path, 'w') as file:
        global_scenarios_data = {k:v for k,v in scenarios_db.items() if k != 'scenarios'}
        file.write(json.dumps(global_scenarios_data, indent=3))
    
    # Update specific scenario data
    scenario_folder_path = scenarios_folder_path + f"{sep}{scenario.name}"
    if not os.path.exists(scenario_folder_path):
        os.mkdir(scenario_folder_path)        
    
    json_path = scenario_folder_path + f"{sep}scenario_data.json"
    with open(json_path, 'w') as file:
        to_exclude = ["description", "goal", "solution"]
        for attribute_name in scenario.__dict__:
            if attribute_name not in to_exclude and getattr(scenario, attribute_name) == "":
                setattr(scenario, attribute_name, "N/A")
                
        images = [image.toDict() for image in scenario.images.values()]
        for image in images:
            for key in image:
                if image[key] == "":
                    image[key] = "N/A"
        
        scenario_data = {"name":scenario.name, "CVE":scenario.cve, "difficulty":scenario.difficulty, "type":scenario.type, "sources":scenario.sources, "images":images}
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
    types.remove("")
    return types

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
    
    name = scenario_json_data['name']
    cve = scenario_json_data['CVE']
    diff = scenario_json_data['difficulty']
    type = scenario_json_data['type']
    sources = scenario_json_data['sources']
    
    desc = ""; goal = ""; sol = ""
    if readme_path != "":
        desc, goal, sol = ParseReadme(readme_path)
    
    images = dict[str,Image]()
    for image in scenario_json_data['images']:
        for key in image:
            if image[key] == "N/A":
                image[key] = ""
        images[image['name']] = (Image(name=image['name'], dockerfile=image['dockerfile'], is_main=image['is_main'], ports=image['ports'], os=image['operating_system']))

    return Scenario(name=name, CVE=cve, difficulty=diff, type=type, sources=sources, description=desc, goal=goal, solution=sol, images=images)

def ParseReadme(readme_file_path : str) -> tuple[str, str, str]:
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