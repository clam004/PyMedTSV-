# get list of directories 
dirs = get_immediate_subdirectories(Population_path)
len(dirs)
# create the txt file with header inside

DIMENSION_NAME = "note.txt"
IOPheader = stringheader 

for MRN in dirs:
    
    textpath = Population_path + str(MRN) + '/' + DIMENSION_NAME
    if os.path.exists(Population_path + str(MRN)) and not os.path.exists(textpath):
    
        # create add the file 
        file = open(textpath, "w")
        file.write(IOPheader + "\n") # remember to use the \n to go to next line 
        file.close()
