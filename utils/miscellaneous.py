from pathlib import Path
import os
import numpy as np

def save_to_txt_file(lines_to_write, destination_path):
    '''
    function to save line to a text file

    Parameters: 
    - lines_to_write (str): list of str(lines)
    - destination_path (str): destination path of the text file to be saved

    Returns: 
    - True (boolean): if saved sucessfully
    - False (boolean): if failed to save sucessfully
    
    '''
    destination_path_obj = Path(destination_path)
    # Ensure the file has a .txt extension
    if destination_path_obj.suffix != '.txt':
        destination_path_obj = destination_path_obj.with_suffix('.txt')
    
    try:
        with open(destination_path_obj, 'w') as file:
            for line in lines_to_write:
                file.write(line + '\n')
        print(f"Sucessfully saved the lines to the file: {destination_path_obj.name}")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False


def get_filenames_of_extention(folder_path, extention='.jpg'):
    file_names = []
    # Check if the folder path exists
    if os.path.exists(folder_path):
        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            # Check if the file has a .jpg extension
            if filename.lower().endswith(extention):
                # print(filename.lower())
                # Add the file to the list of jpg_files
                file_names.append(filename)
    else:
        print("Folder path does not exist.")
        return False, file_names
    return True, file_names


def get_all_filenames(folder_path): 
    file_names = []
    # Check if the folder path exists
    if os.path.exists(folder_path):
        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
                # Add the file to the list of jpg_files
                file_names.append(filename)
    else:
        print("Folder path does not exist.")
    return file_names


def path_valid(path):
    '''
    Check the validity of the given path.
    
    Parameters:
    - path (str): The path to check.
    
    Returns:
    - bool: True if the path is valid, False otherwise.
    '''
    path_obj = Path(path)
    
    if not path_obj.exists():
        print(f"The path '{path}' does not exist.")
        return False
    
    if not os.access(path, os.R_OK):
        print(f"The path '{path}' is not readable.")
        return False
    
    return True

# Function to rotate a point (x, y) around origin (0, 0) by angle (in degrees)
def rotate_point(x, y, angle):
    angle_rad = np.deg2rad(angle)
    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)
    new_x = x * cos_theta - y * sin_theta
    new_y = x * sin_theta + y * cos_theta
    return new_x, new_y