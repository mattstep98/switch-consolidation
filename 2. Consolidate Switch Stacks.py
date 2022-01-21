import os
import csv
import time


start_time = time.time()


myDir = os.listdir(os.getcwd())


#Create or rewrite csv file to store stack information from previously generated csv files
with open('Switches.csv', 'w', newline='') as f:
    
    #Writing the headers to the created file
    f.write('Switch Stack,Total Ports,Switch Counts,Access Points - Up,Access Points - Down,Data - Up,Data - Down,Phone - Up,Phone - Down,Camera - Up,Camera - Down,Trunk - Up,Trunk - Down,No Description - Up,No Description - Down,Other Count,Other Notes\n')

    #Looping through each file in the directiory that we are in, initializing variable to 0 for each file
    for filename in myDir:

        countTotalPorts = 0
        
        countAP_Up = 0
        countData_Up = 0
        countPhone_Up = 0
        countCamera_Up = 0
        countTrunk_Up = 0
        countNoDesc_Up = 0

        countAP_Down = 0
        countData_Down = 0
        countPhone_Down = 0
        countCamera_Down = 0
        countTrunk_Down = 0
        countNoDesc_Down = 0

        countOtherDesc = 0
        otherDesc = ""

        switchNumPortsArr = []
        switchNumPortsDesc = ""
        switchArrPrev = 0
        
        #Only open the file if it is a csv file, and not the one we just created
        if (((filename[-3:]) == 'csv') and filename != 'MSU_Consolidated_Switches.csv'):
            switchName = filename[:-4]
            switchFile = open(filename, "r")

            #Loop through the csv for each stack. Saving a list version of the row for easier manipulation. RowArr = The entire row, InterfaceSplit=The interface split into a list by '/'. ex. Gi1/0/12 -> ['Gi1','0','12']
            for row in switchFile:
                rowArr = row.split(',')
                interfaceSplit = rowArr[0].split('/')

                #Only work with interfaces that begin with Gi or Te in this implementation
                if (row[0:2].lower() == "gi" or row[0:2].lower() == "te"):

                    #Add one to totalPorts if the interface contains 3 parts (Gi1/0/12 is good. Gi0/0 is not counted)
                    if((len(interfaceSplit) > 2) and ((int(interfaceSplit[1]) == 0) or ((int(interfaceSplit[1]) == 1) and row[0:2].lower() == 'te'))):
                        countTotalPorts += 1

                    #If gig interface and second position is 0 and contains the 3 parts similar to above(pattern: Gi#/0/#) or is a Te port and second position is 1(pattern:Te#/1/#) then we want to update the array with the amount of ports for each switch in the stack.
                    #We allocate a new position in the array if we move onto a new switch in the stack
                    if(((interfaceSplit[0])[0:2].lower() == 'gi' and (int(interfaceSplit[1]) == 0) and (len(interfaceSplit) > 2)) or ((row[0:2].lower() == "te") and (int(interfaceSplit[1]) == 0))):
                        if (int((interfaceSplit[0])[2:]) != switchArrPrev):
                            switchNumPortsArr.append(0)
                        switchNumPortsArr[int((interfaceSplit[0])[2:])-1] = interfaceSplit[2]
                        switchArrPrev = int((interfaceSplit[0])[2:])
                    #Length of row array is 4 or more, then we know that there is a description for the port. Incrementing by one for a matched description    
                    if not(len(rowArr) < 4):
                        rowDesc = str(rowArr[3].lower())

                        #Matched Description for where the ports are UP according to the status of the port. If no matches, increment other and append the formatted description to the other notes column
                        if ((rowArr[1].lower()) == "up"):
                            if("access point" in rowDesc):
                                countAP_Up += 1
                            elif(("data") in rowDesc):
                                countData_Up += 1
                            elif(("phone") in rowDesc):
                                countPhone_Up += 1
                            elif(("camera") in rowDesc):
                                countCamera_Up += 1
                            elif((("trunk") in rowDesc) or (("po") in rowDesc)):
                                countTrunk_Up += 1
                            else:
                                otherDesc += ("[" + rowArr[0] + ":" + rowDesc.strip() + ":up" + "]")
                                countOtherDesc += 1
                                                            
                        #Matched Description for where the ports are DOWN according to the status of the port. If no matches, increment other and append the formatted description to the other notes column
                        if ((rowArr[1].lower()) == "down"):
                            if("access point" in rowDesc):
                                countAP_Down += 1
                            elif(("data") in rowDesc):
                                countData_Down += 1
                            elif(("phone") in rowDesc):
                                countPhone_Down += 1
                            elif(("camera") in rowDesc):
                                countCamera_Down += 1
                            elif((("trunk") in rowDesc) or (("po") in rowDesc)):
                                countTrunk_Down += 1
                            else:
                                otherDesc += ("[" + rowArr[0] + ":" + rowDesc.strip() + ":down" + "]")
                                countOtherDesc += 1
                                
                    #If the length is less than 4 for the row, there is no description, increment the variable depending if the status is UP or Down        
                    else:
                        if(rowArr[1].lower() == "up"):
                            countNoDesc_Up += 1
                        else:
                            countNoDesc_Down += 1


            #Formatting the array we created for the switch number and gig ports in the switch to identify what kind of switch it is        
            switchNum = 1
            for switchPortsNum in switchNumPortsArr:
                switchNumPortsDesc += "[Switch" + str(switchNum) + ":" + str(switchPortsNum) + "Ports]"
                switchNum += 1

                
            #Writing each row to the consolidated file  
            f.write(switchName + ',' + str(countTotalPorts) + ',' + str(switchNumPortsDesc) + ',' + str(countAP_Up) + ',' + str(countAP_Down) + ',' + str(countData_Up) + ',' + str(countData_Down) + ',' + str(countPhone_Up) + ',' + str(countPhone_Down) + ',' + str(countCamera_Up) + ',' + str(countCamera_Down) + ',' + str(countTrunk_Up) + ',' + str(countTrunk_Down) + ',' + str(countNoDesc_Up) + ',' + str(countNoDesc_Down) + ',' + str(countOtherDesc) + ',' + str(otherDesc) + '\n')

    #Closing the file we were writing to        
    f.close()

#Printing the amount of time it took to complete    
print("--- %s seconds ---" % str((time.time() - start_time))[0:6])       
            
