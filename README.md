KEGG Crawler
====
Author: Shay Maor

KEEG Crawler is a Python script that uses KEEGs REST API to first attain a list of pathways, as well as their respective chemical reactions and metabolites. It utilizes its threading module to make the crawler process parallel, minimizing bandwidth latency issues. It utilizes 8 threads with stacks on each thread of the target crawls. It also utilizes the urllib2 module to initiate the crawls. The last module it uses is HTMLParser which comes from the Beautiful Soup library. This requires a pip install of beautiful soup (after pip is installed, this can be done through the cmd "pip install beautifulsoup"). 

The main crawler has a progress indicator and presents a message when each thread makes 50% progress and when it reaches completion. The script itself runs for approximately 20-30 minutes on a cable connection.

It is divided into 3 different files:

crawler.py is responsible for the crawls. It utilizes the rest of the scripts to perform the crawl.

dbReader.py utilizes pattern recognition to create an object inheriting a dictionary type containing deeper information. This is useful for later applications as some information might prove helpful for future endeavors. In the case of metabolites, this includes entries such as formula, molecular weight, reactions involved in, metabolic pathways, enzymes involved, as well as some information on external database fields (such as ChEBI and PubChem identifiers). The instance can then be called such as dbInstance['DBLINKS'] or dbInstance['ENZYME']

mapArea.py utilizes html parsing of the maparea section of the pathway maps. It was used for producing the secondary csv called pathway_connection.csv, explained later. It is the only script which uses HTMLParser, since it examines the <maparea> tags within the html source found in pathways to look for metabolite nodes.


It generates 5 csv's as well as python pickle files (dictionaries that can be imported). A later release will contain the python scripts that show proper usage of the pickle files. One of the Pickle files (compoundsD, a more complete collection of data on each metabolite) usually contains approximately 70 MB.

A prompt will take place after maparea threads have completed. This is to avoid the heavier, more lengthy crawl from taking place in case testing functions were provided prior.

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
