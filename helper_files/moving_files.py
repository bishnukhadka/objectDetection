# this is a script to arrange the images in different folders 

import os
import shutil

from crop import get_jpg_filenames

def move_images(source_folder, dest_folder_base, batch_size=100):
    # Ensure the destination base folder exists
    if not os.path.exists(dest_folder_base):
        os.makedirs(dest_folder_base)
    
    # Get a list of all files in the source folder
    files = get_jpg_filenames(source_folder)
    
    # Sort files to maintain a consistent order
    files.sort()
    
    for file in files: 
        print(file)

    print(len(files))

    # Process files in batches
    for i in range(0, len(files), batch_size):
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


if __name__ == "__main__":
    # Define your source and destination folders here
    source_folder = '/home/bishnu/Documents/objectDetection/cropped_images'
    dest_folder_base = '/home/bishnu/Documents/objectDetection/cropped_images/image_batches'

    # Call the function
    move_images(source_folder, dest_folder_base)
