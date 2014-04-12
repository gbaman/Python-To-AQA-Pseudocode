
#Python-to-AQA-psudocode converter
#By Andrew Mulholland aka gbaman

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.



#Enter the file name of the python file you want to convert below
#You should use its full file path
pythonFile = "test.py"




import time
from logging import debug, info, warning, basicConfig, INFO, DEBUG, WARNING
basicConfig(level=WARNING)



def getTextFile(filep):
    file = open(filep)
    svgfile = []
    while 1:
        line = file.readline()
        if not line:
            break
        svgfile.append(line) #Go through entire SVG file and import it into a list
    return svgfile

def removeN(svgfile):
    time.sleep(0.5)
    for count in range(0, len(svgfile)):
        #print(len(svgfile))
        #print(svgfile[count][0: (len(svgfile[count]))-1])
        svgfile[count] = svgfile[count][0: (len(svgfile[count]))-1]
    return svgfile

def blankLineRemover(svgfile):
    toremove = [ ]
    #toremove.append(len(svgfile))
    for count in range(0, len(svgfile)): #Go through each line in the text file
        found = False
        for i in range(0, len(svgfile[count])): #Go through each char in the line
            if not (svgfile[count][i] == " "):
                found = True
        if found == False:
            toremove.append(count)

    #toremove.append(len(svgfile))
    toremove1 = []
    for i in reversed(toremove):
        toremove1.append(i)


    for r in range(0, len(toremove)):
        svgfile.pop(toremove1[r])
        debug("just removed " + str(toremove1[r]))
    return svgfile



def wordReplacer(svgfile, clues, charCheck = True, removeEndChar = False):   #Charcheck can be used to disable specific character checking, will remove words in middle of things though!
    usefulLineNums = []

    for count in range(0, len(svgfile)):
        for i in range(0, len(clues)):
            found = svgfile[count].find(clues[i][0]) #Check if the current line in the SVG file has the required string
            if not (found == -1):
                if (found > 0) and (len(svgfile[count]) > (found+len(clues[i][0]))) and charCheck:
                    workingOn = svgfile[count]
                    debug(svgfile[count][found-1])
                    debug(svgfile[count][found+len(clues[i][0])])
                    if count == 14:
                        pass
                    if ((svgfile[count][found-1] == "(") or (svgfile[count][found-1] == " ") or (svgfile[count][found-1] == '"') or (svgfile[count][found-1] == '.')) and ((svgfile[count][found+len(clues[i][0])] == "(") or (svgfile[count][found+len(clues[i][0])]== " ") or (svgfile[count][found+len(clues[i][0])] == '"') or (svgfile[count][found+len(clues[i][0])] == ".")):
                        firstbit = svgfile[count][:found]
                        secondbit = svgfile[count][found+len(clues[i][0]):len(svgfile[count])]
                        fixed = firstbit + clues[i][1] + secondbit
                        svgfile[count] = fixed

                else:
                    firstbit = svgfile[count][:found]
                    secondbit = svgfile[count][found+len(clues[i][0]):len(svgfile[count])]
                    fixed = firstbit + clues[i][1] + secondbit
                    svgfile[count] = fixed
                    if removeEndChar:
                        WorkingOn = removeEndBit(svgfile[count], clues[i][2])
                        svgfile[count] = WorkingOn
    return svgfile


def writeTextFile(svgfile, name = "/Users/andrew/PycharmProjects/Experiments/psudocode/pythonfixed.py"):
    name = name[0:len(name)-3] + "-Psudocode" + name[(len(name)-3) : len(name)]
    file = open(name, 'w')
    mainstr = ""
    for i in range(0, len(svgfile)):
        mainstr = mainstr + svgfile[i] + "\n"
    file.write(mainstr)
    file.close()
    print("")
    print("------------------------")
    print("Psudocode file generated")
    print("The file can be found at " + name)
    print("------------------------")
    print("")




