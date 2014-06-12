
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
    """
    Opens the text file and goes through line by line, appending it to the svgfile list.
    Each new line is a new object in the list, for example, if the text file was
    ----
    hello
    world
    this is an awesome text file
    ----
    Then the list would be
    ["hello", "world", "this is an awesome text file"]
    Each line is a new object in the list

    """
    file = open(filep)
    svgfile = []
    while 1:
        line = file.readline()
        if not line:
            break
        svgfile.append(line) #Go through entire SVG file and import it into a list
    return svgfile

def removeN(svgfile):
    """
    Removes the final character from every line, this is always /n, aka newline character.
    """
    for count in range(0, len(svgfile)):
        svgfile[count] = svgfile[count][0: (len(svgfile[count]))-1]
    return svgfile

def blankLineRemover(svgfile):
    """
    Removes blank lines in the file, these mess around with indentation tracing so are just removed.
    """
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

def multiLineCommentTracker(textFile):
    """
    Goes through the file and finds multiline comments. If a multiline comment is found, it will ignore the entire line! You have been warned
    """
    searchingForEnd = False
    startLine = 0
    endLine = 0
    avoidLines = []
    for count in range(0, len(textFile)):
        found = textFile[count].find('"""')
        if (found != -1):
            if searchingForEnd == False:
                searchingForEnd = True
                startLine = count
                foundMore = False
                for count3 in range(found, len(textFile[count])-3):
                    if textFile[count][count3 : count3+3] == '"""':
                        searchingForEnd = False

            else:
                searchingForEnd = False
                endLine = count
                for count2 in range(startLine, endLine+1):
                    avoidLines.append(count2)
                    #print(textFile[count2])
    return avoidLines



def wordReplacer(svgfile, linesToAvoid, clues, charCheck = True, removeEndChar = False):   #Charcheck can be used to disable specific character checking, will remove words in middle of things though!
    """
    wordReplacer goes through the program line by line removing the any items found in clues list. Think of it as a find and replacer.
    """
    usefulLineNums = []

    for count in range(0, len(svgfile)):
        for i in range(0, len(clues)):
            found = svgfile[count].find(clues[i][0]) #Check if the current line in the SVG file has the required string
            if (not (found == -1)) and not (count in linesToAvoid):
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
    """
    Writes the final list to a text file.
    Adds a newline character (\n) to the end of every sublist in the file.
    Then writes the string to the text file.
    """
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




def indentationFinder(svgfile, linesToAvoid):
    """
        This function traces through the entire file tracing indentation to find where structures start and end.
        The protocol for the lists is as follows
        [WordSearchingFor, WordReplaceWith, EmptyList, EmptyList, AddANewLineAfter?]
        The 2 emtpy lists are used to store the location and line number of where the items are found, which is passed onto the replacing function

        A basic description of what is going on
            We define the list of lists, searchFor which holds the stuff we are going to look for.
            We then, using a for loop iterate through every line.
            Inside that loop we have a second for loop which iterates through all the objects in searchFor.
            Basically we are checking to see if any of the words are on the current line, 1 word at a time from searchFor.
            If we find a word and it isn't a line we are meant to be avoiding (maybe it has a multiline comment?) we move down
                We assign distance to how many characters in from the left the found word was, this will be the level in we are tracing with.
                The program then searches each line that follows to see if it can find any character to the left (or equal) to distance on its current line.
                If it finds and first character is else, # or ~~~ it ignores those lines.
                If it isn't any of those special characters that has been found first, we can assume this structure has finished as it has unindentected.
                    We write the line number and how far in the structure started to the 2 empty lists inside the sublist.
            Finally we return the searchFor list, hopefully with lots of line numbers and indentation distances.


    """
    searchFor = [["if", "ENDIF", [], [], False], ["def", "ENDFUNCTION", [], [] , True ], ["class", "ENDCLASS", [], [] , True ], ["while", "ENDWHILE", [], [] , False ], ["for", "ENDFOR", [], [] , False]]
    #print("CLEAR")
    for count in range(len(svgfile)): #Iterate through each line in the text file
        for i in range(len(searchFor)): #For each line in text file, iterate through clues
            currentClue = searchFor[i][0]
            found = svgfile[count].find(searchFor[i][0]) #Check if the current line in the file has the required string
            #print("founder!" + str(found))


            if (not (found == -1)) and not (count in linesToAvoid):
                debug("found an if on line " + str(count))
                #print(svgfile[count])
                debug("found is " + str(found))
                #time.sleep(0.1)
                distance = found  #Distance is basically how many characters it is indented in
                lineDone = False
                for a in range(count+1, len(svgfile)): #Iterate through rest of the lines
                    f = False

                    for x in range(0, distance + 1): #
                        if distance == 0:
                            pass
                        try:
                            if not (svgfile[a][x] == " "):
                                if svgfile[a][distance:(distance+4)] == "else":
                                    debug("else found" + str(a))
                                    f = False
                                elif (svgfile[a][distance:(distance+1)] == "#"):
                                    debug("# found "+ str(a))
                                    f = False
                                elif (svgfile[a][distance:(distance+3)] == "~~~"):
                                    debug(svgfile[a][distance:(distance+4)])
                                    f = False
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
    debug("HI")
    return searchFor





