from PIL import Image
import os
import yaml
# script to take a photo and output differnet 256*256 image window of that photo

def extract_windows(image_path, output_folder, window_size=256):
    image = Image.open(image_path)
    width, height = image.size
    print(f"window_size: {width}*{height}")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    image_name = os.path.splitext(os.path.basename(image_path))[0]  # Get the name of the input image file

    window_count = 0
    for i in range(0, height-height%window_size, window_size):
        for j in range(0, width-width%window_size, window_size):
            try:
                # image.crop((left, upper, right, lower))
                window = image.crop((j, i, j + window_size, i + window_size))
                window.save(os.path.join(output_folder, f'{image_name}{window_count}.jpg'))
                window_count += 1
                print(f"{image_name}{window_count} saved sucessfully.")


                print(f"size of {window_count} :::: ({j},{i}), ({j+window_size},{i+window_size})")
            except Exception as e:
                print(e)
        
    print(width - width%window_size)
    print(height - height%window_size)


def get_jpg_files_path(folder_path):
    jpg_files_path = []
    # Check if the folder path exists
    if os.path.exists(folder_path):
        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            # Check if the file has a .jpg extension
            if filename.lower().endswith('.jpg'):
                # print(filename.lower())
                # Add the file to the list of jpg_files
                jpg_files_path.append(os.path.join(folder_path, filename))
    else:
        print("Folder path does not exist.")
    return jpg_files_path


def read_yaml_file(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            # Load YAML data from the file
            yaml_data = yaml.safe_load(yaml_file)
            return yaml_data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        return None


def main(): 
    # # Example usage
    # image_path = 'helper_files/Vinicius-Jr-6c9ba9a.jpg'
    # copped_image_output_folder = 'helper_files/cropped'
    # extract_windows(image_path, copped_image_output_folder)


    # Replace 'folder_path' with the path to your folder
    # folder_path = '/home/bishnu/Documents/river photos data/DJI_202405181237_003'
    

    # Example usage:
    file_path = 'path_constants.yaml'  # Replace with the path to your YAML file
    yaml_data = read_yaml_file(file_path)
    if yaml_data:
        print("YAML data:")
        print(yaml_data)
        folder_path = yaml_data['folder_path']
        copped_image_output_folder=yaml_data['copped_image_output_folder']

        jpg_files_paths = get_jpg_files_path(folder_path)

        for jpg_files_path in jpg_files_paths:
            print(file_path)
            extract_windows(jpg_files_path, copped_image_output_folder)


if __name__ == "__main__":
    main()

