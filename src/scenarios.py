import os
import json
from scenario import Scenario

scenarios = {}
scenarios_file = "scenarios.json"

# A few default variables
scenarios['scenarios'] = []
scenarios['total'] = 0
scenarios['types'] = []
scenarios['total_types'] = 0

def Load() -> dict:
    '''
    Returns the scenarios database as a python dictionnary.
    '''
    global scenarios

    if not os.path.exists(scenarios_file):
        with open(scenarios_file, 'w') as file:
            file.write(json.dumps(scenarios))
            return scenarios

    with open(scenarios_file, 'r') as file:
        _scenarios = json.load(file)
        return _scenarios
    
def scenarioIndex(s_list : dict, name : str):
    '''

    '''
    for index, scenario in enumerate(s_list):
        if scenario['name'] == name:
            return index
            
def UpdateFields(func):
    '''
    Decorator of the Save() function to properly update all the variables of the scenario database file. 
    '''
    def UpdateTypes(s_list, types):
        for scenario in s_list:
            if scenario['type'] not in types and scenario['type'] is not None:
                types.append(scenario['type'])
        return types

    def wrapper(*args, **kwargs):

        scenarios = func(*args, **kwargs)
        scenarios['total'] = len(scenarios['scenarios'])
        scenarios['types'] = UpdateTypes(scenarios['scenarios'], scenarios['types'])
        scenarios['total_types'] = len(scenarios['types'])

        with open(scenarios_file, 'w') as file:
            file.write(json.dumps(scenarios))

    return wrapper

@UpdateFields
def Save(Scenario : Scenario):
    '''
    Saves a given Scenario object into the database file, updating all the necessary fields.
    '''
    scenarios = Load()

    index = scenarioIndex(scenarios['scenarios'], Scenario.name)
    if index is not None:
        scenarios['scenarios'][index] = Scenario.__str__()
    else:
        scenarios['scenarios'].append(Scenario.__str__())

    return scenarios

def Parse(_json : dict) -> Scenario:
    '''
    Instanciates a Scenario object from a json string.
    ---------------
    Parameters:

    _json: The dictionnary we are going to read to instantiate the scenario.
    '''
    name = _json['name']
    desc = _json['description']
    base = _json['base']
    images = _json['images']
    type = _json['type']

    scen = Scenario(name, desc, base, images, type)
    return scen

def LoadScenario(name : str) -> Scenario:

    scenarios = Load()
    index = scenarioIndex(scenarios['scenarios'], name)
    if index is not None:
        return Parse(scenarios['scenarios'][index])
    
# region =====Testing=====

def test_saving_scenarios():
    ubuntu = Scenario('Blank Ubuntu', 'Basic ubuntu image', 'ubuntu', ['ubuntu'], None)
    kali = Scenario('Blank Kali', 'Basic kali image', 'kali', ['kali'], None)
    Save(ubuntu)
    Save(kali)

def test_retrieving_scenario():
    ubuntu = LoadScenario('Blank Ubuntu')
    fake = LoadScenario('Fake')
    print(ubuntu.__str__())
    print(fake)

# endregion

if __name__ == "__main__":
    test_saving_scenarios()
    #test_retrieving_scenario()