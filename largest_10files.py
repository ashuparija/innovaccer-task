import os
import sys

# Import the necessary modules
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue


# add more directories to the follwing list to search them
# NOTE: Add paths relative to home directory
allowed_dirs = ['Downloads']

# Adding paths to allowed directories using the command line arguments
if not len(sys.argv) == 1:
    directory_list = sys.argv[1:]
    for directory in directory_list:
        allowed_dirs.append(directory)

# maximum number of files that we need
MAX_FILES = 10

# find the complete path for the home and store it in home_dir
home_dir = os.path.expanduser('~')

# modifying allowed directories to store full paths
allowed_dirs = ['{}/{}'.format(home_dir, d) for d in allowed_dirs]

# Define priorityQueue to store MAX_FILES number of largest files
largest_files = PriorityQueue(maxsize=MAX_FILES)

def process(directory):
    """
    Recieves path of a directory as parameter
    Iterates though all the files and folders inside the path 
    and puts the largest files in the priorityQueue
    Appends the paths of the folders to allowed_dirs
    """
    global largest_files
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
            # get the size of the file
            file_size = os.path.getsize(content_path)
            # check if the priorotyQueue is full
            if largest_files.full():
                smallest = largest_files.get()
                # check if smallest element of priorityQueue has smaller size than considered file and pop it
                if smallest[0] < file_size:
                    largest_files.put((file_size, content_path))
                else:
                    largest_files.put(smallest)
            else:
                largest_files.put((file_size, content_path))

        else:
            # append the directory path to the allowed dirs list for the recursive search
            allowed_dirs.append(content_path)

def largest():
    """
    Calls process recursively by using allowed_dirs list as a stack
    Returns the MAX_FILES number of largest files as priorityQueue
    """
    global largest_files
    while len(allowed_dirs):
        process(allowed_dirs.pop())

    return largest_files

def main():
    """
    Calls largest and obtains the largest files priorityQueue
    Converts the priorotyQueue into list of tuples and prints
    filename and its size in Dessending order
    """
    pq = largest()
    file_paths = []
    while not pq.empty():
        file_paths.append(pq.get())
    file_paths = file_paths[::-1]
    #print('Filename - Size')
    for file_path in file_paths:
        print('filepath : {} - filesize : {}MB'.format(file_path[1], int(file_path[0]/(1024*1024))))

if __name__ == '__main__':
    main()
