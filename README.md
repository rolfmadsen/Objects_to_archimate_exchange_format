# Archimate Exchange Format

The purpose of this repository is to generate a valid Archimate Exchange Format XML file from a CSV-file of source nodes, representing Arhcimate application component elements, and target nodes, representing Archimate application dataObject elements, connected by Archimate association relationships.

The main.py script will take the CSV-file, containing column A as the source nodes and column B as the target nodes, as input and outputs an XML file in the Archimate Exchange Format.

## Archimatetool (Archi) application
The Archi application can be used to view the model for further manipulation in Archimate:
1. Download and install https://www.archimatetool.com/download
2. Run Archi
3. File > Import > Model from Archimate Open Exchange File
4. Select output.xml file
5. Open the Models windows
6. Open the Views folder
7. Right click "Application Cooperation" view
8. Select "Open view"

## Gephi application

If the model is very large you can transform the Archimate Exchange Format XML file by running the gephi.py script which will output the two gephi_nodes.csv and gephi_edges.csv files which can be imported from the Gephi application.

### Gephi
1. Download and install https://gephi.org/users/install/
2. Run Gephi

#### Import nodes
1. Select File > New Project
2. Open the Data Laboratory tab
3. Open Import Spreadsheet
4. Select and open the gephi_nodes.csv file
5. Select the separator: Comma
6. Select Import as: Nodes table
7. Select finish
8. Select "Append to existing workspace"
9. Select OK

#### Import edges
1. Open Import Spreadsheet
2. Select and open the gephi_edges.csv file
3. Select the separator: Comma
4. Select Import as: Edges table
5. Select finish
6. Select "Append to existing workspace"
7. Select OK

#### View graph
1. Select Window > Graph
2. Select the "**T**" icon at the buttom left of the Graph window to display the node labels
