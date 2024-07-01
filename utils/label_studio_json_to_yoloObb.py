import json 
import pandas as pd
from pathlib import Path
import os
import math
from miscellaneous import save_to_txt_file, path_valid


def convert_json_to_obb_format(json_path, destination_path, image_size=(256,256)):
    '''
    function that converts the dataframe to yolo_obb format

    Parameters:
    - json_path (str): path to the label-studio json file
    - destination_path (str) : path to the destination directory
    - image_size (tuple) : image size eg. 256*256 (image_height, image_width)
    
    TODO: check the class label also and then put that class label in the files

    Returns: 
    True (bool): if successful
    False (bool): if unsuccessful
    '''

    # check validity of the path of json
    if not path_valid(json_path) and not path_valid(destination_path):
        print(f'The path for json_path or destination_path is invalid.')
        return False
    
    json_path_obj = Path(json_path)
    destination_path_obj = Path(destination_path)

    # Check if the file extension is .json
    if json_path_obj.suffix != '.json':
        print(f"The file '{json_path}' is not a JSON file.")
        return False

    # Check if the destination_path is a directory
    if not destination_path_obj.is_dir():
        print(f"The path '{destination_path}' is not a directory.")
        return False
    
    df = get_bboxes_from_label_studio_json(json_path)

    print(df)

    # convert the b_boxes into yolo_obb format
    for _, row in df.iterrows():
        file_name = row['file_name']
        # file_name needs to be be .txt not .jpg
        split_file_name = file_name.split('.')
        file_name = split_file_name[0]

        print(file_name)

        b_boxes = row['b_boxes']
        # Get original image dimensions
        img_height, img_width = image_size

        # Scale factors
        x_scale = img_width / 100
        y_scale = img_height / 100

        lines_to_write = []
        for bbox in b_boxes:
            x0 = bbox['x'] * x_scale
            y0 = bbox['y'] * y_scale
            width = bbox['width'] * x_scale
            height = bbox['height'] * y_scale
            angle = bbox['rotation']

            # Calculate rotated points: clockwise direction
            '''
            ptl is the initial point.
            pt2 is obtained by moving horizontally from ptl considering the rotation.
            pt3 is obtained by moving vertically from pt2 considering the rotation.
            pt4 is obtained by moving vertically from ptl considering the rotation.
            '''
            pt1 = (round(x0, 3), round(y0, 3))
            pt2 = (round(x0 + width * math.cos(math.radians(angle)), 3), round(y0 + width * math.sin(math.radians(angle))))
            pt3 = (round(x0 + width * math.cos(math.radians(angle)) - height * math.sin(math.radians(angle)), 3), round(y0 + width * math.sin(math.radians(angle)) + height * math.cos(math.radians(angle)), 3))
            pt4 = (round(x0 - height * math.sin(math.radians(angle)), 3), round(y0 + height * math.cos(math.radians(angle)), 3))

            # TODO: convert the class-labels which is in b_boxes['rectanglelabels'] = ['class1', 'class2', 'class3']
            class_label = bbox['rectanglelabels'][0]

            # TODO: way to get the difficuulty of finding the class-label
            difficulty = 0 # default 
            
            x1,y1 = pt1
            x2,y2 = pt2
            x3,y3 = pt3
            x4,y4 = pt4

            # save the files in the yolo_obb format (x1,y1,x2,y2,x3,y3,x4,y4)
            coordinates = (x1,y1,x2,y2,x3,y3,x4,y4)
            # print(coordinates)
            new_file_path = destination_path_obj.joinpath(file_name)
            # line = str(class_label) + ',' + ','.join(map(str, coordinates))
            line = ','.join(map(str, coordinates)) + ',' + str(class_label) + ',' + str(difficulty)
            
            lines_to_write.append(line)
        save_to_txt_file(lines_to_write=lines_to_write, destination_path=new_file_path)
    return True

