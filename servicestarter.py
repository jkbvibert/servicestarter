import requests
from requests.auth import HTTPBasicAuth
import getpass
import socket
import paramiko
import re
import reprlib  #used for the repr function to debug
from colorama import init, Fore, Back, Style
import configparser

def all_servers(servers):
    if len(servers) != 1:
        print(Style.BRIGHT + Fore.GREEN + "All Servers" + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + Fore.GREEN + "Single server installation" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.YELLOW + "1. " + Style.RESET_ALL + "service1")
    print(Style.BRIGHT + Fore.YELLOW + "2. " + Style.RESET_ALL + "service2")
    print(Style.BRIGHT + Fore.YELLOW + "3. " + Style.RESET_ALL + "service3")
    print(Style.BRIGHT + Fore.YELLOW + "4. " + Style.RESET_ALL + "service4")
    print(Style.BRIGHT + Fore.YELLOW + "5. " + Style.RESET_ALL + "service5")
    print(Style.BRIGHT + Fore.YELLOW + "6. " + Style.RESET_ALL + "service6")
    print(Style.BRIGHT + Fore.YELLOW + "7. " + Style.RESET_ALL + "service7")
    print(Style.BRIGHT + Fore.YELLOW + "8. " + Style.RESET_ALL + "All Services")
    answer = input("Enter #s (separated by columns): ")
    if answer == "8":
        conf_var = input("Are you certain? Y/N: ")
        if conf_var.lower() == "no" or conf_var.lower() == "n":
            print("Exiting")
            exit(0)
    answer = answer.replace(" ", "")
    answer = answer.split(",")
    services = []
    for number in answer:
        if number == 1:
            services.append("service1")
        elif number == 2:
            services.append("service2")
        elif number == 3:
            services.append("service3")
        elif number == 4:
            services.append("service4")
        elif number == 5:
            services.append("service5")
        elif number == 6:
            services.append("service6")
        elif number == 7:
            services.append("service7")
        elif number == 8:
            services = ["service1", "service2", "service3", "service4", "service5", "service6","service7"]
    for server_name in servers:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=server_name, username=sshun,key_filename=r"C:\Users\<directory>\file.ppk",passphrase=sshpw)
        print(Fore.GREEN + Style.BRIGHT + '++ ' + server_name + ' ++' + Style.RESET_ALL)
        for service in services:
            print(Style.BRIGHT + Fore.YELLOW + service + Style.RESET_ALL + " is being restarted")
            stdin, stdout, stderr = client.exec_command('sudo /sbin/service servicename restart' + service, timeout=10) #creates an array with each value being its own line
            service_stdout = stdout.readlines()  # can only be read once so needs to be stored at first read
            service_stdout = repr(''.join(service_stdout))  # converts the array into a string
            match = re.search(r"(unrecognized service)", service_stdout)
            if match is None:  # if not unrecognized service
                match = re.search(r"(stopped).*(started)", service_stdout)
                if match is not None:
                    print(
                        Style.BRIGHT + Fore.YELLOW + service + Style.RESET_ALL + " was " + Style.BRIGHT + Fore.GREEN + "successfully" + Style.RESET_ALL + " restarted")
                else:
                    print(
                        Style.BRIGHT + Fore.YELLOW + service + Style.RESET_ALL + Style.BRIGHT + Fore.RED + " unsuccessfully " + Style.RESET_ALL + "restarted: ")
                    print(service_stdout)
        client.close()

init()
config = configparser.ConfigParser()
config.read('params.txt')
if config.has_option('<service_acronym>', 'email'):  # login to API and check if API is functioning as expected
    email = config.get('<service_acronym>', 'email')
else:
    config['<service_acronym>'] = {'email': ''}
    email = input("Enter your <service_acronym> email address: ")
    match = re.search(r"(.+)[@](\S+)(\.com)", email)
    if not match:
        print(Style.BRIGHT + Fore.RED + "Not a valid email" + Style.RESET_ALL)
        exit(1)
    config['<service_acronym>']['email'] = email
<service_acronym>pw = getpass.getpass('<service_acronym> Password: ')

resp = requests.get('<API_endpoint>', auth=HTTPBasicAuth(email, <service_acronym>pw))
if resp.status_code != 200:
    print("Received non-200 status code [%s] (likely incorrect pw)\nABORTING!" % resp.status_code)
    exit(1)
else:
    resp_formatted = resp.json()
    if resp_formatted['id'] == 0:
        print("ID == 0\nABORTING!")
        exit(1)

<service_acronym>id = input("Enter the InstallationID to operate on: ")

# grab hosts for that <service_acronym> id
resp = requests.get('<API_endpoint>' + <service_acronym>id, auth=HTTPBasicAuth(email, <service_acronym>pw))
containers = resp.json()
servers = []
for each in containers:
    servers.append(each['hostname'])
