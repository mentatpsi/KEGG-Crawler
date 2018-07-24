import urllib2
import threading
import string
import pickle
import re
import time

from dbReader import DatabaseReader as DBReader

from mapArea import MapArea,MyHTMLParser


def mapAreaWorker(queue,j):
    print "Map Area Thread %i initalized\n" % (j)
    for pathway in queue:
        curPathwayMap = MapArea(pathway)
        pathwayConnection[pathway] = curPathwayMap.connectMaps 
    print "Map Area Thread %i finished\n" % (j)
def prDictionWorker(queue):
    
    for prURL in queue:
        #print prURL
        curContent = getContents(prURL)
        pathway = prURL.split("/")[-1]
        #print pathway
        #print "=========="
        curReactions = [pathwaysUR(curItem) for curItem in curContent if len(string.split(curItem,"\t")) == 2]
        pRNurlContents.append(curReactions)
        pathwayReact[pathway] = curReactions
        #print curReactions

def dictionWorker(queue, j):
    qLen = len(queue)
    print "KEGG Crawler thread %i initalized\n" % (j)
    s = 0
    last = -1
    for qItem in queue:
        perc = ((s*100)/qLen)
        
        if (perc % 25) == 0:
            if (last != perc):
                last = perc
                print "KEGG Crawler Thread %i at %i percent\n" % (j, perc)
        
        #print qItem
        identifer = qItem
        curDictionary = DBReader("http://rest.kegg.jp/get/" + identifer)
        #print identifer
        idenType = string.split(identifer,":")[0]
        if (idenType == "path"):
            pathwaysD[identifer] = {}
            pathwaysD[identifer].update(curDictionary.diction)
            
            #print pathwaysD[identifer].keys()
        elif (idenType == "rn"):
            reactionsD[identifer] = {}
            reactionsD[identifer].update(curDictionary.diction)
            #print curDictionary.diction
            if "ENZYME" in curDictionary.diction.keys():
                #print "enzymes"
                enzymes = curDictionary.diction["ENZYME"]
                enzymesN = []
                for enzyme in enzymes:
                    if enzyme not in enzymesN:
                        enzymesN.append(enzyme)
                #print enzymesN
                
                reactionsD[identifer]["ENZYME"] = enzymesN
                reactionsD[identifer]["OCC"] = 0
            if "EQUATION" in curDictionary.diction.keys():
                curEquation = curDictionary.diction["EQUATION"][0]
                tempSplit = string.split(curEquation,"<=>")


                indiciesR = [m.start() for m in re.finditer('C', tempSplit[0])] + [m.start() for m in re.finditer('G', tempSplit[0])]
                indiciesP = [m.start() for m in re.finditer('C', tempSplit[1])] + [m.start() for m in re.finditer('G', tempSplit[1])]
                
                reactants = [tempSplit[0][i:i+6] for i in indiciesR]
                products = [tempSplit[1][i:i+6] for i in indiciesP]
                reactionsD[identifer]["REACTANTS"] = reactants
                reactionsD[identifer]["PRODUCTS"] = products
                reactionsD[identifer]["OCC"] = 0
                
                #print reactionsD[identifer]["REACTANTS"]
                #print reactionsD[identifer]["PRODUCTS"]
                
            #print reactionsD[identifer]
            #print reactionsD[identifer].keys()
        elif (idenType == "cpd"):
            #print identifer
            
            compoundsD[identifer] = {}
            #compounds[identifer] = {}
            #compoundsOcc[identifer] = {}
            compoundsD[identifer].update(curDictionary.diction)
            try:
                compoundsD[identifer]["chEBI"] = [string.split(item,":")[1].lstrip() for item in compoundsD[identifer]["DBLINKS"] if item[:5] == "ChEBI" and len(string.split(item,":"))==2][0]
                compoundsD[identifer]["chEBI"] = compoundsD[identifer]["chEBI"].replace(" ","|") 
                #compounds[identifer]["chEBI"] = [string.split(item,":")[1].lstrip() for item in compoundsD[identifer]["DBLINKS"] if item[:5] == "ChEBI" and len(string.split(item,":"))==2][0]
            except:
                #compounds[identifer]["chEBI"] = ""
                compoundsD[identifer]["chEBI"] = ""
            #print compoundsD[identifer]["chEBI"]
            #print curDictionary.diction["
            #compoundsD[identifier].update({"OCC": 0})
            #compoundsOcc.update({identifier:0})
            #compoundsOcc[identifier] = 0
            #compounds[identifier]["OCC"] = 0
            
        elif (idenType == "gl"):
            compoundsD[identifer] = {}
            #compounds[identifer] = {}
            #compoundsOcc[identifer] = {}
            compoundsD[identifer].update(curDictionary.diction)

            try:
                compoundsD[identifer]["chEBI"] = [string.split(item,":")[1].lstrip() for item in compoundsD[identifer]["DBLINKS"] if item[:5] == "ChEBI" and len(string.split(item,":"))==2][0]
                compoundsD[identifer]["chEBI"] = compoundsD[identifer]["chEBI"].replace(" ","|") 
                #compounds[identifer]["chEBI"] = [string.split(item,":")[1].lstrip() for item in compoundsD[identifer]["DBLINKS"] if item[:5] == "ChEBI" and len(string.split(item,":"))==2][0]
            except:
                #compounds[identifer]["chEBI"] = ""
                compoundsD[identifer]["chEBI"] = ""
            
            
            #compoundsD[identifer]["chEBI"] = [string.split(item,":")[1].lstrip() for item in compoundsD[identifer]["DBLINKS"] if item[:5] == "ChEBI" and len(string.split(item,":"))==2][0]
            #compounds[identifer]["chEBI"] = [string.split(item,":")[1].lstrip() for item in compoundsD[identifer]["DBLINKS"] if item[:5] == "ChEBI" and len(string.split(item,":"))==2][0]
            
            #compoundsD[identifier].update({"OCC": 0})
            #compoundsOcc.update({identifier:0})
            #compoundsOcc[identifier] = 0
        s+=1
            #compounds[identifier]["OCC"] = 0
    print "KEGG Crawler Thread %i finished\n" % (j)
    return 0
