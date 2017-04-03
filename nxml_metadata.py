#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  NXML biblographic data extractor
#  
#  David Cirella, decirella@gmail.com
#  2016-11-16
#  Last updated: 2017-01-21
#
#  Usage: 
#   $ python nxml_metdata.py doc_collection_path_name
# 
  
import os
import json
import sys
from datetime import date
from sys import argv
from xml.dom.minidom import parse

# take input of dir path of nxml docs
script, targ_dir = argv

# output to json for solr indexing
coll_bib = []


def xml_parse(raw_file):
    # open xml file and parse file
    doc_bib = dict()
    dom = parse(raw_file)
    node = dom.documentElement
    journal_title = node.getElementsByTagName('journal-title')[0]\
                    .firstChild.nodeValue
    article_title = node.getElementsByTagName('article-title')[0]\
                    .firstChild.nodeValue
    author_group = node.getElementsByTagName('contrib')
    pub_date = node.getElementsByTagName('pub-date')
    pub_info = node.getElementsByTagName('article-meta')
    abstract = node.getElementsByTagName('abstract')
    author_group = node.getElementsByTagName('contrib')
    # get all authors/co-authors
    authors = []
    for auth in author_group:
        surname = auth.getElementsByTagName('surname')[0].firstChild\
                    .nodeValue
        given_name = auth.getElementsByTagName('given-names')[0]\
                    .firstChild.nodeValue
        authors.append((surname + ", " + given_name))
    for num in pub_date:
        year = num.getElementsByTagName('year')[0].firstChild.nodeValue
    for metadat in pub_info:
        vol = metadat.getElementsByTagName('volume')[0].firstChild\
            .nodeValue
        pmid = metadat.getElementsByTagName('article-id')[0].firstChild\
            .nodeValue
        try:
            issue = metadat.getElementsByTagName('issue')[0].firstChild\
                .nodeValue
            doc_bib.update({'issue': issue})
        except:
            e = sys.exc_info()[0]
        pgf = metadat.getElementsByTagName('fpage')[0].firstChild\
            .nodeValue
        pgl = metadat.getElementsByTagName('lpage')[0].firstChild\
            .nodeValue
        pages = pgf + "-" + pgl
        
    for p in abstract:
        ab_text = p.getElementsByTagName('p')[0].firstChild.nodeValue
        
    doc_bib = {'publication' : journal_title, 'year' : year, 
                'title' : article_title, 'authors': authors, 
                'abstract' : ab_text, 'pages': pages, 'vol': vol, 
                'pmid': pmid}
    
    coll_bib.append(doc_bib)
    return 0

def get_docs(targ_dir):
    for file in os.listdir(targ_dir):
        if file.endswith(".nxml"):
            file_path = os.path.join(targ_dir, file)
            # list processed files to terminal
            print file_path
            xml_parse(file_path)
            
def json_out(collection_parsed):
    filename = '%s/%s' % ('output', str(date.today())+'_'+\
            'parsed_bib.json')
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename , 'w') as f: 
        json.dump(collection_parsed, f)

def main():
    get_docs(targ_dir)
    json_out(coll_bib)
    return 0

if __name__ == '__main__':
    main()