def indentationFinder(svgfile):
    searchFor = [["if", "ENDIF", [], [], False], ["def", "ENDFUNCTION", [], [] , True ], ["class", "ENDCLASS", [], [] , True ], ["while", "ENDWHILE", [], [] , False ], ["for", "ENDFOR", [], [] , False]]
    #print("CLEAR")
    for count in range(len(svgfile)): #Iterate through each line in the text file
        for i in range(len(searchFor)): #For each line in text file, iterate through clues
            currentClue = searchFor[i][0]
            found = svgfile[count].find(searchFor[i][0]) #Check if the current line in the SVG file has the required string
            #print("founder!" + str(found))


            if not (found == -1):
                debug("found an if on line " + str(count))
                #print(svgfile[count])
                debug("found is " + str(found))
                time.sleep(0.1)
                distance = found
                lineDone = False
                for a in range(count+1, len(svgfile)): #Iterate through rest of the lines
                    f = False

                    for x in range(0, distance + 1): #
                        #if distance == 10:
                        #    print("10")
                        #letter = svgfile[a][x]
                        #liner = svgfile[a]
                        if distance == 0:
                            continue
                        try:
                            if not (svgfile[a][x] == " "):
                                #if not ((svgfile[a][distance:(distance+4)] == "else")or (svgfile[a][distance:(distance+1)] == "#") or (svgfile[a][distance:(distance+4)] == "elif")):
                                    #debug("End of statement is on line" + str(a))
                                    #f = True
                                #else:
                                #    debug("else found " + str(a))
                                if svgfile[a][distance:(distance+4)] == "else":
                                    debug("else found" + str(a))
                                    f = False
                                elif (svgfile[a][distance:(distance+1)] == "#"):
                                    debug("# found "+ str(a))
                                    f = False
                                elif (svgfile[a][distance:(distance+3)] == "~~~"):
                                    debug(svgfile[a][distance:(distance+4)])
                                    f = False
                                    #print("elif found " + str(a))
                                else:
                                    f = True

                        except:
                            debug("error")

                    if f:
                        if lineDone == False:
                            searchFor[i][2].append(a)
                            searchFor[i][3].append(distance)
                            lineDone = True
                        break
                        #continue
                    #print(svgfile[a])
    debug("HI")
    return searchFor



def rebuildList(svgfile, searchFor, toRemove = []):
    svgfile2 = []
    for i in range(0, len(svgfile)): #iterate through the text file
        for count in range(0, len(searchFor)): #Iterate through each of the words to be replaced
            if i in searchFor[count][2]: #Checks if this line is being requested
                for x in range(0, len(searchFor[count][2])): #If it is, lets iterate through and find the exact reference
                    if searchFor[count][2][x] == i: #Checks if it is the exact reference
                        workingWith = x
                        indented = ""
                        for z in range(0, searchFor[count][3][x]):
                            indented = indented + " "

                        svgfile2.append(indented + searchFor[count][1])
                        if searchFor[count][4]:
                            svgfile2.append("")
        if not (i in toRemove):
            svgfile2.append(svgfile[i])

    #for i in range(0, len(svgfile2)):
        #debug(svgfile2[i])
    return svgfile2


def removeLines(svgfile, clues):
    toRemove = []
    for i in range(0, len(svgfile)):
        for cl in range(0, len(clues)):
            found = svgfile[i].find(clues[cl])
            if found != (-1):
                toRemove.append(i)
    return toRemove

def convertStringToList(string):
    theList = []
    for x in range(0, len(string)):
        theList.append(string[x])
    return theList

def convertListToString(theList):
    string = ""
    for x in range(0, len(theList)):
        string = string + theList[x]
    return string

def removeEndBit(theLine, toRemove):
    theLine = convertStringToList(theLine)
    for i in range(len(theLine) -1, 0, -1):
        if theLine[i] == toRemove:
            theLine.pop(i)
            break
    return convertListToString(theLine)


def main(filename):

    print("Now working on " + filename)
    svgfile = getTextFile(filename)
    svgfile = removeN(svgfile)
    svgfile = blankLineRemover(svgfile)

    print("Searching through file, this may take a while")

    clues = [["elif", "~~~"],]

    for i in range(0, 6):
        svgfile = wordReplacer(svgfile, clues)

    searchfor =  indentationFinder(svgfile)

    svgfile = rebuildList(svgfile, searchfor, removeLines(svgfile, ["debug", "info", "warning", "#print"]))
    #writeTextFile(svgfile)




    for x in range(0, 10):
        svgfile = wordReplacer(svgfile, [["def", "FUNCTION"], ["print", "OUTPUT"], ["self.", " "], ["return", "RETURN"], ["else:", "ELSE:"], ["==", "|"], ["if", "IF"], ["or", "OR"], ["and", "AND"],["and", "AND"], ["class", "CLASS"]  ])
    for x in range(0, 5):
        svgfile = wordReplacer(svgfile, [["self.", " "],], False)
    for x in range(0, 10):
        svgfile = wordReplacer(svgfile, [["=", "<-"], ["~~~", "ELSEIF"]])
    for x in range(0, 10):
        svgfile = wordReplacer(svgfile, [["|", "="],])

    svgfile = wordReplacer(svgfile, [["OUTPUT(", "OUTPUT ", ")"]], False, True)


    svgfile = wordReplacer(svgfile, [["<- ?", "= ?"]])
    svgfile = wordReplacer(svgfile, [["<- ?", "= ?"]])


    writeTextFile(svgfile, filename)




#-----------------------------------Main program----------------------------------------
#-----------------------------------Main program----------------------------------------
#-----------------------------------Main program----------------------------------------



main(pythonFile)


print("")
print("")
print("----------------")
print("Process complete")
print("----------------")
