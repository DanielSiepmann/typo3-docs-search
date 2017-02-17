#!/usr/bin/env python

from datetime import datetime
from elasticsearch import Elasticsearch
import argparse
import hashlib
import json
import sys


def initArguments():
    parser = argparse.ArgumentParser(
        description='Import scraped information to Elasticsearch'
    )
    parser.add_argument(
        '-i --inputFile',
        type=file,
        required=True,
        help='The file to import',
        dest='inputfile'
    )
    return parser.parse_args()


def get_document_id(doc):
    h = hashlib.new('sha1')
    h.update(doc['url'] + doc['url'] + doc['version'])
    id = h.hexdigest()


def importFile(data_file, es):
    for doc in json.load(data_file):
        # Provide further information to document.
        doc.update({
            'timestamp': datetime.now(),
        })

        es.index(
            index='en',
            doc_type='doc',
            id=get_document_id(doc),
            body=doc
        )

args = initArguments()
es = Elasticsearch()
importFile(args.inputfile, es)
es.indices.refresh(index='en')
