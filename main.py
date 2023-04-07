import csv
import uuid
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_ncname_uuid():
    return "id-" + str(uuid.uuid4()).replace('-', '').replace('_', '')

def generate_aef_from_csv(csv_file):
    app_components = []
    data_objects = []

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            app_component, data_object = row
            app_components.append(app_component)
            data_objects.append(data_object)

    model = Element(
        'model',
        attrib={
            'xmlns': 'http://www.opengroup.org/xsd/archimate/3.0/',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.opengroup.org/xsd/archimate/3.0/ http://www.opengroup.org/xsd/archimate/3.1/archimate3_Diagram.xsd',
            'identifier': create_ncname_uuid(),
        }
    )

    name = SubElement(model, 'name')
    name.set('xml:lang', 'en')
    name.text = 'CSV source and target transformation to Archimate Exchange Format'

    elements = SubElement(model, 'elements')
    relationships = SubElement(model, 'relationships')
    organizations = SubElement(model, 'organizations')
    application_item = SubElement(organizations, 'item')
    application_label = SubElement(application_item, 'label')
    application_label.set('xml:lang', 'en')
    application_label.text = 'Application'

    app_component_ids = []
    for app_component in app_components:
        element = SubElement(elements, 'element', attrib={
            'identifier': create_ncname_uuid(),
            'xsi:type': 'ApplicationComponent',
        })
        app_component_name = SubElement(element, 'name')
        app_component_name.set('xml:lang', 'en')
        app_component_name.text = app_component
        app_component_ids.append(element.get('identifier'))
        # add application item for each app component
        item = SubElement(application_item, 'item', attrib={'identifierRef': element.get('identifier')})

    data_object_ids = []
    for data_object in data_objects:
        element = SubElement(elements, 'element', attrib={
            'identifier': create_ncname_uuid(),
            'xsi:type': 'DataObject',
        })
        data_object_name = SubElement(element, 'name')
        data_object_name.set('xml:lang', 'en')
        data_object_name.text = data_object
        data_object_ids.append(element.get('identifier'))
        # add application item for each data object
        item = SubElement(application_item, 'item', attrib={'identifierRef': element.get('identifier')})

    relation_item = SubElement(organizations, 'item')
    relation_label = SubElement(relation_item, 'label')
    relation_label.set('xml:lang', 'en')
    relation_label.text = 'Relations'

    relationship_ids = []

    for app_component_id, data_object_id in zip(app_component_ids, data_object_ids):
        relationship = SubElement(relationships, 'relationship', attrib={
            'identifier': create_ncname_uuid(),
            'source': data_object_id,  # This should be data_object_id
            'target': app_component_id,  # This should be app_component_id
            'xsi:type': 'Association',
        })
        relationship_ids.append(relationship.get('identifier'))

        # add relation item for each relationship
        item = SubElement(relation_item, 'item', attrib={'identifierRef': relationship.get('identifier')})

    # Create a new 'item' element for the 'organizations' element
    organizations_item = SubElement(organizations, 'item')

    # Create a 'label' element with text 'Views' and add it to the new 'item' element
    label = SubElement(organizations_item, 'label', {'xml:lang': 'en'})
    label.text = 'Views'

    # Add views element after organizations
    views = SubElement(model, 'views')
    diagrams = SubElement(views, 'diagrams')

       # Create a new view with a unique identifier and a name
    view = SubElement(diagrams, 'view', attrib={
        'identifier': create_ncname_uuid(),
        'xsi:type': 'Diagram',
        'viewpoint': 'Application Cooperation',
    })
    view_name = SubElement(view, 'name')
    view_name.set('xml:lang', 'en')
    view_name.text = 'Application Cooperation'

    # Add the view identifier reference to the 'Views' label within the 'organizations' element
    views_item = SubElement(organizations_item, 'item', {'identifierRef': view.get('identifier')})

    data_object_node_ids = []
    app_component_node_ids = []

    # Add instances (application components and data objects) as nodes in the view
    instance_y_pos = 0  # initialize y-axis position to 0
    for index, (app_component_id, data_object_id) in enumerate(zip(app_component_ids, data_object_ids)):
        for instance_type, instance_id in [('data_object', data_object_id), ('app_component', app_component_id)]:
            node_id = create_ncname_uuid()
            
            x_offset = 250 if instance_type == 'app_component' else 0  # add an offset to the x-axis position if it's an application component
            
            node = SubElement(view, 'node', attrib={
                'identifier': node_id,
                'elementRef': instance_id,
                'xsi:type': 'Element',
                'x': str(84 + x_offset),
                'y': str(instance_y_pos),
                'w': '120',
                'h': '55',
            })
            
            # Store node identifiers in separate lists
            if instance_type == 'data_object':
                data_object_node_ids.append(node_id)
            else:
                app_component_node_ids.append(node_id)
        
            style = SubElement(node, 'style')
            fill_color = SubElement(style, 'fillColor', attrib={'r': '181', 'g': '255', 'b': '255', 'a': '100'})
            line_color = SubElement(style, 'lineColor', attrib={'r': '92', 'g': '92', 'b': '92', 'a': '100'})
            font = SubElement(style, 'font', attrib={'name': 'Sans', 'size': '9'})
            font_color = SubElement(font, 'color', attrib={'r': '0', 'g': '0', 'b': '0'})
        
        instance_y_pos += 72  # add 72 to the y-axis position for each new row in the CSV

    # Add connections for relationships
    for index, relationship_id in enumerate(relationship_ids):
        source_node_id = data_object_node_ids[index]
        target_node_id = app_component_node_ids[index]

        connection = SubElement(view, 'connection', attrib={
            'identifier': create_ncname_uuid(),
            'relationshipRef': relationship_id,
            'xsi:type': 'Relationship',
            'source': source_node_id,
            'target': target_node_id,
        })

        # Add the style element
        style = SubElement(connection, 'style')
        line_color = SubElement(style, 'lineColor', attrib={'r': '0', 'g': '0', 'b': '0'})
        font = SubElement(style, 'font', attrib={'name': 'Sans', 'size': '9'})
        font_color = SubElement(font, 'color', attrib={'r': '0', 'g': '0', 'b': '0'})

    # Save the generated XML to a file
    with open('output.xml', 'w', encoding='utf-8') as f:
        f.write(prettify(model))
        print(f"AEF file generated at: output.xml")

if __name__ == '__main__':
    csv_file = 'input.csv'
    generate_aef_from_csv(csv_file)