def makeCSV(iType, dictionaries):
    line = lambda n: "%s" % n
    curStr = ""
    idenMod = lambda current: current[current.find(":")+1:]
    dictionary = {}
    if iType == "CG":
        header = '"KEGG ID","Names"\n'
        line = lambda data : '"%s","%s"\n' % (idenMod(key), dictionary[key])
        dictionary = dictionaries[0]
    elif iType == "P":
        header = '"Pathway ID","Pathway Name","KEGG ID"\n'
        line = lambda data : '"%s","%s"\n' % (idenMod(key), dictionary[key])
        dictionary = dictionaries[1]
    elif iType == "R":
        header = '"id","reaction id","reaction kegg","reactants","products","reversible","EC #List"\n'
        line = lambda data : '"%s","%s"\n' % (idenMod(key), dictionary[key])
        dictionary = dictionaries[2]
        
    curStr += header
    
    for key in sorted(dictionary.keys()):
        curStr += '"%s","%s"\n' % (idenMod(key), dictionary[key])

    return curStr


def makeRCSV(rDictionary):
    curStr = '"Reaction KEGG ID","Reactants","Products","Reversability","EC list","Occurences","Names"\n'
    i = 0
    for reaction in sorted(rDictionary.keys()):
        reactionT = reaction[3:]
        if "ENZYME" in rDictionary[reaction].keys():
            ecListStr = string.join(rDictionary[reaction]["ENZYME"],"|")
        else:
            ecListStr = ""
        if "NAME" in rDictionary[reaction].keys():
            curName = string.join(rDictionary[reaction]["NAME"],"|")
        else:
            curName = ""
                       
        reactantsStr = string.join(rDictionary[reaction]["REACTANTS"],"|")
        productsStr = string.join(rDictionary[reaction]["PRODUCTS"],"|")

        metabolites = rDictionary[reaction]["REACTANTS"] + rDictionary[reaction]["PRODUCTS"]
        rDictionary[reaction]["METABOLITES"] = metabolites
        reactionsD[reaction]["METABOLITES"] = metabolites

        for metabolite in metabolites:
            #print metabolite
            prefix = lambda metabolite: "gl:" if metabolite[0] == "G" else "cpd:" 
            metaName = prefix(metabolite) + metabolite
            #print metaName
            
            #compoundsD[metaName]["OCC"]+=1
            if metaName in compoundsOcc.keys():
                compoundsOcc[metaName]+=1
            else:
                compoundsOcc[metaName]=1
        
        occurences = reactionsOcc[reaction]
        curStr += '"%s","%s","%s","1","%s","%i","%s"\n' % (reactionT,reactantsStr,productsStr,ecListStr, occurences,curName)        
        i+=1
    return curStr
        