servers = list(set(servers))
servers.sort(reverse=True)
if config.has_option('SSH', 'username'):
    sshun = config.get('SSH', 'username')
else:
    config['SSH'] = {'username': ''}
    sshun = input("Enter your SSH username: ")
    config['SSH']['username'] = sshun
sshpw = getpass.getpass('SSH passphrase: ')
with open('params.txt', 'w') as configfile:
    config.write(configfile)

try:
    if len(servers) != 1:
        msg = "Would you like to operate on " + Style.BRIGHT + Fore.YELLOW + "some" + Style.RESET_ALL + " or " + Style.BRIGHT + Fore.YELLOW + "all" + Style.RESET_ALL + " servers? "
        print(msg, end="")
        services_prompt = input()
        if services_prompt.lower() == 'some':
            num = 1
            for each in servers:
                print(Style.BRIGHT + Fore.YELLOW + str(num) + Style.RESET_ALL + ". " + each)
                num += 1
            answer = input("Enter #s (separated by columns): ")
            answer = answer.replace(" ", "")
            answer = answer.split(",")
            print(Style.BRIGHT + Fore.YELLOW + "1. " + Style.RESET_ALL + "service1")
            print(Style.BRIGHT + Fore.YELLOW + "2. " + Style.RESET_ALL + "service2")
            print(Style.BRIGHT + Fore.YELLOW + "3. " + Style.RESET_ALL + "service3")
            print(Style.BRIGHT + Fore.YELLOW + "4. " + Style.RESET_ALL + "service4")
            print(Style.BRIGHT + Fore.YELLOW + "5. " + Style.RESET_ALL + "service5")
            print(Style.BRIGHT + Fore.YELLOW + "6. " + Style.RESET_ALL + "service6")
            print(Style.BRIGHT + Fore.YELLOW + "7. " + Style.RESET_ALL + "service7")
            print(Style.BRIGHT + Fore.YELLOW + "8. " + Style.RESET_ALL + "All Services")
            service_answer = input("Enter #s separated by columns): ")
            if service_answer == "8":
                conf_var = input("Are you certain? Y/N: ")
                if conf_var.lower() == "no" or conf_var.lower() == "n":
                    print("Exiting")
                    exit(0)
            service_answer = service_answer.replace(" ", "")
            service_answer = service_answer.split(",")
            service_answer = list(map(int, service_answer))
            services = []
            for number in service_answer:
                if number == 1:
                    services.append("service1")
                elif number == 2:
                    services.append("service2")
                elif number == 3:
                    services.append("service3")
                elif number == 4:
                    services.append("service4")
                elif number == 5:
                    services.append("service5")
                elif number == 6:
                    services.append("service6")
                elif number == 7:
                    services.append("service7")
                elif number == 8:
                    services = ["service1", "service2", "service3", "service4", "service5","service6", "service7"]
            for server_name in servers:
                for each in answer:
                    if server_name == servers[int(each)-1]:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(hostname=server_name, username=sshun,key_filename=r"C:\Users\<directory>\file.ppk",passphrase=sshpw)
                        print(Fore.GREEN + Style.BRIGHT + '++ ' + server_name + ' ++' + Style.RESET_ALL)
                        for service in services:
                            print(Style.BRIGHT + Fore.YELLOW + service + Style.RESET_ALL + " is being restarted")
                            stdin, stdout, stderr = client.exec_command('sudo /sbin/service <servicename> restart ' + service, timeout=10) #creates an array with each value being its own line
                            service_stdout = stdout.readlines()  # can only be read once so needs to be stored at first read
                            service_stdout = repr(''.join(service_stdout))  # converts the array into a string
                            match = re.search(r"(unrecognized service)", service_stdout)
                            if match is None:  # if not unrecognized service
                                match = re.search(r"(stopped).*(started)", service_stdout)
                                if match is not None:
                                    print(Style.BRIGHT + Fore.YELLOW + service + Style.RESET_ALL + " was " + Style.BRIGHT + Fore.GREEN + "successfully" + Style.RESET_ALL + " restarted")
                                else:
                                    print(Style.BRIGHT + Fore.YELLOW + service + Style.RESET_ALL + Style.BRIGHT + Fore.RED + " unsuccessfully " + Style.RESET_ALL + "restarted: ")
                                    print(service_stdout)
                        client.close()
        elif services_prompt.lower() == 'all':
            all_servers(servers)
        else:
            exit(0)
    else:
        all_servers(servers)
except socket.timeout as e:
    print(Fore.YELLOW + "Command timed out" + Style.RESET_ALL)
    client.close()
except paramiko.SSHException:
    print(Style.BRIGHT + Fore.RED + "Failed to execute the command for some reason on " + Fore.GREEN + each + Style.RESET_ALL + Fore.RED + Style.BRIGHT + ". Look into this if hit" + Style.RESET_ALL)
    client.close()