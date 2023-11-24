import os
import sys
import rpyc

def get_file(master, sourceDir):
    pass
    # files = master.get_files()

def get_all_files(master):
    files = master.get_files()
    print(files)

def put_file(master, sourceFile):
    size = os.path.getsize(sourceFile) # get size
    with open(sourceFile, "rb") as f:
        file_blocks = master.write(f.name, size, f.read()) # call server function
        
    print("blocks: ", file_blocks)  # {file,txt, [uuid1, uuid2, ...]}


def main(args):
    os.path.join
    c = rpyc.connect("localhost", 18861)
    master = c.root
    
    if args[0] == "get":
        get_all_files(master) # get source.txt 

    elif args[0] == "put":
        put_file(master, args[1]) # put source.txt
    else:
        return "try 'put srcFile destFile OR get file'"

    # print(c.root.create_file(f))
    # the service is exposed as the root object of the connection
    # print(c.root)
    # print(c.root.listdir("/Users"))

if __name__ == "__main__":
    main(sys.argv[1:])
