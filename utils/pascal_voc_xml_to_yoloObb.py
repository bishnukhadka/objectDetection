import math
import pandas as pd
from pathlib import Path
import os
from miscellaneous import path_valid, save_to_txt_file
import xml.etree.ElementTree as ET
from miscellaneous import rotate_point, get_filenames_of_extention

def convert_pascal_voc_xml_to_yoloOBB(source_folder, destination_folder):
    '''
    Convert the Pascal Voc XML format of the source folder to the YOLO_OBB format
    and save it to the destination folder. 

    Parameters: 
    - source_folder (str): path to source folder
    - destination_folder (str): path to destination folder

    '''
    # check the validity of source_folder and destination_folder
    if not path_valid(source_folder) and not path_valid(destination_folder): 
        print(f'Path of source folder or the destination folder is not correct')
        return False, []

    # Ensure the path(str) is a path(obj)
    source_path_obj = Path(source_folder)
    destination_folder_path_obj = Path(destination_folder)

    # get the filename of all the xml files in the folder
    filenames_xml = get_filenames_of_extention(source_folder, extention='.xml')      


    failed_lables = []
    # loop all the filename and convert them to yoloOBB fomrat
    for i,filename in enumerate(filenames_xml):
        print(f'{i}: {filename}')
        # path of the .xml file
        xml_path_obj = source_path_obj/filename
        success = convert_single_pascal_voc_xml_to_yoloObb(xml_path_obj, destination_folder_path_obj, image_size=(256,256))
        if not success: 
            # print('failed')
            failed_lables.append(xml_path_obj.name)
    
    return True, failed_lables


def convert_single_pascal_voc_xml_to_yoloObb(xml_path, destination_path, image_size=(256,256)):
    '''
    function that converts the dataframe to yolo_obb format

    Parameters:
    - json_path (str): path to the label-studio json file
    - destination_path (str) : path to the destination directory
    - image_size (tuple) : image size eg. 256*256 (image_height, image_width)
    
    TODO: check the class label also and then put that class label in the files

    Returns: 
    - True (bool): if sucessful
    - False (bool): if error occured
    '''

    # check validity of the path of json
    if not path_valid(xml_path) and not path_valid(destination_path):
        print(f'The path for xml_path or destination_path is invalid.')
        return None

    # Ensure the path(str) is a path(obj)
    xml_path_obj = Path(xml_path)
    
    # print(f'suffix: {xml_path_obj.suffix}')
    destination_path_obj = Path(destination_path)

    # Check if the file extension is .json
    if xml_path_obj.suffix != '.xml':
        print(f"The file '{xml_path}' is not a xml file.")
        return False

    # Check if the destination_path is a directory
    if not destination_path_obj.is_dir():
        print(f"The path '{destination_path}' is not a directory.")
        return False
    
    df = extract_b_boxes_and_rotation(xml_path)

    # print(df)

    # check that the df has only a single row. 
    if df.shape[0] != 1: 
        print(f'Error in extracting b_boxes form xml_path. Shape: {df.shape}')
        return False


    # convert the b_boxes into yolo_obb format  
    file_name = df['file_name'][0]
    # file_name needs to be be .txt not .jpg
    split_file_name = file_name.split('.')
    file_name = split_file_name[0]

    # print(file_name)

    b_boxes = df['b_boxes'][0]
    # Get original image dimensions
    img_height, img_width = image_size

    lines_to_write = []
    new_file_path = destination_path_obj.joinpath(file_name)
    num_of_bboxes =0
    for bbox in b_boxes:
        xmin = bbox['xmin']
        ymin = bbox['ymin']
        xmax = bbox['xmax']
        ymax = bbox['ymax']
        rotation_angle = bbox['rotation']

        # Calculate center and dimensions
        cx = (xmax + xmin) / 2
        cy = (ymax + ymin) / 2
        # width = xmax - xmin
        # height = ymax - ymin

        # Rotate each corner of the rectangle around its center
        x1, y1 = rotate_point(xmin - cx, ymin - cy, rotation_angle)
        x2, y2 = rotate_point(xmax - cx, ymin - cy, rotation_angle)
        x3, y3 = rotate_point(xmax - cx, ymax - cy, rotation_angle)
        x4, y4 = rotate_point(xmin - cx, ymax - cy, rotation_angle)

        # Translate back to original coordinates
        x1 += cx
        y1 += cy
        x2 += cx
        y2 += cy
        x3 += cx
        y3 += cy
        x4 += cx
        y4 += cy

        # Normalize the coordinates
        x1, x2, x3, x4 = round(x1/img_width,5), round(x2/img_width,5), round(x3/img_width,5),round(x4/img_width,5)
        y1, y2, y3, y4 = round(y1/img_height,5), round(y2/img_height,5) , round(y3/img_height,5), round(y4/img_height,5)

        # save the files in the yolo_obb format (x1,y1,x2,y2,x3,y3,x4,y4)
        coordinates = (x1,y1,x2,y2,x3,y3,x4,y4)

        # a function to map different class label to their respective int values
        class_label_int = 0


        line = str(class_label_int) + ',' + ','.join(map(str, coordinates))
        # print(line)
    
        lines_to_write.append(line)
        num_of_bboxes = num_of_bboxes +1 
    print(f'Number of bboxes: {num_of_bboxes}')
    # print(lines_to_write)
    save_to_txt_file(lines_to_write=lines_to_write, destination_path=new_file_path)
    print()
    return True


# Function to extract bounding box coordinates and rotation
def extract_b_boxes_and_rotation(file_path):
    """
    Extracts bounding box coordinates and rotation from an XML file and returns a DataFrame.

    Args:
    - file_path (str): Path to the XML file containing object annotations.

    Returns:
    - pd.DataFrame: DataFrame with columns 'file_name' and 'b_boxes', where 'b_boxes' contains a list of dictionaries
      representing bounding boxes and their attributes.

    Raises:
    - ET.ParseError: If there's an error parsing the XML file.
    - FileNotFoundError: If the specified file_path does not exist.
    - Exception: For any other unexpected errors during file processing.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing the XML file: {e}")
        return []
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    boxes = []
    row = {}
    file_name = root.find('filename').text
    for obj in root.findall('object'):
        name = obj.find('name').text
        xmin = float(obj.find('bndbox/xmin').text)
        ymin = float(obj.find('bndbox/ymin').text)
        xmax = float(obj.find('bndbox/xmax').text)
        ymax = float(obj.find('bndbox/ymax').text)
        rotation = float(obj.find('attributes/attribute/value').text)
        box = {
            'label': name,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax,
            'rotation': rotation
        }
        boxes.append(box)
        # print(type(boxes))
    row['file_name'] = file_name
    row['b_boxes'] = boxes
    df = pd.DataFrame({
    'file_name': [row['file_name']],
    'b_boxes': [row['b_boxes']]
    })
        
    return df

def main():
    xml_path = "C:\\Users\\HP\\Documents\\py\\Object Detection\\YOLO v5\\files_required for annotation\\bagmati-patch1-waste2\\Annotations"
    destination_path = "C:\\Users\\HP\\Documents\\py\\Object Detection\\dataset\\bagmati\\bagmati-patch-1-cropped\\Bagmati patch 1-waste2\\bagmati patch 1 waste 2 batch_1_to_5\\lables"
    _ , failed_lables = convert_pascal_voc_xml_to_yoloOBB(xml_path, destination_path)

    print(f'Failed lables: {len(failed_lables)}')

if __name__ == "__main__":
    main()