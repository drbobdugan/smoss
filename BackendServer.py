#!/usr/bin/env python3.6

#
#   FILE:   BackendServer.py
#   AUTHOR: mmiddleton
#   DATE:   19 FEB 2018
#
#   DESCRIPTION:
#   This file comprises the code that runs the Flask server for our MOSS solution.
#

from flask import *
from SortResults import SortResults
from DataAggregator import DataAggregator
from MOSSResultsRetriever import MOSSResultsRetriever
from Graph import Graph
import os


# Global Variables
app = Flask(__name__, template_folder=os.path.dirname('./'))
sorter = SortResults ()
aggregator = DataAggregator()
retriever = MOSSResultsRetriever()
graph = Graph(None)


#
#   _Index ():     Generates the landing page for SMOSS.
#
@app.route ('/', methods = ['GET', 'POST'])
def _Index ():
    print('[BackendServer]\tIndex page displayed!')
    if request.method == "POST":
        inputURLs = request.form['text'] #input from the user
        retriever.urls = inputURLs.split("\n")

        valid, url = getValidorInvalidURL(retriever.urls)
        if not valid:
            template = "templates/errorpage.html"
            error = ("Invalid URL: "+ url)
            return render_template(template, value=error)
        else:
            return redirect('selectionpage')

    template = "templates/index.html"
    return render_template (template)

@app.route('/selectionpage',  methods = ['GET', 'POST'])
def _MOSSselectpage():
    print('[BackendServer]\tMOSS Selection page displayed!')
    template = "templates/SelectionPage.html"

    if request.method == "POST":
        selection = request.form['selection']
        retriever.reInit()

        if (selection == "allURLs"):
            for url in retriever.urls:
                updated_url = url.rstrip()
                retriever.urls.append(updated_url)
        else:
            retriever.urls.append(selection)
            retriever.get_results()
        aggregator.reInit(retriever.results)
        return redirect('moss')
    duplicateValues, urlList = checkForDuplicates(retriever.urls)
    return render_template(template, urlList=urlList, duplicateValues=duplicateValues)

#
#   _MOSSOutput (): Formerly held within SortResults.py
# , this displays the MOSSoutput template at localhost:5000/moss
#
@app.route ('/moss')
def _MOSSOutput ():
    print('[BackendServer]\tMOSS Output page displayed!')
    template, value = getValidorInvalidMossTemplate()
    percentsValues = getValidorInvalidAggregateLinesTemplate()
    linesValues = getValidorInvalidAggregatePercentTemplate()
    results = retriever.results;

    graph = Graph(results)
    graphJson = graph.getJsonObject(results)
    nodes = graphJson["nodes"]
    edges = graphJson["edges"]
    return render_template(template, value=value, percentsValues=percentsValues, linesValues=linesValues, nodes=nodes, edges=edges)


@app.route('/URLvalidation')
def _MOSSurlvalidation():
    print('[BackendServer]\tMOSS URL validation page displayed!')
    template, value = getValidorInvalidURL()
    return render_template(template, value=value)


def checkForDuplicates(urlList):
    nonDuplicates = set()
    duplicates=set()
    for url in urlList:
        if url.rstrip() not in nonDuplicates:
            nonDuplicates.add(url.rstrip())
        else:
            duplicates.add(url.rstrip())

    return duplicates, nonDuplicates


def getValidorInvalidURL(urlList):

    valid, url = retriever.getValidity(urlList)
    if not valid:
        return False, url
    else:
        return True, url


def getValidorInvalidMossTemplate():
    if not(sorter.validateData()):
        template = "templates/errorpage.html"
        value = "Invalid File Data"
    else:
        template = "templates/MOSSoutput.html"
        value = sorter.get_csv()
    return template, value


def getValidorInvalidAggregatePercentTemplate():
    percentsValues = aggregator.top_percents
    return percentsValues


def getValidorInvalidAggregateLinesTemplate():
    linesValues = aggregator.top_lines
    return linesValues

#
#   _ErrorHandler ():   Displays the generic error page with output on the error type
#


@app.errorhandler (403)
@app.errorhandler (404)
def _ErrorHandler (errorCode):
    template = "templates/errorpage.html"
    return render_template (template, value = errorCode)


if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)
