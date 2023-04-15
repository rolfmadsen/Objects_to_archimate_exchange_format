# Archimate Exchange Format

The purpose of this repository is to generate a valid Archimate Exchange Format XML file from a CSV-file of source nodes, representing Arhcimate application component elements, and target nodes, representing Archimate application dataObject elements, connected by Archimate association relationships.

The main.py script will take the CSV-file, containing column A as the source nodes and column B as the target nodes, as input and outputs an XML file in the Archimate Exchange Format.

## Archimatetool (Archi) application
The Archi application can be used to view the model for further manipulation in Archimate:
1. Download https://www.archimatetool.com/
2. Run Archi
3. File > Import > Model from Archimate Open Exchange File
4. Select output.xml file
5. Open the Models windows
6. Open the Views folder
7. Right click "Application Cooperation" view
8. Select "Open view"

## Gephi application

If the model is very large you can transform the Archimate Exchange Format XML file by running the gephi.py script which will output the two gephi_nodes.csv and gephi_edges.csv files which can be imported from the Gephi application.
