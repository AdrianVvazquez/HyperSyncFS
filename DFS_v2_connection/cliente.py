import rpyc

c = rpyc.connect("localhost", 18861)

# with open("new_doc2.txt", "x") as f:
#     f.write("Halo\n")

# the service is exposed as the root object of the connection
# print(c.root)
# print(c.root.create_file(f))
# print(c.root.get_files())
print(c.root.listdir("/Users"))
