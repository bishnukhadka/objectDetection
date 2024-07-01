import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
from matplotlib.patches import Polygon
from miscellaneous import rotate_point

def plot_oriented_bbox(obb_file, image_file):
    """
    Plots oriented bounding boxes on an image using coordinates from a YOLO OBB format file.

    The YOLO OBB format is assumed to be:
    class_label_int, x1, y1, x2, y2, x3, y3, x4, y4
    where (x1, y1), (x2, y2), (x3, y3), (x4, y4) are the normalized coordinates of the rectangle's corners.

    Parameters:
    -----------
    yolo_obb_file : str
        Path to the YOLO OBB file containing the bounding box coordinates.
        
    image_file : str
        Path to the image file corresponding to the YOLO OBB file.
        
    Returns:
    --------
    None
        Displays the image with the oriented bounding boxes plotted.
        
    Raises:
    -------
    FileNotFoundError
        If the image file or YOLO OBB file is not found.
        
    ValueError
        If there are issues with parsing the bounding box coordinates.
        
    Exception
        For any other unexpected errors.
    """
    try:
        # Load the image
        image = plt.imread(image_file)
        if image is None:
            print(f"Error: Unable to load image from {image_file}")
            return
        
        # Read the YOLO OBB file
        with open(obb_file, 'r') as file:
            lines = file.readlines()
        
        # Plot the image
        fig, ax = plt.subplots(1)
        ax.imshow(image)

        num_of_bboxes =0 
        # Parse each line in the YOLO OBB file
        for line in lines:
            num_of_bboxes = num_of_bboxes + 1
            data = line.strip().split(',')
            print(data)
            if len(data) != 10:
                print(f'Invalid format.')
                return
            try:
                # Extract class and coordinates
                # Extract coordinates and convert to float
                x1, y1, x2, y2, x3, y3, x4, y4 = list(map(float, data[:8]))

                # Extract class label and difficulty
                cls = data[8]
                difficulty = int(data[9])  # Assuming difficulty should be an integer   
            except ValueError as e:
                print(f"Error parsing line: {line}, {e}")  # Debug: Print parsing error
                return
            
            # Create a polygon from the coordinates
            rect = patches.Polygon(((x1, y1), (x2, y2), (x3, y3), (x4, y4)), closed=True, edgecolor='r', facecolor='none')
            
            # Add the polygon to the plot
            ax.add_patch(rect)
        
        plt.title(f'{image_file.split('\\')[-1]}, #Bboxes: {num_of_bboxes}')
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to draw bounding boxes on an image using matplotlib.pyplot
def plot_rotated_rect_label_stuido_json(bounding_boxes, image_path):
    """
    Plots angled rectangles on an image based on a list of bounding boxes.

    The bounding boxes are expected to be dictionaries with keys 'x', 'y', 'width', 'height', and 'rotation'.
    The coordinates and dimensions are percentages of the image dimensions, while the rotation is in degrees.

    Parameters:
    -----------
    bounding_boxes : list of dict
        A list of dictionaries where each dictionary represents a bounding box with the following keys:
            - 'x' (float): X-coordinate of the top-left corner as a percentage of the image width.
            - 'y' (float): Y-coordinate of the top-left corner as a percentage of the image height.
            - 'width' (float): Width of the bounding box as a percentage of the image width.
            - 'height' (float): Height of the bounding box as a percentage of the image height.
            - 'rotation' (float): Rotation angle of the bounding box in degrees.
    
    image_path : str
        Path to the image file on which the bounding boxes will be plotted.
    
    Returns:
    --------
    None
        Displays the image with the bounding boxes plotted.
    
    Raises:
    -------
    FileNotFoundError
        If the image file is not found.
        
    ValueError
        If there are issues with parsing the bounding box coordinates or scaling factors.
        
    Exception
        For any other unexpected errors.
    
    Example:
    --------
    >>> bounding_boxes = [
    >>>     {'x': 10, 'y': 20, 'width': 30, 'height': 40, 'rotation': 15},
    >>>     {'x': 50, 'y': 60, 'width': 20, 'height': 10, 'rotation': 45}
    >>> ]
    >>> image_path = 'path/to/image.jpg'
    >>> draw_angled_rec_from_list_of_bboxes(bounding_boxes, image_path)
    """
    img = plt.imread(image_path)

    if img is None:
        print(f"Error: Unable to load image from {image_path}")
        return
    
    # Get original image dimensions
    original_height, original_width = img.shape[:2]

    # Create figure and axes
    fig, ax = plt.subplots(1)
    
    # Display the image
    ax.imshow(img)
    
    # Scale factors
    x_scale = original_width / 100
    y_scale = original_height / 100

    for i,bbox in enumerate(bounding_boxes):
        x0 = bbox['x'] * x_scale
        y0 = bbox['y'] * y_scale
        width = bbox['width'] * x_scale
        height = bbox['height'] * y_scale
        angle = bbox['rotation']

        # Calculate rotated points
        pt1 = (round(x0, 3), round(y0, 3))
        pt2 = (round(x0 + width * math.cos(math.radians(angle)), 3), round(y0 + width * math.sin(math.radians(angle))))
        pt3 = (round(x0 + width * math.cos(math.radians(angle)) - height * math.sin(math.radians(angle)), 3), round(y0 + width * math.sin(math.radians(angle)) + height * math.cos(math.radians(angle)), 3))
        pt4 = (round(x0 - height * math.sin(math.radians(angle)), 3), round(y0 + height * math.cos(math.radians(angle)), 3))

        # Create a rotated rectangle patch
        rect = patches.Polygon([pt1,pt2,pt3,pt4],
                                closed=True, fill=None, edgecolor='b')

        # Add the rectangle patch to the Axes
        ax.add_patch(rect)

        # Plot dots at the corners
        # ax.plot(x0, y0, 'o', markersize=8, color='red')
        # ax.plot(x0 + width * math.cos(math.radians(angle)), y0 + width * math.sin(math.radians(angle)), 'o', markersize=8, color='red')
        # ax.plot(x0 + width * math.cos(math.radians(angle)) - height * math.sin(math.radians(angle)), y0 + width * math.sin(math.radians(angle)) + height * math.cos(math.radians(angle)), 'o', markersize=8, color='red')
        # ax.plot(x0 - height * math.sin(math.radians(angle)), y0 + height * math.cos(math.radians(angle)), 'o', markersize=8, color='red')

    # Display the plot with bounding boxes
    plt.title('Bounding Boxes')
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()


