import os


filename = 'C:/Users/njvtwk/AppData/Roaming/JetBrains/PyCharmCE2022.3/scratches/category_list.txt'


def check_filename_existance(filename: str) -> bool:
    

    # Check if the file exists
    if os.path.exists(filename):
        return True
        """
        print(f"The file {filename} exists.")
    # Check if the file is readable
        if os.access(filename, os.R_OK):
            print(f"The file {filename} is readable.")
        else:
            print(f"The file {filename} is not readable.")
            """
    else:
        return False
        #print(f"The file {filename} does not exist.")