# Archimate Exchange Format

The node_to_archimage_exchange_format.py script will take a CSV-file as input and outputs an XML file in Archimate Exchange Format.

## Archi
The Archi application can then be used to view the model:
1. Download https://www.archimatetool.com/
2. Run Archi
3. File > Import > Model from Archimate Open Exchange File
4. Select output.xml file
5. Open the Models windows
6. Open the Views folder
7. Right click "Application Cooperation" view
8. Select "Open view"

## Gephi

Run the gephi.py script to transform the archimate_exchange_format.xml file to the two gephi_nodes.csv and gephi_edges.csv files which can be imported from the Gephi application.
