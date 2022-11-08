from dis import Instruction
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
        CreateDefault()

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

def CreateDefault():
    '''
    Function that writes all the default scenarios into the scenarios file.
    '''
    
    # Scenario 1 : log4shell
    name = 'log4shell'
    base = 'ghcr.io/christophetd/log4shell-vulnerable-app'
    description = ('Also known as CVE-2021-44228, log4shell is a zero-day software vulnerability in Apache Log4j2, a popular Java library used for logging purposes in applications.\n'
                   'This vulnerability enables a remote attacker to take control of a device on the internet if the device is running certain unpatched versions of Log4j2.\n'
                   'In December 2021, Apache had to release up to 4 corrective patches to fully close the breach. It is believed that malicious actors likely knew about the vulnerability'
                   ' and exploited it before experts did, hence why it is considered zero-day.')
    instructions = ('You need to do this and that, blablabla.')
    images = {}
    images['main'] = {}
    images['main']['name'] = base
    images['main']['interaction'] = 'browser'
    images['main']['ports'] = {"8080/tcp":8080} # Container port: Host port
    images['main']['download_link'] = None
    images['other'] = []
    cve = 'CVE-2021-44228'
    type = 'Remote Code Execution'
    sources = ['https://www.dynatrace.com/news/blog/what-is-log4shell/', 'https://en.wikipedia.org/wiki/Log4Shell', 'https://github.com/christophetd/log4shell-vulnerable-app']
    scenario = Scenario(name, description, instructions, base, images, cve, type, sources)
    Save(scenario)


def Parse(_json : dict) -> Scenario:
    '''
    Instanciates a Scenario object from a json string.
    ---------------
    Parameters:

    _json: The dictionnary we are going to read to instantiate the scenario.
    '''
    name = _json['name']
    desc = _json['description']
    inst = _json['instructions']
    base = _json['base']
    images = _json['images']
    cve = _json['CVE']
    type = _json['type']
    sources = _json['sources']

    scen = Scenario(name, desc, inst, base, images, cve, type, sources)
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
    #test_saving_scenarios()
    #test_retrieving_scenario()
    scen = Load()
    print(json.dumps(scen, indent=3))