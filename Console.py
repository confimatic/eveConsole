# Import the necessary packages
from subprocess import PIPE, run
from consolemenu import *
from consolemenu.items import *
import json


def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout



def main():

    target = "192.168.1.10"

    # Get the list of devices and its telnet port
    my_output = out("ps -fea | pcregrep --om-separator=, -o3 -o1 -o2 '_wrapper -C\s([0-9]{5})\s.*-T\s([^\s]*)\s.*-t\s([^\s]*)' | uniq")

    # Create a list with the result of the command
    list_output = my_output.split('\n')

    # Initialize variables 
    consoleDic = {}

    # Convert array to dictionary
    for element in list_output:

        elementArray = element.split(',')
        if len(elementArray) > 1:

            name = elementArray[0]
            port = elementArray[1]
            lab = elementArray[2]

            consoleDic[name] = [port, lab]

    # Sort dictionary alphabetically, it returns an ordered array
    consoleSorted = (sorted(consoleDic.items()))

    # Create the menu
    menu = ConsoleMenu("Console server EVE", "Please select the device")

    menuDic = dict()
    # Create a dictionary with lab number, device name and TCP port
    for console in consoleSorted:
        if console[1][1] in menuDic:
            menuDic[console[1][1]].append([console[0],console[1][0]])
        else:
            menuDic[console[1][1]] = [[console[0],console[1][0]]]


    #print(json.dumps(menuDic, indent=2))

    # Get the lab numbers
    keys = []
    for key in menuDic:
        keys.append(key)





    # Create the menu content
    for key in menuDic:
        
        submenu = ConsoleMenu("LAB " + key, "Console server")

        for console in menuDic[key]:
            command = 'telnet ' + target + ' ' + console[1]
            command_item = CommandItem(console[0],command)
            submenu.append_item(command_item)


        submenu_item = SubmenuItem("LAB " + key, submenu=submenu)
        submenu_item.set_menu(menu)

        menu.append_item(submenu_item)



    # Finally, we call show to show the menu and allow the user to interact
    # Show the menu
    menu.start()
    menu.join()


if __name__ == "__main__":
    main()