def get_bboxes_from_label_studio_json(json_path):    
    '''
    Function to convert label-studio-json-to-yolo-obb
    
    Parameters:
    - path (str): The path to check.
    
    Returns
    - pandas.DataFrame : DataFrame containing the bounding boxes and relevant metadata.
        ['id', 'annotations' 'file_name', 'b_boxes', 'total_annotations']
        format of b_boxes: x,y,width,height,rotation
    - None: if the json_path is invalid

    TODO: check the class label also and then put that class label in the files 
    - 
    '''
    # open the json file as datafarme
    ## check if the path is a valid path
    if not path_valid(json_path):
        print(f'The json path is not valid')
        return None

    with open (json_path, 'r') as file: 
        data = json.load(file)

    df = pd.DataFrame(data)

    # drop some columns
    df.drop(columns=['drafts', 'predictions','meta','created_at', 'updated_at', 
                     'inner_id', 'cancelled_annotations', 'total_predictions', 
                     'comment_count','unresolved_comment_count','last_comment_updated_at',
                     'updated_by','comment_authors','data','total_annotations', 'project'], inplace=True)
    '''
    Here, 'total_annotations' was also dropped and later manually calculated.
    This is because, all column record has 1 as their element. 
    '''

    # From 'annotation' column get only the bounding boxes
    rows = []
    row_count = 0
    for i, row in df.iterrows():
        row_count += 1
        new_row = {}
        # print(f'image# {i}')
        # print(f'id: {row['id']}')
        new_row['id'] = row['id']
        for j,annotation in enumerate(row['annotations']):
            # print(f'j: {j}')
            annotation_count = 0
            b_boxes = []
            for k in annotation['result']:
                annotation_count =annotation_count+1
                # print(k['value'])
                b_boxes.append(k['value'])
            # print(f'annotation_count: {annotation_count}')
            new_row['b_boxes'] = b_boxes
            new_row['total_annotations'] = annotation_count
            rows.append(new_row)  
    
    # make a new column 'b_boxes' to resultant dataframe
    b_boxes_df = pd.DataFrame(rows)
    df = pd.merge(df, b_boxes_df, on="id", how="left")

    # drop the 'annotations' column since we now have b_boxes column. 
    df.drop(columns=['annotations'])

    # Drop all the rows which has NaN
    df = df[df['total_annotations'].notnull()]

    # Drop all the rows which has 0 annotations
    df = df.drop(df.query('total_annotations == 0').index)
    # print(f'#rows={row_count}')

    # rename the column 'file_upload' to 'file_name'
    df.rename(columns={'file_upload': 'file_name'}, inplace=True)
    
    return df


def convert_json_to_yolo_with_roataion(json_path, destination_path, image_size):
    '''
    function that converts the dataframe to yolo_obb format

    Parameters:
    - json_path (str): path to the label-studio json file
    - destination_path (str) : path to the destination directory
    - image_size (tuple) : image size eg. 256*256 (image_height, image_width)
    
    TODO: check the class label also and then put that class label in the files
    '''

    # check validity of the path of json
    if not path_valid(json_path) and not path_valid(destination_path, image_size):
        print(f'The path for json_path or destination_path is invalid.')
        return None
    
    json_path_obj = Path(json_path)
    destination_path_obj = Path(destination_path)

    # Check if the file extension is .json
    if json_path_obj.suffix != '.json':
        print(f"The file '{json_path}' is not a JSON file.")
        return False

    # Check if the destination_path is a directory
    if not destination_path_obj.is_dir():
        print(f"The path '{destination_path}' is not a directory.")
        return False
    
    df = get_bboxes_from_label_studio_json(json_path)

    # print(df)

    # convert the b_boxes into yolo_obb format
    for _, row in df.iterrows():
        file_name = row['file_name']
        # file_name needs to be be .txt not .jpg
        split_file_name = file_name.split('.')
        file_name = split_file_name[0]

        print(f'filename: {file_name}')

        b_boxes = row['b_boxes']
        # Get original image dimensions
        img_height, img_width = image_size

        # Scale factors
        x_scale = img_width / 100
        y_scale = img_height / 100

        lines_to_write = []
        for bbox in b_boxes:
            x0 = bbox['x'] * x_scale
            y0 = bbox['y'] * y_scale
            width = bbox['width'] * x_scale
            height = bbox['height'] * y_scale
            angle = bbox['rotation']

            # TODO: convert the class-labels which is in b_boxes['rectangables'] = ['class1', 'class2', 'class3']
            class_label = 0
            # normalize the points. 
            x0, y0 = round(x0/img_width,3), round(y0/img_height,3)
            width, height = round(width/img_width,3), round(height/img_height,3)

            # TODO: check if we need to normalize the angle as well. 

            # save the files in the yolo_obb format (x1,y1,x2,y2,x3,y3,x4,y4)
            coordinates = (x0,y0,width,height,angle)
            print(coordinates)
            new_file_path = destination_path_obj.joinpath(file_name)
            line = str(class_label) + ',' + ','.join(map(str, coordinates))
            
            lines_to_write.append(line)
        save_to_txt_file(lines_to_write=lines_to_write, destination_path=new_file_path)

def main():
    # TODO: use parser to make it take cmd args. 
    print("This is the main function.")
    path = 'label-studio json files\\bagmati-patch2_waste1\\bagmati-patch2_waste1.json'
    destination_path = 'dataset\\labelTxt\\bagmati-patch2-waste1'

    # Your program logic goes here
    convert_json_to_obb_format(json_path=path, destination_path=destination_path, image_size=(256,256))

if __name__ == "__main__":
    main()