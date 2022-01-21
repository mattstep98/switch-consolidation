from netmiko import ConnectHandler
import csv
import os
import re
import time


def main():

    #Open the file that contains device name in colA and ipAddr in colB
    with open('MSU_AcademicSwitches.csv',newline='') as csvfile:
        line = csv.reader(csvfile,dialect='excel')
        #Row A:deviceName, Row B:ipAddr
        #next(line) if there are headers
        
        #Set each variable for the row to work with and get rid of any whitespace
        for row in line:
            deviceName = row[0].strip()
            ipAddr = row[1].strip()

            #Create a txt file named the deviceName from the csv. This will store the output from the switch
            f = open(deviceName+".txt", "w")
            
            #Switch information
            cisco_switch = {
                'device_type': 'cisco_ios',
                'host':   ipAddr,
                'username': '',
                'password': '',
                'port' : 22,          # optional, defaults to 22
                #'secret': 'secret',     # optional, defaults to ''
            }

            #Command to connect to the switch via ssh
            net_connect = ConnectHandler(**cisco_switch)

            #Sending the command to the switch
            output = net_connect.send_command('show interfaces description')

            #Writing the command's output to the txt file we created
            f.write(output)
            f.close()

    #Once finished with getting the output for each stack in the switch, we loop through each txt file we created
    myDir = os.listdir(os.getcwd())
    for filename in myDir:
        #Only work with files ending in the extension txt, these are the ones we created
        if (filename[-3:]) == 'txt':
            interfaceFile = open(filename, "r")
            #Skip the first line of the txt file becasue that is the header that we will write in later due to formatting
            next(interfaceFile)

            #Create the csv with the deviceName's to work with the data much easier than if it were just a txt file  
            with open(filename[:-4] + '.csv', 'w', newline='') as f:

                #Writing in the headers to the file
                f.write("Interface,Status,Protocol,Description\n")

                #Navigating through each line of the file. Replacing whitespace with commas with simple regex to adhere to the csv format. Writing it to the file
                for line in interfaceFile:
                    writeLine = ""
                    line = line.strip()

                    count = 0

                    writeLine += (re.sub('\s{2,}', ',', line))
                    output = writeLine + "\n"

                    f.write(output)
                    
            #Closing Files and deleting the temporary txt files       
            f.close()
            interfaceFile.close()
            os.remove(filename)


if __name__ == "__main__":
    input("Welcome!\n\nPlease ensure that you are in a directory that has nothing but this python file and a '.csv' including 'Device Names','IP Addresses'\n\nHit 'enter' to proceed or 'ctrl+c' to quit.")
    start_time = time.time()
    main()
    print("--- %s seconds ---" % str((time.time() - start_time))[0:6]) 




