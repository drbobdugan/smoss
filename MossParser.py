# Class MossParser
# This class is designed to take a url as input and creates a csv file of results from MOSS in the same directory
# as this program
import urllib
import urllib.request
from html.parser import HTMLParser
from Config import Config


class MossParser ():
    def __init__(self, csvFileName):
        self.csvFileName = csvFileName
        self.config = Config()

    # Parse a single URL
    def parse(self, url):
        # Get the html text from the URL
        html = self.getHtml(url)

        # Process the html into table strings
        tableStrings = self.processHtml(html)

        # Process the table strings into csv strings
        csvStrings = self.processTableStrings(tableStrings)
        self.writeToCsv(csvStrings)

    # Parse multiple URLs
    def parseMultiple(self, urls):
        counter = 0
        for url in urls:
            html = self.getHtml(url)
            tableStrings = self.processHtml(html)
            csvStrings = self.processTableStrings(tableStrings)
            if (counter != 0):
                self.appendToCsv(csvStrings)
            else:
                self.writeToCsv(csvStrings)
                counter = 1

    def appendToCsv(self, csvStrings):
        f = open(self.csvFileName, 'a')
        for item in csvStrings:
            for value in item[:-1]:
                f.write(value + ",")
            f.write(item[-1])
            f.write('\n')
        f.close()

    def writeToCsv(self, csvStrings):
        f = open(self.csvFileName, 'w')
        f.write("User1,FileName1,Match1,User2,FileName2,Match2,Lines_Matched,URL")
        f.write('\n')
        for item in csvStrings:
            for value in item[:-1]:
                f.write(value+",")
            f.write(item[-1])
            f.write('\n')
        f.close()

    # Gets the name of the student for a given file name
    def getName(self, fileName):
        values=fileName.split("_")
        if values[0] == "previous":
            return values[1]
        else:
            return values[0]

    # Returns True if the URL is valid, else returns False
    def testUrl(self, url):
        request = urllib.request.Request(url)

        # Attempt to access the URL
        try:
            response = urllib.request.urlopen(request) # response now contains the HTML
            return True

        # Create an exception and return False if the URL is not valid
        except:
            return False

    def processHtml(self, html):
        # Parse until table
        htmlParser=myHtmlParser()
        htmlParser.feed(html)

        # Here we have all of the rows in one long string
        # now we parse through the string and split them up into individual strings
        stripped=htmlParser.tableString.strip('\n')
        stripped = stripped.replace('\n', '')
        splitStrings=stripped.split("tr")

        # Have list of strings split up
        # first two indexes are a blank space and the header, so remove them
        del(splitStrings[0])
        del(splitStrings[0])
        return splitStrings

    def getHtml(self, url):
        html = urllib.request.urlopen(url)
        mybytes = html.read()
        mystr = mybytes.decode("utf8")
        html.close()
        return mystr

    def processTableStrings(self, tableStrings):
        # Go through list and turn them into Result object
        csvStrings=[]
        csvPreviousStrings=[]
        previousSet=set()

        for tableString in tableStrings:
            tableString=self.formatTableString(tableString)
            tableStringValues=tableString.split(",")
            name1=self.getName(tableStringValues[1].strip())
            name2 = self.getName(tableStringValues[4].strip())
            fileName1=tableStringValues[1].strip()
            fileName2=tableStringValues[4].strip()
            previousMatch = self.previousYearMatch(fileName1, fileName2)
            csvString=[name1, fileName1, tableStringValues[2], name2, fileName2, tableStringValues[5],tableStringValues[6], tableStringValues[0]];
            if previousMatch:
                previousSet.add(fileName1)
                csvPreviousStrings.append(csvString)
            else:
                csvStrings.append(csvString)
        if(len(csvStrings)>0):
            return csvStrings
        else:
            return csvPreviousStrings

    def previousYearMatch(self, fileName1, fileName2):
        values1 = fileName2.split("_")
        values2 = fileName1.split("_")

        if values1[0] == values2[0]:
            previousMatch = True  # Assignment are previous years
            return previousMatch
        else:
            previousMatch = False  # Assignments are current years
            return previousMatch


    def formatTableString(self,tableString):
        tableString.lstrip()
        tableString = tableString.replace("td a href", '')
        tableString = tableString.replace("a  td align right", '')
        tableString = tableString.replace("a       ", '')
        tableString=tableString.replace("  http://",'http://')
        tableString=tableString.replace("  ",",")
        tableString=tableString.replace(" ",", ")
        tableString=tableString.replace(" (","(")
        tableString=tableString.replace("(","")
        tableString=tableString.replace(")","")
        tableString=tableString.replace("%","")
        return tableString

#
# Inner class myHtmlParser extends HTMLParser
#
class myHtmlParser (HTMLParser):
    tableString=""
    seenTable=False
    seenEndOfTable=False

    def handle_starttag(self, tag, attrs):
        if(self.seenTable and (not self.seenEndOfTable)):
            self.tableString=self.tableString+tag+" "
            for attr in attrs:
                tupleList=list(attr)
                for item in tupleList:
                    self.tableString=self.tableString+item+" "
        if(tag=="table"):
            self.seenTable=True

    def handle_endtag(self, tag):
        if(self.seenTable and (not self.seenEndOfTable)):
            if(tag=="table"):
                self.seenEndOfTable=True
            else:
               self.tableString=self.tableString+tag+" "

    def handle_data(self, data):
        if(self.seenTable and (not self.seenEndOfTable)):
            self.tableString = self.tableString + data + " "