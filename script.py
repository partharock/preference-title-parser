import os
import xml.etree.ElementTree as ET

def extract_preferences(xml_path, strings_path):
    preferences_list = []

    # Parse strings.xml to create a mapping of resource IDs to string values
    strings_tree = ET.parse(strings_path)
    strings_root = strings_tree.getroot()
    string_mapping = {elem.attrib['name']: elem.text for elem in strings_root.findall('.//string')}

    # Parse the XML file containing preferences
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Traverse the XML tree and extract preferences with titles
    for preference_elem in root.findall(".//*[@android:title]"):
        title_attr = preference_elem.get("android:title")

        # Check if the title attribute references a string resource
        if title_attr.startswith("@string/"):
            resource_id = title_attr.split("/")[1]
            string_value = string_mapping.get(resource_id, "")
            preferences_list.append(string_value)
        else:
            preferences_list.append(title_attr)

    return preferences_list

def process_directory(directory_path, strings_path):
    all_preferences = []

    # Traverse all XML files in the specified directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".xml"):
                xml_path = os.path.join(root, file)
                preferences = extract_preferences(xml_path, strings_path)
                all_preferences.extend(preferences)

    return all_preferences

# Example usage
directory_path = "/path/to/xml/files"
strings_path = "/path/to/res/values/strings.xml"

preferences_list = process_directory(directory_path, strings_path)

# Print the list of preferences
print(preferences_list)
