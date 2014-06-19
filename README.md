Constructing Master List of Colleges & Data
=========================================

### Getting Started
######Install dependencies:  
`pip install -r requirements.txt`

####Additional output:

output-debug.tsv provides all colleges in this output format:

`upstart_id freebase_id  search_score actual name result name`

reconcile.tsv provides all colleges (in input format) that were not found in Freebase during the initial Search.

####Notes:
* ".encode('utf-8')" necessary for strings with non-English characters.
* Input file contains "--" when appending city or campus name to university name ("University of State--Campus"). The college name in the Freebase result usually appears as "University of State Campus", "University of State, Campus" or "University of State at Campus".
* Changed state abbreviations to full names. 
http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/

###Procedure:
* The Search API was used to find Freebase IDs by provided college names. Checking manually for results, this produced most of the data. The 'score' is provided by Freebase Search and 
* The difference in strings (difflib) determines whether or not to further reconcile
* Initially the Reconciliation endpoint of the Freebase API was used to target those that could not be found via Search. However, results were not produced for all colleges provided.
* Instead, variations of the college name are needed for Freebase to find the correct Freebase ID.
* Confidence percentages were based off of the Freebase scores in a logarithmic scale. Only scores less than 100 were considerable during testing. 
