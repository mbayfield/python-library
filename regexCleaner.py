#!/usr/bin/env python
##################################################################################
#regexCleaner.py
# Author: Mark Bayfield
# Date: 2009-08-28
# 
# Cleans HTTrack files for use in directory compares.
#
# Usage:
#   python regexCleaner.py dirname
#
#   Point this at a directory of HTTrack files that need cleaning
#   and it removes all the common elements to make it a clean compare for changes.
##################################################################################
import sys, os, re, string

# pupulate and return 'fileslist[]' with all files inside 'dir' matching 'regx'
def make_files_list(dir, regx):
    
    # compile the search regexp
    cregex=re.compile(regx)
    bad=re.compile('.svn')
    # initialize the file list
    fileslist = []
    
    for root, dirs, files in os.walk(dir, topdown=False):
        
        for name in files:
           
            if cregex.search(name):
                if not bad.search(name):
                    path = os.path.join(root, name)
                    fileslist.append(path)
                    

    # return the file list
    return fileslist[:]
    
def replace_in_files( fileslist, searchregx ):
    
     # loop on all files
    for xfile in fileslist:
        
        # open file for read  
        readlines=open(xfile,'r').readlines()
        # intialize the list counter
        listindex = -1

        # search and replace in current file printing to the user changed lines
        for currentline in readlines:

            # increment the list counter
            listindex = listindex + 1
            
            for cursearchregx, replacestring in searchregx.iteritems(): 
                
                cregex=re.compile( cursearchregx )
                # if the regexp is found
                if cregex.search(currentline):
                     # make the substitution
                    f=re.sub(cursearchregx,replacestring,currentline)
                    
                    # update the whole file variable ('readlines')
                    readlines[listindex] = f
        
        # open the file for writting  
        write_file=open(xfile,'w') 

        # overwrite the file  
        for line in readlines:
            write_file.write(line)

        # close the file
        write_file.close()
    

# main function
def main():
   
    
    if len(sys.argv) < 2:

        print '\nUsage:'
        print 'python regexCleaner.py dirname'

        sys.exit(1)
        
    # The regex and replacements
    searchregx1 = {
        'cell[a-z]+ing="0"'                                             :       '',
        'content_[0-9]+'                                                :       '',
        'FooterGallery/[a-zA-Z0-9\_]+.jpg'                              :       'FooterGallery/evr_sml.jpg',
        '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'  :       '',
        'captcha_img(-)?[0-9]*.png'                                     :       'captcha_img.png',
        'FooterGallery/[a-z\_]+.jpg'                                    :       'FooterGallery/evr_sml.jpg',
        'HeaderImages/[a-z\_]+.jpg'                                     :       'HeaderImages/Gas.jpg',
        'id="[a-z]+_[\-0-9]+"'                                          :       'id=""',
        '<input value=".{32}" type="hidden" name="SecurityKey">'        :       '<input value="" type="hidden" name="SecurityKey">',
        '<input value=".{32}" type="hidden" name="VerifyKey">'          :       '<input value="" type="hidden" name="VerifyKey">'
    }
    
    # These needs to be run on its own at the end
    searchregx2 = { 'table[\s]+': 'table '}
    searchregx3 = { '"[\s]+>': '">' }
    
    # Make a list of all the html files in the directory
    fileslist = make_files_list(sys.argv[1], 'html')
    
    # run the regex against the file list
    replace_in_files( fileslist, searchregx1 )
    replace_in_files( fileslist, searchregx2 )
    replace_in_files( fileslist, searchregx3 )

if __name__ == '__main__':
    main()