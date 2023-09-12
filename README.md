# RainWorldCheckPoint
This Python program allows you to easily change the sav file for Rain World.
</br>
## How to run:
  Make sure Python is installed on your system and is working
</br>

## IMPORTANT:
  Make sure to replace \<PATH HERE\> with the path to your Rain World folder (not in the Steam folder) it should be 
    something like "C:\Users\[USERHERE]\AppData\LocalLow\Videocult\Rain World"


## How to use

When you run the bat script or run main.py from a console for the first time it will prompt you to create some files and folders, Make sure the path to these items is correct
  
  Once you get into the main menu there are 3 options:
  
  ### Load a save:
  This will change your selected save to whichever one you choose.
  <br>

  ### Copy selected save:
  This will create a copy of whatever save you have selected, you will be prompted for a name for 
  this copy and will then be placed in storage with your other saves (the current save will STAY selected)
  <br>

  ### Delete a save:
  RISKY This will delete a save from storage.
  <br>

  ## Load save into selected
  Warning This will override the selected save
  This command allows you to copy a backup into the selected save, overriding the selected save with one in storage (the name is kept though to prevent confusion).
  <br>

## Backup Folder:
  In your Rain World folder (not Steam one) there should be a new folder called "RWCPsavs" This is where all the saves are stored when not selected. Inside that folder, you
     will find another folder called "backups", Each time you run main.py (from the .bat file or console) it will create a backup with the date (with the format YYYY-MM-DD [HH-MM-SS]) 
    Inside each backup, you can see all your saves
