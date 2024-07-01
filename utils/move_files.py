import os
import shutil
from pathlib import Path
from miscellaneous import get_filenames_of_extention

def move_imgs_having_labels(labels_folder, source_folder, destination_folder, extention='.jpg'):
    '''
    Function to move all the files having the specified extention to the destination folder

    Parameters: 
    - labels_folder (str): path of the folder that has the labels
    - source_folder (str): path to the source folder
    - destination_folder (str): path to the destination folder (where the files are to be moved)
    - extention: move all the files with this extension

    Returns: 
    - True: if successful
    - False: if unsuccessful
    '''
    status_label, filenames_with_ext = get_filenames_of_extention(labels_folder, extention='.txt')

    # Remove the extension of the file name
    if status_label:
        lablenames_without_ext = [Path(filename).stem for filename in filenames_with_ext]
    else:
        print(f'Error in getting filenames of labels from {labels_folder}')
        return False

    print(f"Label filenames without extension: {lablenames_without_ext}")

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Move image files
    for labelname in lablenames_without_ext:
        image_filename = f"{labelname}{extention}"
        source_path = Path(source_folder) / image_filename
        destination_path = Path(destination_folder) / image_filename

        if source_path.exists():
            shutil.copy(str(source_path), str(destination_path))
            print(f"Copied {image_filename} to {destination_folder}")
        else:
            print(f"Image file {image_filename} not found in {source_folder}")

    return True

    

def main():
    source_folder = 'dataset\\bagmati\\bagmati-patch-1-cropped\\Bagmati patch 1-waste2\\bagmati patch 1 waste 2 batch_1_to_5'
    labels_folder = "dataset\\labelTxt\\bagmati-patch1-waste1"
    destination_folder = 'dataset\\images'
    extention = '.jpg'

    move_imgs_having_labels(labels_folder, source_folder, destination_folder, extention)

if __name__ == "__main__":
    main()
        

