## Systems and Methods for Big and Unstructured Data Project #1 ##
# Neo4j Database for Tracing People Contacts

Neo4j is a graph database management system developed by Neo4j, Inc. Described by its developers as an ACID-compliant transactional database with native graph storage and processing.

Neo4j is implemented in Java and accessible from software written in other languages using the Cypher query language through a transactional HTTP endpoint, or through the binary "Bolt" protocol.

## Installation
In [scripts](01/scripts/) you can find some useful tools to generate CSV file that can be imported into Neo4J. 
To launch 'generate_dataset.py', make sure to install the dependencies first:
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all that's needed.
```bash
pip -r 01/scripts/requirements.txt
```
Run [generate_dataset.py](01/scripts/generate_dataset.py) and copy the output files in the Neo4J import folder.
```bash
python 01/scripts/generate_dataset.py
```
Afterwards, use the Cypher Load Queries found in [load_queries.txt](01/scripts/load_queries.txt) to populate the dataset.
You can also use some .dump example files in this folder:
## UI

...

## ER-Model
To visualize the Entity-Relation model, go [here](https://www.diagrams.net)

## Datasets Information
Following some information about how nodes are generated.
### People
**People** dataset is made by: **First Name** and **Last Name** retrieve by a function of names package, **Sex**/ by a random choice between the two values, **Phone Number**/**Mail**/**Birth** by a random function, **Positive** is randomly defined by a positive ratio variable. **Last Confirm** by two random function: if Positive is true Last Confirm is within the last fourty-five days, otherwise the function range is from 1/1/2020 to now, **Birthplace** is retrieved from CSV file of Italian Cities and **CIF** is calculated via a function imported from codicefiscale package. 

### Medical Records
The **Medical Records** dataset has **CIF** of the related person, **Risky Subject**/**Covid Vaccinated** by a random choice between ("True","False") **Health Status** by a random choice between ("bad","average","good"). 

### Covid vaccines
The **Covid vaccines** dataset is made with **CIF** of the current person,**Date** by a random function and **Type** by a random choice between ("Pfizer", "Moderna", "Astrazeneca", "Johnson e Johnson") with a restriction of at most 2 vaccines per person.

### Covid tests
The **Covid Tests** dataset is made with **CIF** of the current person, **Date** equals to last confirm of the person if it's positive and **Result** equals to "positive". This cover with at least one test positives. After which a cycle to make more tests per person, with a discrete normal distribution centered in 0 , at most ten per person.

### Places
The **Places** dataset is made of **Code** by a key generator function, and the other values are taken from a CSV file.  A place is later defined as capable  of having rooms, which are then connected to it

### Rooms
The **Rooms** dataset is made of **Room Name** by a custom function, **Capience** by a random function with max set to 150, **Code** taken from place.

### Contacts
The **Contacts** dataset is made of: **CIF1**/**CIF2** by taking two random people, **Date** by random function and **Duration** by a random function with range from 10 minutes to 1439 minutes.

### Visits
The **Visits ** dataset has **CIF1** by taking one random person, **Place**, by taking the code of one random place, **Room** is equals to "None" if the place type don't has a room else by taking a random room ,**Date** by random function and **Duration** by a random function with range from 5 minutes to 720 minutes.

### Lives
The **Lives ** dataset is made by taking one person and link together al least one and at most 6 people

## License
[MIT](https://choosealicense.com/licenses/mit/)
