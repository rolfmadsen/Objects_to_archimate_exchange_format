import xml.etree.ElementTree as ET
import csv

# Parse the XML file
tree = ET.parse('archimate_exchange_format.xml')
root = tree.getroot()

# Extract elements and relationships
elements = root.find('{http://www.opengroup.org/xsd/archimate/3.0/}elements')
relationships = root.find('{http://www.opengroup.org/xsd/archimate/3.0/}relationships')

# Create dictionaries for elements and relationships
element_dict = {}
relationship_dict = {}

# Extract and organize element information
for element in elements:
    element_id = element.get('identifier')
    element_type = element.get('{http://www.w3.org/2001/XMLSchema-instance}type')
    element_name = element.find('{http://www.opengroup.org/xsd/archimate/3.0/}name').text
    element_dict[element_id] = {'type': element_type, 'name': element_name}

# Extract and organize relationship information
for relationship in relationships:
    relationship_id = relationship.get('identifier')
    relationship_type = relationship.get('{http://www.w3.org/2001/XMLSchema-instance}type')
    relationship_source = relationship.get('source')
    relationship_target = relationship.get('target')
    relationship_dict[relationship_id] = {'type': relationship_type, 'source': relationship_source, 'target': relationship_target}

# Save elements as nodes.csv
with open('gephi_nodes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Id', 'Label', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for element_id, element_data in element_dict.items():
        writer.writerow({'Id': element_id, 'Label': element_data['name'], 'Type': element_data['type']})

# Save relationships as edges.csv
with open('gephi_edges.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Id', 'Source', 'Target', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for relationship_id, relationship_data in relationship_dict.items():
        writer.writerow({'Id': relationship_id, 'Source': relationship_data['source'], 'Target': relationship_data['target'], 'Type': relationship_data['type']})
