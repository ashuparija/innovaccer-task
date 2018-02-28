import os
import sys

# take the directory to be sorted and the desination as command line arguments
if len(sys.argv) == 3:
    SOURCE = sys.argv[1]
    TARGET = sys.argv[2]
else:
    print("Please prvide the source and target directory paths as command line arguments respectively. Eg: python sorted.py /home/<username>/Desktop /home/<username>/Downloads") 
    exit(1)

content_dict = {}

def process(directory):
    """
    Takes the source directory as input parameter.
    Forms the content_dict which is a dictionary of keys as target directories 
    and the values as the files to be put there.
    """
    global content_dict
    # form the list of all files and directories inside the given path
    contents = os.listdir(directory)
    
    # iterate through each item in contents
    for content in contents:
        content_path = '{}/{}'.format(directory, content)
        # check if the path formed is a file
        if os.path.isfile(content_path):
            # check if the path is of symlink
            if os.path.islink(content_path):
                # skip rest of the statements and move the control back to the start of the loop
                continue
            
            # getting the filename from the complete path
            _, filename = os.path.split(content_path)
            # finding the name and extension of the file
            name, extension = os.path.splitext(filename)
            #remoing the extra . from the extension
            extension = extension.upper()[1:]
            if content_dict.get(extension):
                content_dict[extension].append(content_path)
            else:
                content_dict[extension] = [content_path]

def organize(content_dict):
    """
    Takes dictionary of keys as target directories and the values as the files 
    to be put there as a parameter.
    Using the content_dict parameter it moves the files from source to the 
    target folder.
    """
    for ext, file_paths in content_dict.items():
        # create target path
        target_path = '{}/{}'.format(TARGET, ext)
        if not os.path.isdir(target_path):
            # create target directory if doesn't already exists
            os.makedirs(target_path)
        for file_path in file_paths:
            # getting the filename from the complete path
            _, filename = os.path.split(file_path)
            # moving the files to the target folder
            os.rename(file_path, '{}/{}'.format(target_path, filename))

def sorter():
    """
    Calls process function to form the dictionary of keys as target directories
    and the values as the files to be put there.
    Calls organise to move the files form source to target folder
    """
    global content_dict
    process(SOURCE)
    organize(content_dict)

if __name__ == '__main__':
    sorter()
