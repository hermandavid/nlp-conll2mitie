### ConLL2MITIE

Simple tool to transfer ConLL format to format accepted by NER classifier from [mit-nlp/MITIE](https://github.com/mit-nlp/MITIE).

#### Usage

At first, you can with script with `-h` parameter to show help.
``` bash
$ ./conll2mitie.py -h

usage: conll2mitie.py [-h] -s SOURCE_DATA

optional arguments:
  -h, --help      show this help message and exit
  -s SOURCE_DATA  Input file containing data in ConLL format
```

Example usage
``` bash
$ ./conll2mitie.py -s ./data/conll2003/eng.train
```

#### Notes

* Tool was written using `Python 3.6`