def makePWCSV(pathwayconnections):
    curStr = '"Pathway1 KEGG","Pathway2 KEGG","Connecting reactions","Connection metabolites"\n'
    for pathway in sorted(pathwayconnections.keys()):
        cPathways = pathwayconnections[pathway]
        #print pathway
        
        for cPathway in cPathways:
            if cPathway[:5] != "path:":
                ctPathway = "path:" + cPathway
            else:
                ctPathway = cPathway
            cReactionsStr = ""
            cMeabolitesStr = ""
            
            if pathway[:5] != "path:":
                tPathway = "path:" + pathway
            else:
                tPathway = pathway
            if ((tPathway in pathwayReact.keys()) and (ctPathway in pathwayReact.keys())): 
                cReactions = [reaction[3:] for reaction in pathwayReact[tPathway] if reaction in pathwayReact[ctPathway]]
                cReactionsStr = string.join(cReactions,"|")
                cMetabolites = []
            
                for reaction in cReactions:
                    tReaction = "rn:" + reaction
                    if tReaction in reactionsD.keys():
                        for metabolite in reactionsD[tReaction]["METABOLITES"]:
                            if metabolite not in cMetabolites:
                                cMetabolites.append(metabolite)
                cMetabolitesStr = string.join(cMetabolites,"|")
            #[metabolite for metabolite in rDictionary[reaction]["METABOLITES"] if metaolite in cReactions]
            
            curStr+= '"%s","%s","%s","%s"\n' % (pathway[5:], cPathway,cReactionsStr,cMetabolitesStr)

    return curStr

def makeRPCSV(prnDictionary):
    curStr = '"Pathway ID","Pathway KEGG","Reaction KEGG ID"\n'
    i = 0
    j = 0
    for pathway in sorted(prnDictionary.keys()):
        keggRL = prnDictionary[pathway]
        for keggR in keggRL:
            #reactionsD[keggR]
            reactionsOcc[keggR]+=1
            reactionsD[keggR]["OCC"]+=1
            curStr += '"%i","%s","%s"\n' % (i,pathway[5:],keggR[3:])        
            j += 1
        i+=1
        j=0
    return curStr
             
def makePCSV(dictionary):
    curStr = '"Pathway ID","Pathway Name","KEGG ID"\n'
    
    idenMod = lambda current: current[current.find(":")+1:]
    i = 0
    for key in sorted(dictionary.keys()):
        curStr += '"%i","%s","%s"\n' % (i, dictionary[key], idenMod(key))
        i += 1
    return curStr
   
def makeCGCSV(dictionary):
    curStr = '"KEGG ID","Names","chEBI","Occurence"\n'
    idenMod = lambda current: current[current.find(":")+1:]
    for key in sorted(dictionary.keys()):
        metabolite = key
        prefix = lambda metabolite: "gl:" if metabolite[0] == "G" else "cpd:" 
        metaName = prefix(metabolite) + metabolite
        if "chEBI" in compoundsD[key].keys():
            chEBI = compoundsD[key]["chEBI"]
        else:
            chEBI = ""
        curStr += '"%s","%s","%s","%i"\n' % (idenMod(key), dictionary[key],chEBI,compoundsOcc[key])
    return curStr

def getContents(url):
    i = 0
    contents = 0
    while ((contents ==0) and (i < 5)):
        try:
            contents = urllib2.urlopen(url).readlines()
        except:
            contents = 0
        i+= 1
    return contents


if __name__ == "__main__":
    pathwaysUrl = "http://rest.kegg.jp/list/pathway"
    compoundsUrl = "http://rest.kegg.jp/list/compound"
    reactionsUrl = "http://rest.kegg.jp/list/reaction"
    glycanUrl = "http://rest.kegg.jp/list/glycan"


    listUrls = [pathwaysUrl, compoundsUrl, reactionsUrl, glycanUrl]

    #http://rest.kegg.jp/link/rn/map00010

    listsOrganized = []

    pathwaysD = {}
    compoundsD = {}
    reactionsD = {}

    pRnURL = lambda path: "http://rest.kegg.jp/link/rn/" + path

    compoundsOcc = {}
    
    
    
    
    
    lists = [getContents(url) for url in listUrls]

    for content in lists:
        listsOrganized.append([line.strip("\n").split("\t") for line in content])

    #the following joins compound names in format name[0]|name[1]
    joinNames = lambda compoundNames: string.join([names.lstrip(" ").rstrip(" ")
                     for names in string.split(compoundNames,";")],"|")

    alterNames = lambda compoundNames: compoundsName.rstrip(" ").replace("; ","|")

    #the following takes advantage of a type:value style representation
    luKeypair = lambda current: (current[0][current[0].find(":")+1:],current[1])
    keypair = lambda current: (current[0],current[1])

    pathways = dict((keypair(line) for line in listsOrganized[0])) 

    rnURLs = [pRnURL(pathway) for pathway in sorted(pathways.keys())]

    rnURLsD = {}
    
    for pathway in sorted(pathways.keys()):
        rnURLsD.update({pathway:pRnURL(pathway)})
        
    pathwayrnUrl = {}
    
    pRNurlContents = []

    pathwayReact = {}

    pathwayConnection = {}

    cores = 8
    
    pwcQueue = [[]*cores for item in range(cores)]

    answ = raw_input("Run Map Area Workers? ")

    if answ == "Y" or answ == "y":
        mapAreaPrompt = True
    else:
        mapAreaPrompt = False

    if mapAreaPrompt:
        pwcThreads = []
        i = 0
        for pathway in sorted(pathways.keys()):
            #prURL = rnURLsD[pathway]
            pwcQueue[i%cores].append(pathway)
            i += 1
        j = 0
        for queue in pwcQueue:
            t = threading.Thread(target=mapAreaWorker, args=(queue,j))
            pwcThreads.append(t)
            j+=1

        for thread in pwcThreads:
            thread.start()

        for thread in pwcThreads:
            thread.join()
        
    
    #for pathway in sorted(pathways.keys()):
        #curPathwayMap = MapArea(pathway)
        #pathwayConnection[pathway] = curPathwayMap.connectMaps 
    
    pathwaysUR = lambda content: string.split(content.rstrip("\n"),"\t")[1] 

    
    
    prThreads = []
    prQueue = [[]*cores for item in range(cores)]

    i = 0
    for pathway in sorted(rnURLsD.keys()):
        prURL = rnURLsD[pathway]
        prQueue[i%cores].append(prURL)
        i += 1

    for queue in prQueue:
        t = threading.Thread(target=prDictionWorker, args=(queue,))
        prThreads.append(t)

    for thread in prThreads:
        thread.start()

    for thread in prThreads:
        thread.join()
        
        #print pathwayReact
            

    with open("pathwaysRDa.pkl","wb") as outputPathways:
            pickle.dump(pathwayReact, outputPathways)    


    

    compounds = {}
    #lookupCompounds = {}
    
    for line in listsOrganized[1]:
        (key, value) = keypair(line)
        #(key1, value1) = luKeypair(line)
        value = joinNames(value)
        compounds.update({key:value})
        #lookupCompounds.update({key1:value1}) 

    for line in listsOrganized[3]:
        (key, value) = keypair(line)
        value = joinNames(value)
        compounds.update({key:value})
     
    reactions = dict((keypair(line) for line in listsOrganized[2]))

    reactionsOcc = {}
    
    
    


    answ = raw_input("Are you sure you want to continue? ")

    if (answ == "Y" or answ == "y"):
        threads = []
        cores = 8
        
        queues = [[]*cores for i in range(cores)]
        i = 0
        for reaction in sorted(reactions.keys()):
            queues[i%cores].append(reaction)
            i+=1

        i = 0
        for pathway in sorted(pathways.keys()):
            queues[i%cores].append(pathway)
            i+=1

        for metabolite in sorted(compounds.keys()):
            queues[i%cores].append(metabolite)
            i+=1

        j = 0
        for queue in queues:
            t = threading.Thread(target=dictionWorker, args=(queue,j))
            threads.append(t)
            j+=1
            
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        print "Gotten past it"

        

        for identifer in sorted(compounds.keys()):
            compoundsOcc[identifer] = 0

        for identifer in sorted(reactionsD.keys()):
            reactionsOcc[identifer] = 0        

        #for pathway in sorted(pathways.keys()):
            #reactionsOcc[identifer] = 0  


        pCSV = makePCSV(pathways)

        pC = open("pathways.csv","w")
        pC.write(pCSV)
        pC.close()

        rpCSV = makeRPCSV(pathwayReact)

        pRC = open("pathways_reactions.csv","w")
        pRC.write(rpCSV)
        pRC.close()
        
        
        rCSV = makeRCSV(reactionsD)
        rCS = open("reactions.csv","w")
        rCS.write(rCSV)
        rCS.close()
        
        cgCSV = makeCGCSV(compounds)

        CG = open("metabolites.csv","w")
        CG.write(cgCSV)
        CG.close()



        if mapAreaPrompt:
            pwCSV = makePWCSV(pathwayConnection)

            PW = open("pathway_connection.csv","w")
            PW.write(pwCSV)
            PW.close()
        
        
        
        

        with open("pathwaysA.pkl","wb") as outputPathways:
            pickle.dump(pathways, outputPathways)    

        with open("compoundsA.pkl","wb") as outputCompounds:
            pickle.dump(compounds, outputCompounds)
            
        with open("reactionsA.pkl","wb") as outputReactions:
            pickle.dump(reactions, outputReactions)    


        with open("pathwaysD.pkl","wb") as outputPathways:
            pickle.dump(pathwaysD, outputPathways)    

        with open("compoundsD.pkl","wb") as outputCompounds:
            pickle.dump(compoundsD, outputCompounds)
            
        with open("reactionsD.pkl","wb") as outputReactions:
            pickle.dump(reactionsD, outputReactions)
    
    
        
