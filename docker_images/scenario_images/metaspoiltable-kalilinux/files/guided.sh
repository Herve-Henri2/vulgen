#! /bin/bash

# Get your ip and the subnet address
network_identification(){
    echo -e "In order to get information on your IP address and the networks you're in you can use 'ip a'."

    read -p "Press Enter to see the command output:"

    echo -e "\n> ip a"
    ip a || true
}

# Look for other machines in the network
network_exploration(){
    echo -e "'netdiscover -r {network_ip}' allows you to see all the IP addresses in the provided network. ('q' to stop)"

    read -p "Address of the network you wish to explore: " network_ip

    echo -e "\n> netdiscover -r $network_ip"
    netdiscover -r $network_ip || true
}

# Looking for open ports on the metasploitable2 machine
ports_discovery(){
    echo -e "'nmap {machine_ip}' will check for open ports on the provided machine."

    read -p "Address of the machine you want to check: " machine_ip

    echo -e "\n> nmap $machine_ip"
    nmap $machine_ip || true
}

# Exploiting ftp
ftp_connection(){
    echo -e "When a ftp server is not correctly configured anyone can open a connection using anonymous/anonymous."
    echo -e "To open a connection you can use the command 'ftp {server_ip} {port}'."

    read -p "Address of the machine: " machine_ip
    read -p "Port to use: " port

    echo -e "\n> ftp $machine_ip $port"
    ftp $machine_ip $port || true
}


# Main
main(){
    choice=-1
    while [ $choice -ne 0 ]
    do
        echo -e "Menu:"
        echo -e "\t1. Network identification"
        echo -e "\t2. Network exploration"
        echo -e "\t3. Ports discovery"
        echo -e "\t4. ftp connection"
        echo -e "\t0. Exit\n"

        read -p "Choice: " choice
        echo -e ""

        case $choice in
            1)
                network_identification
                ;;

            2)
                network_exploration
                ;;

            3)
                ports_discovery
                ;;

            4)
                ftp_connection
                ;;
        esac

        echo -e "\n"
    done
}

main