def plot_rotated_rectangle_pascal_voc_format(bounding_boxes, image_path):
    """
    Plots rotated rectangles on an image based on a list of bounding boxes in Pascal VOC format.

    The bounding boxes are expected to be dictionaries with keys 'xmin', 'ymin', 'xmax', 'ymax', and 'rotation'.
    The coordinates are in the same scale as the image dimensions, and the rotation is in degrees.

    Parameters:
    -----------
    bounding_boxes : list of dict
        A list of dictionaries where each dictionary represents a bounding box with the following keys:
            - 'xmin' (float): X-coordinate of the top-left corner of the bounding box.
            - 'ymin' (float): Y-coordinate of the top-left corner of the bounding box.
            - 'xmax' (float): X-coordinate of the bottom-right corner of the bounding box.
            - 'ymax' (float): Y-coordinate of the bottom-right corner of the bounding box.
            - 'rotation' (float): Rotation angle of the bounding box in degrees.

    image_path : str
        Path to the image file on which the bounding boxes will be plotted.

    Returns:
    --------
    None
        Displays the image with the bounding boxes plotted.

    Raises:
    -------
    FileNotFoundError
        If the image file is not found.

    ValueError
        If there are issues with parsing the bounding box coordinates or scaling factors.

    Exception
        For any other unexpected errors.

    Example:
    --------
    >>> bounding_boxes = [
    >>>     {'xmin': 10, 'ymin': 20, 'xmax': 30, 'ymax': 40, 'rotation': 15},
    >>>     {'xmin': 50, 'ymin': 60, 'xmax': 70, 'ymax': 80, 'rotation': 45}
    >>> ]
    >>> image_path = 'path/to/image.jpg'
    >>> plot_rotated_rectangle_pascal_voc_format(bounding_boxes, image_path)
    """
    img = plt.imread(image_path)

    if img is None:
        print(f"Error: Unable to load image from {image_path}")
        return
    
    # Get original image dimensions
    original_height, original_width = img.shape[:2]

    # Create figure and axes
    fig, ax = plt.subplots(1)
    
    # Display the image
    ax.imshow(img)

    num_of_bboxes = 0
    for bbox in bounding_boxes:
        num_of_bboxes = num_of_bboxes + 1
        xmin = bbox['xmin']
        ymin = bbox['ymin']
        xmax = bbox['xmax']
        ymax = bbox['ymax']
        rotation_angle = bbox['rotation']

        # Calculate center and dimensions
        cx = (xmax + xmin) / 2
        cy = (ymax + ymin) / 2
        width = xmax - xmin
        height = ymax - ymin

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

        # Create a rotated rectangle patch
        rect = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], closed=True, fill=None, edgecolor='b')

        # Add the rotated rectangle patch to the Axes
        ax.add_patch(rect)
    
    print(f'Number of bounding boxes: {num_of_bboxes}')

    # Display the plot with bounding boxes
    plt.title('Bounding Boxes')
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()

def main():
    yol0_obb_file = "C:\\Users\\HP\\Documents\\py\\Object Detection\\cvat output pascal voc xml\\bagmati-patch1-waste2\\labels\\DJI_20240518124257_0028_V282.txt"
    image_file = "C:\\Users\\HP\\Documents\\py\\Object Detection\\dataset\\bagmati\\Bagmati-patch-1-cropped\\Bagmati patch 1-waste2\\bagmati patch 1 waste 2 batch_1_to_5\\DJI_20240518124257_0028_V282.jpg"

    plot_oriented_bbox(obb_file=yol0_obb_file, image_file=image_file)


if __name__ == "__main__":
    main()