def rebuildList(svgfile, searchFor, toRemove = []):
    """
    Rebuild list takes the current text file, the searchFor list and an option toRemove.
    toRemove just stores line numbers of any lines we need to remove.
    The subroutine goes line by line through the text file passed to it (in a list)
    Then for each line, checks if anything in the searchFor list needs replaced.
    If it is happy, it will append it to the new text file list.
    """
    svgfile2 = []
    for i in range(0, len(svgfile)):                            #iterate through the text file
        for count in range(0, len(searchFor)):                  #Iterate through each of the words to be replaced
            if i in searchFor[count][2]:                        #Checks if this line is being requested
                for x in range(0, len(searchFor[count][2])):    #If it is, lets iterate through and find the exact reference
                    if searchFor[count][2][x] == i:             #Checks if it is the exact reference
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
    """
    Removes blank lines from text file
    """
    toRemove = []
    for i in range(0, len(svgfile)):
        for cl in range(0, len(clues)):
            found = svgfile[i].find(clues[cl])
            if found != (-1):
                toRemove.append(i)
    return toRemove

def convertStringToList(string):
    """
    Really simply converts a string to a list
    """
    theList = []
    for x in range(0, len(string)):
        theList.append(string[x])
    return theList

def convertListToString(theList):
    """
    Really simply converts a list to a string
    """
    string = ""
    for x in range(0, len(theList)):
        string = string + theList[x]
    return string

def removeEndBit(theLine, toRemove):
    """
    Removes characters at the end of any lines
    """
    theLine = convertStringToList(theLine)
    for i in range(len(theLine) -1, 0, -1):
        if theLine[i] == toRemove:
            theLine.pop(i)
            break
    return convertListToString(theLine)


def main(filename):

    print("Now working on " + filename)
    svgfile = getTextFile(filename)                             #Converts text file to a list of lists
    svgfile = removeN(svgfile)                                  #Removes \n (a special escape character that means newline)
    svgfile = blankLineRemover(svgfile)                         #Removes all blank lines from the file, makes easier to work with
    linesToAvoid = multiLineCommentTracker(svgfile)             #Adds lines to be ignored by the replacers, mainly just multiline comments
    print("Searching through file, this may take a while")

    clues = [["elif", "~~~"],]

    for i in range(0, 6):
        svgfile = wordReplacer(svgfile, linesToAvoid, clues)    #Replaces every use of elif with ~~~~ to avoid confusing the indentation finder laster

    searchfor =  indentationFinder(svgfile, linesToAvoid)       #Traces indentation through the file. It finds the start and end of structures, e.g. functions, loops etc. Returns a list containing locations of all of the items being searched for in the file.

    svgfile = rebuildList(svgfile, searchfor, removeLines(svgfile, ["debug", "info", "warning", "#print"])) #Rebuilds the new text file based off the changes from indentationFinder
    linesToAvoid = multiLineCommentTracker(svgfile)




                                                                #All these functions simply replace words with new words. They must be repeated as the wordReplacer function only counts the first find on a line.
    for x in range(0, 10):
        svgfile = wordReplacer(svgfile, linesToAvoid, [["def", "FUNCTION"], ["print", "OUTPUT"], ["self.", " "], ["return", "RETURN"], ["else:", "ELSE:"], ["==", "|"], ["if", "IF"], ["or", "OR"], ["and", "AND"],["and", "AND"], ["class", "CLASS"]  ])
    for x in range(0, 5):
        svgfile = wordReplacer(svgfile, linesToAvoid, [["self.", " "],], False)
    for x in range(0, 10):
        svgfile = wordReplacer(svgfile, linesToAvoid, [["=", "<-"], ["~~~", "ELSEIF"]])
    for x in range(0, 10):
        svgfile = wordReplacer(svgfile, linesToAvoid, [["|", "="],])

    svgfile = wordReplacer(svgfile, linesToAvoid, [["OUTPUT(", "OUTPUT ", ")"]], False, True)


    svgfile = wordReplacer(svgfile, linesToAvoid, [["<- ?", "= ?"]])
    svgfile = wordReplacer(svgfile, linesToAvoid, [["<- ?", "= ?"]])


    writeTextFile(svgfile, filename)                            #Finally write the new text file!




#-----------------------------------Main program----------------------------------------
#-----------------------------------Main program----------------------------------------
#-----------------------------------Main program----------------------------------------



main(pythonFile)


print("")
print("")
print("----------------")
print("Process complete")
print("----------------")