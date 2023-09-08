import pathlib
import shutil
import sys
from datetime import datetime

file = open("RainWorldSaveDir.txt", "r")
rainWorldSaveDir = file.read()
file.close()

rainWorldSaveDir = pathlib.Path(rainWorldSaveDir)
savsDir = rainWorldSaveDir.joinpath("RWCPsavs")
backupsDir = savsDir.joinpath("backups")
currSavNameDir = rainWorldSaveDir.joinpath("RWCPselectedSav.txt")
currSavFileDir = rainWorldSaveDir.joinpath("sav")


print("\n")

if(not rainWorldSaveDir.is_dir()):
    print("Path does not exist")
    sys.exit()
print("Using path:", rainWorldSaveDir, "\n")

# Check if all requird directories and files exist int he rain world 

# Check for sav directory
if (not savsDir.is_dir()):
    usrIn = input("\"" + str(savsDir) + "\" does not exist, should it be created? (Y/N): ")
    if(usrIn.lower() != "y"):
        print("Quitting...")
        sys.exit()
    savsDir.mkdir(parents=False, exist_ok=False)
    backupsDir.mkdir(parents=False, exist_ok=False)

# check if backups directory exists
if (not backupsDir.is_dir()):
    usrIn = input("\"" + str(backupsDir) + "\" does not exist, should it be created? (Y/N): ")
    if(usrIn.lower() != "y"):
        print("Quitting...")
        sys.exit()
    backupsDir.mkdir(parents=False, exist_ok=False)   
    
# Check for currName directory, it will set current as default
if (not currSavNameDir.is_file()):
    usrIn = input("\"" + str(currSavNameDir) + "\" does not exist, should it be created? (Y/N): ")
    if(usrIn.lower() != "y"):
        print("Quitting...")
        sys.exit()
    currSavNameDir.touch(exist_ok=False)
    file = open(currSavNameDir, "w")
    file.write("default")
    file.close()


def getCurrSaveName():
    file = open(currSavNameDir, "r")
    saveName = file.read()
    file.close()
    return saveName

def getSavesNames():
    l = savsDir.glob('*.RWCPsav')
    itemsNames = []
    for item in l:
        itemName = item.name.split(".")[0]
        itemsNames.append(itemName)
    return itemsNames


# =====================
# Create backup, very important

def createBackup():
    # we assume that all required files and folders exist
    currDate = str(datetime.now().strftime("%Y-%m-%d [%H-%M-%Ss]"))
    newBackupDir = backupsDir.joinpath(currDate)
    newBackupDir.mkdir(parents=False, exist_ok=False)
    names = getSavesNames()
    currSaveName = getCurrSaveName()

    for fileName in names: # copy saves in storage
        shutil.copy2(savsDir.joinpath(fileName + ".RWCPsav"), newBackupDir)
    shutil.copy2(currSavFileDir, newBackupDir.joinpath(currSaveName + ".RWCPsav")) # copy main file
        
createBackup() # we have this in a function so we dont pollute the main function with variables


# ===================




def printMainMenu():
    print("Saves:")
    print("-  " + getCurrSaveName() + " *Selected*")
    names = getSavesNames()
    for n in names:
        print("-  " + n)
    print("\nMain Menu")
    print("1 - Load a save")
    print("2 - Copy selected save")
    print("3 - Delete a save (Can't be selected save)\n")

def clear():
    print("\n"*100)

def pause(msg = "\n -> Press \"Enter\" to continue <-"):
    input(msg)

def isValidSave(saveName):
    l = getSavesNames()
    return (saveName in l)


# loads a save from the savs folder into rain world folder
def loadSave(saveName):
    if(not isValidSave(saveName)):
        print("not valid save in loadSave()")
        sys.exit()

    # Get name of current save
    currSaveName = getCurrSaveName()

    # now copy it into the savs folder
    shutil.move(currSavFileDir, savsDir.joinpath(currSaveName + ".RWCPsav"))

    #now move the new sav into the main dir
    shutil.move(savsDir.joinpath(saveName + ".RWCPsav"), rainWorldSaveDir.joinpath("sav"))

    #update txt file to reflect new name
    file = open(currSavNameDir, "w")
    file.write(saveName)
    file.close()
   
def duplicateSelectedSave(newName):
    #copy into sav folder with new name
    shutil.copy2(currSavFileDir, savsDir.joinpath(newName + ".RWCPsav"))

def deleteSave(saveName):
    if(not savsDir.joinpath(saveName + ".RWCPsav").is_file()):
        print("Error in deleteSave() we just saved your life ;)")
        sys.exit()
    
    savsDir.joinpath(saveName + ".RWCPsav").unlink()


 

# Now we are sure that all the needed folders and files are here, time to start the program for real
while(True):
    printMainMenu()
    usrIn = input("Select an option: ")

    if(not usrIn.isdigit()):
        clear()
        continue

    match usrIn:
        case "1": # Load a save
            selectedSave = input("What save would you like to load?: ").lower()
            if (not isValidSave(selectedSave)):
                print("\"" + selectedSave + "\" is not valid")
                pause()
                clear()
                continue
            # if the save is valid we want to load it
            loadSave(selectedSave)
            print("\n\tLoaded \"" + selectedSave + "\"")
        case "2": # Copy current save
            currSaveName = getCurrSaveName()
            newSaveName = input("What should we call the copy?: ").lower()
            if(newSaveName == currSaveName): # if they both have the same name
                print("You can't name it the same thing")
                pause()
                clear()
                continue
            if(isValidSave(newSaveName)): # if we already have a save of that name
                confirm = input("You already have a save called \"" + newSaveName + "\", this will overwrite it, are you sure? (Y/N): ").lower()
                if(confirm != "y"):
                    print("\n\tOperation cancled")
                    pause()
                    clear()
                    continue
            duplicateSelectedSave(newSaveName)
            print("\nCreated a copy of \"" + currSaveName +  "\" called \"" + newSaveName + "\"")
        case "3": # delete a save
            saveToRemove = input("Which save should we remove?: ").lower()
            if(not isValidSave(saveToRemove)):
                print("\"" + saveToRemove + "\" isn't a valid save")
                pause()
                clear()
                continue
            confirm = input("Are you sure you want to delete \"" + saveToRemove + "\"? (Y/N): ").lower()
            if(confirm != "y"):
                print("\n\tCanled")
                pause()
                clear()
                continue
            deleteSave(saveToRemove) # delete save, risky biusness
            print("\n\tDeleted \"" + saveToRemove + "\"")
        case _:
            print("That isn't an option")
    pause()
    clear()