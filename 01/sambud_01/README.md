# what this is

This is a simple graph visualization app for a project at Polimi

# how do i run this

it'll take a while:

- install yarn
- run `yarn` to install dependencies, `yarn start` to start the webapp
- get a working instance of a neo4j database, fill in a file called `secrets.json` with this structure:

````json
{
  "NEO4J_HOST_URI": "bolt://localhost:7687",
  "NEO4J_USER": "neo4j",
  "NEO4J_PASSWORD": "*******",
  "NEO4J_SCHEME": "bolt",
  "NEO4J_FULL_URI": "bolt://localhost:7687"
}


````
