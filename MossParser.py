#Class MossParser
#This class is designed to take a url as input and creates a csv file of results from MOSS in the same directory
#as this program
import validators

class MossParser:

    def main(self):
        print ("need to work on class")
        #If this is not a valid URL display error and exit

        #get the html text from the URL
        #-> html = getHtml(some_url)

        #Process the html into table strings
        #-> tableStrings = processHtml(html)

        #Process the table strings into csv strings
        #-> csvStrings = processTableStrings(tableStrings)

        #Create, save, and close the csv file
    def testUrl(self,urlArg):
        return validators.url(urlArg)



