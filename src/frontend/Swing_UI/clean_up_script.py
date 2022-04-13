import os

'''
Removes all the generated ABC files in the directory.
'''

dir_name = os.getcwd()
list_of_files = os.listdir(dir_name)


for file in list_of_files:
    os.remove(os.path.join(dir_name, file)) if file.endswith(".abc") else None
