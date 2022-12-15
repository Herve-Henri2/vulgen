# This program was created for the vulgen project at https://github.com/Herve-Henri2/vulgen to be part of the scenario called "Antares supply chain"
# Author: Hervé-Henri Houzard
# https://psutil.readthedocs.io/en/latest/

import os, platform, psutil, json


def get_system_info():
    '''
    Gathers information about the current machine such as the os, the process number or cpu usage.
    '''
    sys_info = {}
    sys_info['operating_system'] = f"{os.name} - {platform.system()} {platform.release()}"
    sys_info['machine_name'] = f"{platform.node()}"
    sys_info['machine_type'] = f"{platform.machine()}"
    sys_info['process_number'] = len([proc for proc in psutil.process_iter()])
    sys_info['cpu_cores'] = psutil.cpu_count(logical=False)
    sys_info['cpu_freq'] = f"{psutil.cpu_freq()[0] / 1000} GHz (max: {psutil.cpu_freq()[2] / 1000} GHz)"
    sys_info['cpu_usage'] = f"{psutil.cpu_percent()} %"
    sys_info['memory_usage'] = f"{psutil.virtual_memory()[2]} %"
    sys_info['storage_usage'] = f"{psutil.disk_usage('/')[3]} %"

    return sys_info

def get_network_info():
    '''
    Gathers information about the current machine's network connections and traffic.
    '''
    net_info = {}
    connections = psutil.net_connections()
    interfaces = psutil.net_if_addrs()

    net_info['Interfaces'] = {}
    for interface in interfaces:
        if_info = interfaces[interface]
        interface_dict = net_info['Interfaces'][interface] = {}

        mac_address, ipv4, ipv6, netmask = None, None, None, None
        for nic in if_info:
            if '-' in nic[1]:
                mac_address = nic[1]
            elif '.' in nic[1]:
                ipv4 = nic[1]
                netmask = nic[2]
            elif ':' in nic[1]:
                ipv6 = nic[1]

        interface_dict['MAC'] = mac_address 
        interface_dict['IPv4'] = ipv4
        interface_dict['IPv6'] = ipv6
        interface_dict['netmask'] = netmask

    return net_info

def clear():
    '''
    Clears the console.
    '''
    os.system('cls' if os.name=='nt' else 'clear')

def clear2():
    '''
    Clears the console.
    '''
    print("\033[H\033[3J", end="")

def AppendDict(_dict : dict, text=""):
    '''
    Appends a dictionnary to a given text, or returns a dictionnary as a string.
    '''
    for key, value in _dict.items():
        if isinstance(key, str):
            if isinstance(value, str):
                text += f"{key.replace('_', ' ').capitalize()}: {value}\n"
            elif isinstance(value, dict):
                text += f"{key.replace('_', ' ').capitalize()}: {json.dumps(value, indent=3, ensure_ascii=False)}\n"
    return text

def main():

    logo = ("""
            ___            __                          
           /   |   ____   / /_ ____ _ _____ ___   _____ Tm
          / /| |  / __ \ / __// __ `// ___// _ \ / ___/
         / ___ | / / / // /_ / /_/ // /   /  __/(__  ) 
        /_/  |_|/_/ /_/ \__/ \__,_//_/    \___//____/ 
        """)

    def mainmenu():
        print("Select one of the following by entering the corresponding number:\n"
        "1. Display System Information\n"
        "2. Display Network Information")
        choice = str(input("Your choice: "))
        if choice == "1":
            sys_info = get_system_info()
            text = "----------------------------System Information----------------------------\n"
            text = AppendDict(sys_info, text)
            print(text)
            mainmenu()
        elif choice == "2":
            net_info = get_network_info()
            text = "----------------------------Network Information----------------------------\n"
            text = AppendDict(net_info, text)
            print(text)
            mainmenu()
        else:
            print("Incorrect input")
            mainmenu()

    print(logo)
    mainmenu()


if __name__ == "__main__":
    main()
    