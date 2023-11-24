import os
import sys
import rpyc

def get_file(master, sourceDir):
    pass
    # files = master.get_files()

def put_file(master, sourceFile, destFile):
    size = os.path.getsize(sourceFile) # get size
    with open(sourceFile, "rb") as f:
        blocks = master.write(f.name, size, f.read()) # call server function
    print("blocks: ", blocks)

def main(args):
    os.path.join
    c = rpyc.connect("localhost", 18861)
    master = c.root
    
    if args[0] == "get":
        get_file(master, args[1]) # get source.txt 
    elif args[0] == "put":
        put_file(master, args[1], args[2]) # put source.txt dir/dest.txt
    else:
        return "try 'put srcFile destFile OR get file'"

    # print(c.root.create_file(f))
    # the service is exposed as the root object of the connection
    # print(c.root)
    # print(c.root.listdir("/Users"))

if __name__ == "__main__":
    main(sys.argv[1:])
