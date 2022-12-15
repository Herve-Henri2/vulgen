# This program was created for the vulgen project at https://github.com/Herve-Henri2/vulgen to be part of the scenario called "Antares supply chain"
# Author: Hervé-Henri Houzard
#  

import time, os, sys, platform, psutil

def get_system_info():
    sys_info = {}
    sys_info['operating_system'] = f"{os.name} - {platform.system()} {platform.release()}"
    sys_info['machine_name'] = f"{platform.node()}"
    sys_info['machine_type'] = f"{platform.machine()}"
    sys_info['process_number'] = len([proc for proc in psutil.process_iter()])
    sys_info['cpu_cores'] = psutil.cpu_count(logical=False)
    sys_info['cpu_freq'] = f"{psutil.cpu_freq()[0] / 1000} GHz"
    sys_info['cpu_usage'] = f"{psutil.cpu_percent()} %"
    sys_info['memory_usage'] = f"{psutil.virtual_memory()[2]} %"
    sys_info['disk_usage'] = f"{psutil.disk_usage('/')[3]} %"

    return sys_info

def main():
    # https://psutil.readthedocs.io/en/latest/index.html?highlight=disk%20usage

    def mainloop():
        sys_info = get_system_info()
        text = ("""
            ___            __                          
           /   |   ____   / /_ ____ _ _____ ___   _____ Tm
          / /| |  / __ \ / __// __ `// ___// _ \ / ___/
         / ___ | / / / // /_ / /_/ // /   /  __/(__  ) 
        /_/  |_|/_/ /_/ \__/ \__,_//_/    \___//____/ 
        """)
        text += "\n----------------------------System Information----------------------------\n"
        for key, value in sys_info.items():
            if isinstance(key, str):
                text += f"{key.replace('_', ' ').capitalize()}: {value}\n"
        print(text)

    while True:
        mainloop()
        time.sleep(600) # repeat every 10 minutes

if __name__ == "__main__":
    main()