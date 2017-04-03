# NXML Metadata Pasing tool
The script takes input of a directory of NXML files and returns a JSON file of bibliographic information for each file that is ingestible by Solr indexing.  The script provides a quick way to index the metadata and abstracts for a directory of .nxml files.  The output has the following information for each file:

* Title
* Author(s)
* Year
* Abstract
* Publication title
* Volume
* Issue
* Pages
* PMID

### NXML Format
NXML format is used by the National Library of Medicine for storing articles.  Specifically, the full-text and bibliographic information for all articles in the Pub Med Open Access subset are available in this format.  The tool was developed to aid in the indexing of NXML files made available as a part of the [TREC data set](http://www.trec-cds.org/).

## Index in Solr
The resulting JSON file can be used to create indexes in Apache Solr with the following command:
```
curl 'http://localhost:8983/solr/gettingstarted/update?commit=true' --data-binary @/path/to/output/2017-03-05_parsed_bib.json -H 'Content-type:application/json'
```


### Usage
This was developed and used for working with the NLM Pubmed open access collections.
```
$ python nxml_metadata.py path/to/dir/of/test_docs/
```
Output directory is created, json output file is named with current date_parsed_bib.json
