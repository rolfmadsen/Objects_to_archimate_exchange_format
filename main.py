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
def create_model():
    model = Element('model', {'xmlns': 'http://www.opengroup.org/xsd/archimate/3.0/', 'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'xsi:schemaLocation': 'http://www.opengroup.org/xsd/archimate/3.0/ http://www.opengroup.org/xsd/archimate/3.1/archimate3_Diagram.xsd', 'identifier': create_ncname_uuid(),})
    SubElement(model, 'name', {'xml:lang': 'en'}).text = 'CSV source and target transformation to Archimate Exchange Format'
    return model
def create_model_elements(model):
    elements = SubElement(model, 'elements')
    return elements
def create_model_elements_element_applicationComponent(elements, app_component_uuids, app_component, app_component_ids, organization_item):
    element_applicationComponent = SubElement(elements, 'element', attrib={'identifier': app_component_uuids[app_component], 'xsi:type': 'ApplicationComponent',})    
    SubElement(element_applicationComponent, 'name', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en'}).text = app_component
    app_component_ids.append(element_applicationComponent.get('identifier'))
    SubElement(organization_item, 'item', attrib={'identifierRef': element_applicationComponent.get('identifier')})
    return element_applicationComponent
def create_model_elements_element_dataObject(elements, data_object_uuids, data_object, data_object_ids, organization_item):
    element_dataObject = SubElement(elements, 'element', attrib={ 'identifier': data_object_uuids[data_object], 'xsi:type': 'DataObject',})
    SubElement(element_dataObject, 'name', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en'}).text = data_object
    data_object_ids.append(element_dataObject.get('identifier'))
    SubElement(organization_item, 'item', attrib={'identifierRef': element_dataObject.get('identifier')})
    return element_dataObject
def create_model_relationships(model):
    relationships = SubElement(model, 'relationships')
    return relationships
def relationships_relationship(relationships, data_object_id, app_component_id, relationship_ids):
    relationship = SubElement(relationships, 'relationship', attrib={'identifier': create_ncname_uuid(), 'source': data_object_id, 'target': app_component_id, 'xsi:type': 'Association',})
    return relationship
def create_model_organizations(model):
    organizations = SubElement(model, 'organizations')
    return organizations
def create_model_organizations_item_relations(organizations):
    organizations_item_relation = SubElement(organizations, 'item')
    SubElement(organizations_item_relation, 'label', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en'}).text = 'Relations'
    return organizations_item_relation
def create_model_organization_item_views(organizations, view):
    organizations_item_view = SubElement(organizations, 'item')
    SubElement(organizations_item_view, 'label', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en'}).text = 'Views'
    SubElement(organizations_item_view, 'item', {'identifierRef': view.get('identifier')})
    return organizations_item_view
def create_model_organization_item_application(organizations):
    organizations_item_view = SubElement(organizations, 'item')
    SubElement(organizations_item_view, 'label', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en'}).text = 'Application'
    return organizations_item_view
def create_model_views(model):
    views = SubElement(model, 'views')
    return views
def create_model_views_diagrams(views):
    diagrams = SubElement(views, 'diagrams')
    return diagrams
def create_model_views_diagrams_view(diagrams):
    view = SubElement(diagrams, 'view', attrib={'identifier': create_ncname_uuid(), 'xsi:type': 'Diagram', 'viewpoint': 'Application Cooperation',})
    SubElement(view, 'name', attrib= {'{http://www.w3.org/XML/1998/namespace}lang': 'en'}).text = 'Application Cooperation'
    return view
def create_views_diagrams_view_node(view, node_id, element_id, x_offset, y_pos):
    node = SubElement(view, 'node', attrib={ 'identifier': node_id, 'elementRef': element_id, 'xsi:type': 'Element', 'x': str(84 + x_offset), 'y': str(y_pos), 'w': '120', 'h': '55',})
    return node
def create_views_diagrams_view_connection(view, relationship, source_node_id, target_node_id):
    connection = SubElement(view, 'connection', attrib={'identifier': create_ncname_uuid(), 'relationshipRef': relationship.get('identifier'), 'xsi:type': 'Relationship', 'source': source_node_id, 'target': target_node_id,})
    return connection
def create_views_diagrams_view_connection_style(connection):
    style = SubElement(connection, 'style')
    SubElement(style, 'lineColor', attrib={'r': '0', 'g': '0', 'b': '0'})
    font_name = SubElement(style, 'font', attrib={'name': 'Sans', 'size': '9'})
    SubElement(font_name, 'color', attrib={'r': '0', 'g': '0', 'b': '0'})
    return style
def create_views_diagrams_view_node_style(node):
    style = SubElement(node, 'style')
    SubElement(style, 'fillColor', attrib={'r': '181', 'g': '255', 'b': '255', 'a': '100'})
    SubElement(style, 'lineColor', attrib={'r': '92', 'g': '92', 'b': '92', 'a': '100'})
    font = SubElement(style, 'font', attrib={'name': 'Sans', 'size': '9'})
    SubElement(font, 'color', attrib={'r': '0', 'g': '0', 'b': '0'})
    return style

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
    
    # Create XML structures
    model = create_model()
    elements = create_model_elements(model)
    
    relationships = create_model_relationships(model)
    
    organizations = create_model_organizations(model)
    organizations_item_relation = create_model_organizations_item_relations(organizations)
    organization_item = create_model_organization_item_application(organizations)
    
    views = create_model_views(model)
    diagrams = create_model_views_diagrams(views)
    view = create_model_views_diagrams_view(diagrams)
    create_model_organization_item_views(organizations, view)


    ### Create the views element under organization > item


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
            
            relationship_ids = []
            relationship = relationships_relationship(relationships, data_object_id, app_component_id, relationship_ids)
            relationship_ids.append(relationship.get('identifier'))
            
            SubElement(organizations_item_relation, 'item', attrib={'identifierRef': relationship.get('identifier')})


    app_components_order = list(app_components.keys())
    data_objects_order = list(data_objects.keys())

    for app_component in app_components:
        create_model_elements_element_applicationComponent(elements, app_component_uuids, app_component, app_component_ids, organization_item)


    for data_object in data_objects:
        create_model_elements_element_dataObject(elements, data_object_uuids, data_object, data_object_ids, organization_item)

    app_component_uuids_rev = {v: k for k, v in app_component_uuids.items()}
    data_object_uuids_rev = {v: k for k, v in data_object_uuids.items()}
    data_object_node_ids = []
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

    # Set coordinates for nodes
    processed_nodes = []
    for element_id in set(sorted_data_object_ids + sorted_app_component_ids):
        if element_id in processed_nodes:
            continue

        instance_type = 'app_component' if element_id in app_component_ids else 'data_object'

        node_id = create_ncname_uuid()
        element_to_node_id[element_id] = node_id
        
        # append an offset to the x-axis position if it's an application component
        x_offset = 250 if instance_type == 'app_component' else 0
            
        # Calculate the y position based on the index in the order lists
        if instance_type == 'app_component':
            app_component = app_component_uuids_rev[element_id]
            y_pos = app_components_order.index(app_component) * 72
        else:
            data_object = data_object_uuids_rev[element_id]
            y_pos = data_objects_order.index(data_object) * 72

        # Create the node element under views > diagrams > view
        node = create_views_diagrams_view_node(view, node_id, element_id, x_offset, y_pos)

        processed_nodes.append(element_id)
        
        # Store node identifiers in separate lists
        if instance_type == 'data_object':
            data_object_node_ids.append(node_id)
        else:
            app_component_node_ids.append(node_id)
            
        y_pos += 72  # Update y position for the next node ###
    
        # Create the style element under views > diagrams > view > node
        create_views_diagrams_view_node_style(node)
    
    # Append connections for relationships
    for relationship in relationships:
        source_id = relationship.get('source')
        target_id = relationship.get('target')
        if source_id in data_object_ids and target_id in app_component_ids:
            if source_id not in element_relationships:
                element_relationships[source_id] = []
                source_node_counts[source_id] = 0
            element_relationships[source_id].append(target_id)
            source_node_counts[source_id] += 1

            source_node_id = element_to_node_id[source_id]
            target_node_id = element_to_node_id[target_id]

            # Add a connection element to views > diagrams > view
            connection = create_views_diagrams_view_connection(view, relationship, source_node_id, target_node_id)
            create_views_diagrams_view_connection_style(connection)

    # Save the generated XML to a file
    with open('output.xml', 'w', encoding='utf-8') as f:
        f.write(prettify(model))
        print(f"The model was saved to: output.xml")
if __name__ == '__main__':
    csv_file = 'input.csv'
    generate_aef_from_csv(csv_file)
