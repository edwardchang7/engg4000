import os


# Function to convert a single .mxl file into .abc
# The output file will be generated in the "converted_compositions" directory
def convert(input_file, output_path=os.getcwd()):
    base_name = os.path.basename(input_file)
    os.system("python xml2abc.py " + input_file + " -o converted_compositions " + output_path + "/" + base_name)


# Function that will convert all of the .mxl files in "to_convert" directory
# The output files will be generated in the "converted_compositions" directory
def batch_convert():
    files_to_convert = os.listdir("to_convert")
    for file in files_to_convert:
        convert("to_convert/" + file, "converted_compositions")


if __name__ == "__main__":
    os.chdir("src/backend/mxl_to_abc")
    batch_convert()
