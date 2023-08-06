# pySolr
[Solr](http://lucene.apache.org/solr/) Client for Python3.

## Features
+ Basic operations: eg. selecting, updating & deleting.
+ Index optimization.
+ Timeout support.
+ SolrCloud.

## Support
The author have tested the functions of this tools on these solr version:
+ solr 7.7.1

## Requirements
+ Python 3.3+
+ Requests 2.9.1 +
+ [kazoo](https://github.com/python-zk/kazoo) for SolrCloud(Zookeeper)

## Install
```bash
pip install py3Solr
```
or:
```bash
python setup.py install
```
## Quick Start
[test/test.py](test/test.py)

## TODO
+ global log