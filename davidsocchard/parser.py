import json
import os


def json_to_python_object(file):
    """
    Get all data from json file.

    :param file: file from jsons folder
    """
    with open(f"objects/{file}") as f:
        json_file = json.load(f)  # Load json file
        json_objects = json_file['objects']  # Parse all data into python file
        print(f'Number of objects: {len(json_objects)}')  # To print number of objects
        for i in range(0, len(json_objects)):  # Make sure that we do this for all objects on file
            points = extract_points(json_objects[i])
            occluded = extract_occluded(json_objects[i])
            attributes = extract_attributes(json_objects[i])
            label = extract_label(json_objects[i])
            print("================================")  # Simple object separator (Not necessary, only for visualization)
            print(f'Object number {i + 1}: ')
            print(f'Label: {label} \n'  # Get label from object
                  f'Points: {points} \n'  # Get point from object
                  f'Occlusion: {occluded} \n'  # Get occlusion value from object
                  f'Attributes: {attributes}')  # Get attribute list from object


def extract_points(json_object):
    """
    Get points in [xmin, ymin, xmax, ymin] format.

    :param json_object: json object file
    :return: json data object.
    """
    points = []
    for list_of_points in json_object['data']:
        for el in list_of_points:
            points.append(el)
    return points


def extract_attributes(json_object):
    """
    Get attributes list.

    :param json_object: json object file
    :return:
    """
    return json_object['attribute']


def extract_occluded(json_object):
    """
    Get value of occlusion.

    :param json_object: json object file
    :return: json occlusion object value
    """
    return extract_attributes(json_object)['occlusion']


def extract_label(json_object):
    """
    Get a label.

    :param json_object: json object file
    :return: json class_name object
    """
    return json_object['class_name']


if __name__ == '__main__':
    for filename in os.listdir('objects'):  # Use every file from objects folder
        json_to_python_object(filename)  # Call the main method to get information
        print("////////////////////////////////")  # Simple file separator (Not necessary, only for visualization)
