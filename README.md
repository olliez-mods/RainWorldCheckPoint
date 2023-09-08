# RainWorldCheckPoint
This Python program allows you to easily change the sav file for Rain World.

How to use:
Make sure Python is installed on your system and is working

IMPORTANT:
  Make sure to replace \<PATH HERE\> with the path to your Rain World folder (not in the Steam folder) it should be something like
  "C:\Users\[USERHERE]\AppData\LocalLow\Videocult\Rain World"
  
  When you run the bat script or run main.py from a console for the first time it will prompt you to create some files and folders, make sure the path to these items is correct
  
  Once you get into the main menu there are 3 options:
  Load a save:
    This will change your selected save to whichever one you choose.
  
  Copy selected save:
    This will create a copy of whatever save you have selected, you will be prompted for a name for this copy, and it will then be placed in storage with your other saves (the current save will STAY selected)
  
  Delete a save:
    RISKY This will delete a save from storage.


Backup Folder:
  In your Rain World folder (not Steam one) there should be a new folder called "RWCPsavs" this is where all the saves are stored when not selected. 
  Inside that folder, you will find another folder called "backups", each time you run main.py (from the .bat file or console) it will create a backup with 
  the date (with the format YYYY-MM-DD [HH-MM-SS]) inside each backup you can see all your saves
