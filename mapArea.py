import urllib2
import threading
import string
import pickle
import re
import time


from HTMLParser import HTMLParser


from dbReader import DatabaseReader as DBReader


class MapArea:
    def __init__(self, pathway):
        self.mapAreaUrl = "http://www.genome.jp/kegg-bin/show_pathway?map=%s&show_description=show" % (pathway[5:])
        self.connectMaps = []
        self.parse()
    def parse(self):
        temp = string.join(getContents(self.mapAreaUrl),"")
        parser = MyHTMLParser()
        #print temp
        parser.feed(temp)
        self.connectMaps = parser.maps


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mapArea = 0
        self.maps = []
    def handle_starttag(self, tag, attrs):
        if tag == "map":
            self.mapArea = 1
        if (self.mapArea == 1):
            #print "Encountered a start tag:", tag
            #print "With attributes:", attrs
            for attr in attrs:
                if attr[0] == "title":
                    if attr[1][:3] == "map":
                        area = attr[1][:8]
                        #print area
                        self.maps.append(area)
            
    def handle_endtag(self, tag):
        if tag == "map":
            self.mapArea = 0
        if (self.mapArea == 1):
            pass
            #print "Encountered an end tag :", tag
    def handle_data(self, data):
        if (self.mapArea == 1):
            pass
            #print "Encountered some data  :", data

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
    
    
    mapAreaUrl = lambda path : "http://www.genome.jp/kegg-bin/show_pathway?map=%s&show_description=show" % (path)

    
    
    
    lists = [getContents(url) for url in listUrls]

    for content in lists:
        listsOrganized.append([line.strip("\n").split("\t") for line in content])

    #the following joins compound names in format name[0]|name[1]
    joinNames = lambda compoundNames: string.join([names.lstrip(" ").rstrip(" ")
                     for names in string.split(compoundNames,";")],"|")


    #the following takes advantage of a type:value style representation
    luKeypair = lambda current: (current[0][current[0].find(":")+1:],current[1])
    keypair = lambda current: (current[0],current[1])

    pathways = dict((keypair(line) for line in listsOrganized[0]))

    
    
    maUrls = [mapAreaUrl(path[5:]) for path in sorted(pathways.keys())]


    #contents = [string.join(getContents(url),"") for url in maUrls]

    temp = string.join(getContents(maUrls[0]),"")
    
    for path in sorted(pathways.keys())[:5]:
        tempPath = MapArea(path)
                        


    
    

    
