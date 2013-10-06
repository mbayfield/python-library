"""
Filename: 7zip-backups.py

Description:
    Take a back of a virtuozzo container.
    
    The zipBackup function:
    1.  Finds the most recent full backup of the vz container (which is created on Saturday)
    2.  Find the database backup created today
    3.  Creates a 7z file using the password provided.
    4.  Checks if the backup files already exists and deletes them.

Author: Mark Bayfield
Date: 2009-03-02

Revisions:

"""
import os, calendar, datetime
from os.path import join
def zipBackup( directory, zipFile, strToFind, type ):
    
    # remove the files first if they exist
    if os.path.exists(zipFile) :
        os.remove(zipFile)
    
    # set the 7zip password
    pwd = ''
    
    for root, dirs, files in os.walk( directory ):
        if ( type == 'vz' ) :
            for name in dirs:
                file = join( directory, name )
                if ( str(name).find( strToFind ) != -1 ) :
                    os.popen("\"C:\\Program Files\\7-Zip\\7z.exe\" a -t7z -p"+pwd + " " + zipFile + " " + file ).readlines()
                
        elif ( type == 'sql' ) :
            for name in files:
                file = join( directory, name )
                if ( str(name).find( strToFind ) != -1 ) and ( str(name).find( 'bak' ) != -1 ):
                    os.popen("\"C:\\Program Files\\7-Zip\\7z.exe\" a -t7z -p"+pwd + " " + zipFile + " " + file ).readlines()
                
    return 


if __name__ == "__main__":
    
    # Get today's date
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    
    # look for the most recent Saturday
    saturday = today

    while saturday.weekday() != calendar.SATURDAY:
        saturday -= oneday
    
    vzStrToFind = saturday.strftime("%Y%m%d")
    sqlStrToFind = datetime.date.today().strftime("%Y%m%d")
    
    zipBackup( '[vz-filepath]', '[destinationfile.7z]', vzStrToFind, 'vz' )
    zipBackup( '[db server path]', '[database-destinationfile.7z]', sqlStrToFind, 'sql' )
