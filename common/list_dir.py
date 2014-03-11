import os
Home = "./"
list_dir = os.listdir(Home)
for filename in list_dir:
    file_route = os.path.join(Home, filename)
    os.system("ls "+file_route)
