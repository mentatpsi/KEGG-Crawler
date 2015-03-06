KEEG Crawler
====
Author: Shay Maor

KEEG Crawler is a Python script that uses KEEGs REST API to first attain a list of pathways, as well as their respective chemical reactions and metabolites. It utilizes its multithreading library to make the crawler process parallel, minimizing bandwidth latency issues. It utilizes 8 threads with stacks on each thread of the target crawls. It also utilizes the urllib2 library to utilize the crawls. It has a progress indicator and presents a message when each thread makes 50% progress and when it reaches completion. The script itself runs for approximately 20-30 minutes on a cable connection.

It is divided into 3 different files:

mainCrawler.py is responsible for the crawls.

dbReader.py utilizes pattern recognition to create an object inheriting a dictionary of deeper information. This is useful for later applications as some information might prove helpful.

mapArea.py utilizes html parsing of the maparea section of the pathway maps. It was used for producing the secondary csv called pathway_connection.csv, explained later. 


It generates 5 csv's as well as python pickle files (dictionaries that can be imported). A later release will contain the python scripts that show proper usage of the pickle files. One of the Pickle files (compoundsD, a more complete ) contains

A prompt will take place after maparea threads have taken place. This is to avoid the heavier, more lengthy crawl from taking place in case testing functions were provided prior.

The 4 dominant CSVs created are as follows.

pathways.csv
"Pathway ID","Pathway Name","KEGG ID"

metabolites.csv
"KEGG ID","Names","chEBI","Occurence"

reactions.csv
"Reaction KEGG ID","Reactants","Products","Reversability","EC list","Occurences","Names"

pathways_reactions.csv
"Pathway ID","Pathway KEGG","Reaction KEGG ID"


The secondary CSV it creates:
pathway_connection.csv
"Pathway1 KEGG","Pathway2 KEGG","Connecting reactions","Connection metabolites"

this was for trying to hone down some possible connectivity from one pathway to another. 