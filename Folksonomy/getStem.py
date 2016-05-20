import nltk
import cjson
infile="./webster"

class Stem(object):
    def get_stem_list(files):
        for filename in files:
            f=open(filename,'r')
            for line in f:

