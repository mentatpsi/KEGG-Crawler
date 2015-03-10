import urllib2
import fnmatch, re
import string
import sys

class DatabaseReader(dict):
    """This class is for the importing of flat database files"""
    def __init__(self, url=None,term=None):
        
        if url:
            self.url = url
            self.diction = {}
            self.wholeParse()
            dict.__init__(self,self.diction)
            #self.parsed = 0
    


    def add(self,key,value):
        if (key in self.diction.keys()):
            if (value in self.diction[key]):
                pass
            else:
                self.diction[key] = self.diction[key] + value
        else:
            self.diction[key] = value
    def get(self,key):
        return self.diction[key] 

  
 
    def wholeParse(self):
        text = ""
        i = 0
        while ((text == "") and (i < 5)):
            try:
                text = urllib2.urlopen(self.url).readlines()
            except:
                text = ""
            i+= 1
        i = 0
        cur = ""
        past = ""
        tempSplit = []
        for line in text:
            #tempSplit = string.split(line,"\t")
            #print line
            if (line.find("///") != -1):
                if (past == "cont"):
                    #print tempSplit[1:]
                    self.add(tempSplit[0],tempSplit[1:])
            if (fnmatch.fnmatch(line,"[A-Z][A-Z]*")):
                if (past == "cont"):
                    #self.diction[tempSplit[0]] = tempSplit[1:]
                    self.add(tempSplit[0],tempSplit[1:])
                 #print tempSplit
                past = "title"
                line = line.replace("  ","\t")
                line = line.replace("\n","")
                line = line.replace(";","")
                tempSplit = [ti.lstrip().rstrip() for ti in string.split(line,'\t') if ti!='']
                #print tempSplit
                if (i == 0):
                    pass
                    #print "Title; type"
                    #templateT = tempSplit[2] 
                else:
                    pass
                    #print "Title" 
                #print line
                if fnmatch.fnmatch(line,"DESCRIPTION*"):
                    key = tempSplit[0][:11]
                    value = [tempSplit[0][12:]]
                    self.add(key,value)
                    #self.diction[tempSplit[0][:11]] = [tempSplit[0][12:]]
                    #print "Formula"
                elif fnmatch.fnmatch(line,"PATHWAY_MAP*"):
                    key = tempSplit[0][:11]
                    value = [tempSplit[0][12:]]
                    self.add(key,value)
                else:
                        curTitle = tempSplit[0]
                        key = tempSplit[0]
                        value = tempSplit[1:]
                        self.add(key,value)             
            else:
                if (past == "title"):
                    pass
                    #print "Continuation"
                line = line.replace("  ","\t")
                line = line.replace("\n","")
                line = line.replace(";","")
                
                tempSplit = tempSplit + [ti.lstrip().rstrip() for ti in string.split(line,"\t") if ti!='']      
                
                #print line
                #print tempSplit
                #print " "
                past = "cont"
            i += 1      
        self.parsed = 1



if __name__ == "__main__":
   #print len(sys.argv)
   if (len(sys.argv)) >= 2:
        url = "http://rest.kegg.jp/get/" + str(sys.argv[1])
        print url
        dbT = DatabaseReader(url)
        print dbT.diction.keys()
        if (len(sys.argv)) >= 3:
            key = sys.argv[2]
            print dbT.diction[key]
   else:
        print "Compound"
        dbC = DatabaseReader("http://rest.kegg.jp/get/cpd:C00001")
        
        print dbC.diction.keys()
        print "******************************************************************************************"
        print "Reaction"
        dbR = DatabaseReader("http://rest.kegg.jp/get/rn:R00001")
        print dbR.diction.keys()
        print "******************************************************************************************"
        print "Map"
        dbM = DatabaseReader("http://rest.kegg.jp/get/map00010")
        print dbM.diction.keys()
        print "******************************************************************************************"
