# this is a script to arrange the images in different folders 

import os
import shutil
import sys

from crop import get_filenames_of_extention

def move_files(extention, source_folder, dest_folder_base, batch_size=100):
    # Ensure the destination base folder exists
    if not os.path.exists(dest_folder_base):
        os.makedirs(dest_folder_base)
    
    # Get a list of all files in the source folder
    files = get_filenames_of_extention(source_folder, extention)
    
    # Sort files to maintain a consistent order
    files.sort()
    
    for file in files: 
        print(file)

    total_number_of_files = len(files)
    print(f'{type(total_number_of_files)} total_number_of_files, size={total_number_of_files}')
    print(type(batch_size))

    # Process files in batches
    for i in range(0, total_number_of_files, batch_size):
        batch_files = files[i:i+batch_size]
        batch_folder = os.path.join(dest_folder_base, f'batch_{i//batch_size + 1}')
        
        # Create batch folder if it does not exist
        if not os.path.exists(batch_folder):
            os.makedirs(batch_folder)
        

        error_occured = False
        # Move each file in the batch to the new batch folder
        for file_name in batch_files:
            source_path = os.path.join(source_folder, file_name)
            dest_path = os.path.join(batch_folder, file_name)
            try:
                shutil.move(source_path, dest_path)
                print(f'Moved {file_name} to {batch_folder}')
            except Exception as e:
                print(f'Error moving {file_name} to {batch_folder}: {e}')
                error_occured = False
                
        
        if not error_occured:
            print(f'Moved {len(batch_files)} files to {batch_folder}')

def move_jpgs(source_folder, dest_folder_base, batch_size=100):
    move_files('.jpg', source_folder=source_folder, dest_folder_base=dest_folder_base, batch_size=batch_size)

def get_script_directory():
    # Get the absolute path of the script
    script_path = os.path.abspath(__file__)
    # Get the directory of the script
    script_directory = os.path.dirname(script_path)
    return script_directory

def main():
    print("Arguments you entered are: ")
    for index, arg in enumerate(sys.argv):
        print(f'{index+1}: {arg}')
    # moving_files_of_extention '.jpg' 'source_path' 'destination_path' 'batchsize'
    if len(sys.argv)!=5:
        print("number of args should be 5.")
        sys.exit(1)

    # Call the function
    move_files(extention=sys.argv[1], source_folder=sys.argv[2], dest_folder_base=sys.argv[3], batch_size=int(sys.argv[4]))

if __name__ == "__main__":
    main()