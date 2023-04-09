import csv
import uuid
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_ncname_uuid():
    return f"id-{uuid.uuid4().hex}"

def generate_aef_from_csv(csv_file):

    app_components_order = []
    app_components = {}
    app_component_ids = []
    app_component_uuids = {}

    data_objects_order = []
    data_objects = {}
    data_object_ids = []
    data_object_uuids = {}
    
    processed_nodes = []
    
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
    relation_item = SubElement(organizations, 'item')

    relation_label = SubElement(relation_item, 'label')
    relation_label.set('xml:lang', 'en')
    relation_label.text = 'Relations'
  
    # append views element after organizations
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

    # append the view identifier reference to the 'Views' label within the 'organizations' element
    # Create a new 'item' element for the 'organizations' element
    organizations_item = SubElement(organizations, 'item')

    # Create a 'label' element with text 'Views' and append it to the new 'item' element
    label = SubElement(organizations_item, 'label', {'xml:lang': 'en'})
    label.text = 'Views'
    views_item = SubElement(organizations_item, 'item', {'identifierRef': view.get('identifier')})

    application_item = SubElement(organizations, 'item')
    application_label = SubElement(application_item, 'label')
    application_label.set('xml:lang', 'en')
    application_label.text = 'Application'



    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            app_component, data_object = row
            app_components[app_component] = None
            data_objects[data_object] = None

            if app_component not in app_component_uuids:
                app_component_uuids[app_component] = create_ncname_uuid()
            
            if data_object not in data_object_uuids:
                data_object_uuids[data_object] = create_ncname_uuid()
            
            app_component_id = app_component_uuids[app_component]
            data_object_id = data_object_uuids[data_object]

            if app_component not in app_components:
                app_components.append(app_component)
                app_components_order.append(app_component)
            if data_object not in data_objects:
                data_objects.append(data_object)
                data_objects_order.append(data_object)

            relationship = SubElement(relationships, 'relationship', attrib={
                'identifier': create_ncname_uuid(),
                'source': data_object_id,
                'target': app_component_id,
                'xsi:type': 'Association',
            })
            relationship_ids = []
            relationship_ids.append(relationship.get('identifier'))

            # append relation item for each relationship
            item = SubElement(relation_item, 'item', attrib={'identifierRef': relationship.get('identifier')})


    app_components_order = list(app_components.keys())
    data_objects_order = list(data_objects.keys())

    ##print(app_components_order)
    ##print(data_objects_order)


    for app_component in app_components:

        element = SubElement(elements, 'element', attrib={
            'identifier': app_component_uuids[app_component],
            'xsi:type': 'ApplicationComponent',
        })
        
        name_element = SubElement(element, 'name')
        name_element.set('xml:lang', 'en')
        name_element.text = app_component
        app_component_ids.append(element.get('identifier'))
        # append application item for each app component
        item = SubElement(application_item, 'item', attrib={'identifierRef': element.get('identifier')})

    for data_object in data_objects:

        element = SubElement(elements, 'element', attrib={
            'identifier': data_object_uuids[data_object],
            'xsi:type': 'DataObject',
        })
        
        name_element = SubElement(element, 'name')
        name_element.set('xml:lang', 'en')
        name_element.text = data_object
        data_object_ids.append(element.get('identifier'))
        # append application item for each data object
        item = SubElement(application_item, 'item', attrib={'identifierRef': element.get('identifier')})

    app_component_uuids_rev = {v: k for k, v in app_component_uuids.items()}
    data_object_uuids_rev = {v: k for k, v in data_object_uuids.items()}

    data_object_node_ids = []
    data_object_y_pos = {}
    sorted_data_object_ids = []
    
    app_component_node_ids = []
    sorted_app_component_ids = []

    element_relationships = {}
    element_to_node_id = {}
    source_node_counts = {}

    # Initialize source_node_counts with data_object_ids as keys and set initial value to 0
    for data_object_id in data_object_ids:
        source_node_counts[data_object_id] = 0

    # Populate the element_relationships dictionary with the relationships
    for relationship in relationships:
        source_id = relationship.get('source')
        target_id = relationship.get('target')
        if source_id in data_object_ids and target_id in app_component_ids:
            if source_id not in element_relationships:
                element_relationships[source_id] = []
            element_relationships[source_id].append(target_id)

    # Sort the data_object_ids and app_component_ids based on the relationships
    for data_object_id, related_app_component_ids in element_relationships.items():
        sorted_data_object_ids.append(data_object_id)
        sorted_app_component_ids.extend(related_app_component_ids)

    # append remaining data_object_ids and app_component_ids that have no relationships
    sorted_data_object_ids.extend(data_object_id for data_object_id in data_object_ids if data_object_id not in sorted_data_object_ids)
    sorted_app_component_ids.extend(app_component_id for app_component_id in app_component_ids if app_component_id not in sorted_app_component_ids)

    # append instances (application components and data objects) as nodes in the view
    app_component_index = {app_component_uuids[ac]: index for index, ac in enumerate(app_components)}
    data_object_index = {data_object_uuids[do]: index for index, do in enumerate(data_objects)}

    processed_nodes = []

    for element_id in set(sorted_data_object_ids + sorted_app_component_ids):
        if element_id in processed_nodes:
            continue

        instance_type = 'app_component' if element_id in app_component_ids else 'data_object'

        node_id = create_ncname_uuid()
        element_to_node_id[element_id] = node_id

        x_offset = 250 if instance_type == 'app_component' else 0  # append an offset to the x-axis position if it's an application component
            
        # Calculate the y position based on the index in the order lists
        if instance_type == 'app_component':
            app_component = app_component_uuids_rev[element_id]
            y_pos = app_components_order.index(app_component) * 72
        else:
            data_object = data_object_uuids_rev[element_id]
            y_pos = data_objects_order.index(data_object) * 72

        node = SubElement(view, 'node', attrib={
            'identifier': node_id,
            'elementRef': element_id,
            'xsi:type': 'Element',
            'x': str(84 + x_offset),
            'y': str(y_pos),
            'w': '120',
            'h': '55',
        })

        processed_nodes.append(element_id)
        
        # Store node identifiers in separate lists
        if instance_type == 'data_object':
            data_object_node_ids.append(node_id)
        else:
            app_component_node_ids.append(node_id)
            
        y_pos += 72  # Update y position for the next node ###
    
        style = SubElement(node, 'style')
        fill_color = SubElement(style, 'fillColor', attrib={'r': '181', 'g': '255', 'b': '255', 'a': '100'})
        line_color = SubElement(style, 'lineColor', attrib={'r': '92', 'g': '92', 'b': '92', 'a': '100'})
        font = SubElement(style, 'font', attrib={'name': 'Sans', 'size': '9'})
        font_color = SubElement(font, 'color', attrib={'r': '0', 'g': '0', 'b': '0'})
    
    # append connections for relationships
    for relationship in relationships:
        source_id = relationship.get('source')
        target_id = relationship.get('target')
        if source_id in data_object_ids and target_id in app_component_ids:
            if source_id not in element_relationships:
                element_relationships[source_id] = []
                source_node_counts[source_id] = 0
            element_relationships[source_id].append(target_id)
            source_node_counts[source_id] += 1

            source_node_id = element_to_node_id[source_id]  # Update this line
            target_node_id = element_to_node_id[target_id]  # Update this line

            connection = SubElement(view, 'connection', attrib={
                'identifier': create_ncname_uuid(),
                'relationshipRef': relationship.get('identifier'),
                'xsi:type': 'Relationship',
                'source': source_node_id,
                'target': target_node_id,
            })

            # append the style element
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
