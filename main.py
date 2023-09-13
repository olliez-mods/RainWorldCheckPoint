import pathlib
import shutil
import sys
from datetime import datetime
import subprocess
import os





def ext():
    input("...")
    sys.exit()


print("\n")

appdataRoaming = os.environ.get("APPDATA")
appdataLocalLow = os.path.normpath(appdataRoaming + "\\..\\LocalLow\\Videocult\\Rain World\\")

rainWorldSaveDir = pathlib.Path(appdataLocalLow)

if(not rainWorldSaveDir.exists()):
    print("We could not find \""+str(rainWorldSaveDir)+"\" please make sure you have Rain World installed")
    ext()

savsDir = rainWorldSaveDir.joinpath("RWCPsavs")
backupsDir = savsDir.joinpath("backups")
currSavNameDir = rainWorldSaveDir.joinpath("RWCPselectedSav.txt")
currSavFileDir = rainWorldSaveDir.joinpath("sav")


print("Using path:", rainWorldSaveDir, "\n")

# Check if all requird directories and files exist int he rain world 

# Check for sav directory
if (not savsDir.is_dir()):
    usrIn = input("\"" + str(savsDir) + "\" does not exist, should it be created? (Y/N): ")
    if(usrIn.lower() != "y"):
        print("Quitting...")
        ext()
    savsDir.mkdir(parents=False, exist_ok=False)
    backupsDir.mkdir(parents=False, exist_ok=False)

# check if backups directory exists
if (not backupsDir.is_dir()):
    usrIn = input("\"" + str(backupsDir) + "\" does not exist, should it be created? (Y/N): ")
    if(usrIn.lower() != "y"):
        print("Quitting...")
        ext()
    backupsDir.mkdir(parents=False, exist_ok=False)   
    
# Check for currName directory, it will set current as default
if (not currSavNameDir.is_file()):
    usrIn = input("\"" + str(currSavNameDir) + "\" does not exist, should it be created? (Y/N): ")
    if(usrIn.lower() != "y"):
        print("Quitting...")
        ext()
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
    print("\nMain Menu (Use \"help <number>\" for more info on a command):")
    print("1 - Load a save")
    print("2 - Copy selected save")
    print("3 - Delete a save")
    print("4 - Override Selected With A Stored Save")
    print("5 - Open Rain World folder\n")

def isValidSave(saveName):
    l = getSavesNames()
    return (saveName in l)

def clear():
    print("\n"*100)

def pause(msg = "\n -> Press \"Enter\" to continue <-"):
    input(msg)

# loads a save from the savs folder into rain world folder
def loadSave(saveName):
    if(not isValidSave(saveName)):
        print("not valid save in loadSave()")
        ext()

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
        ext()
    
    savsDir.joinpath(saveName + ".RWCPsav").unlink()

# delete current save and copy another save into it
def loadBackup(saveName):
    if(not savsDir.joinpath(saveName + ".RWCPsav").is_file()):
        print("Error in loadbackup() we just saved your life ;)")
        ext()
    # delete current save
    rainWorldSaveDir.joinpath("sav").unlink()

    # copy and select new save
    shutil.copy2(savsDir.joinpath(saveName + ".RWCPsav"), rainWorldSaveDir.joinpath("sav"))



# Now we are sure that all the needed folders and files are here, time to start the program for real
while(True):
    printMainMenu()
    usrIn = input("Select an option: ")

    match usrIn:
        case "help 1":
            print("\n[Load A Save] This command will switch out the selected save, with one of your choosing.")
            print("The old selected save will be put into storage.")
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
        case "help 2":
            print("\n[Copy Selected Save] This command will copy whatever save is currently selected, and will")
            print("create a copy of it. You will be asked for a name for the copy and")
            print("the new copy will be put in storage.")
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
        case "help 3":
            print("\n[Delete A Save] This command will delete a save that's in storage. You cannot delete a save if it")
            print("is currently selected.")
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
        case "help 4":
            print("\n[Override Selected] This command will replace the selected save with a copy of a save in storage, while keeping")
            print("the name of the current save.")
            print("In other words, we are loading a \"backup\" into our selected save.")
            print("Note: You should not see a difference after running this command as the names will stay unchanged.")
        case "4": # replace current save with backup copy
            saveToReplaceCurrent = input("What save would you like to overide \"" + getCurrSaveName() + "\" with?:")
            if(not isValidSave(saveToReplaceCurrent)):
                print("\"" + saveToReplaceCurrent + "\" is not a valid option")
                pause()
                clear()
                continue
            loadBackup(saveToReplaceCurrent)
            print("Overided selected save with \"" + saveToReplaceCurrent + "\" (Name is kept)")
        case "help 5":
            print("\nThis command will open file explorer to your given Rain World path.")
            print("This is usefull if you need to access the backups we create.")
            print("Note: Rain World handles its own backups so please don't use that folder, use")
            print("the backups folder locased in \"RWCPsavs\\backups\".")
        case "5":
            print("\nOpening Rain World Folder in file explorer (\"" + str(rainWorldSaveDir) + "\")")
            print("Note: If you are trying to restore a backup of you saves, they can be found in \"RWCPsavs\\backups\"")
            subprocess.Popen('explorer ' + str(rainWorldSaveDir))
        case _:
            print("That isn't an option")
    pause()
    clear()