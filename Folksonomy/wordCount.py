#!/usr/bin/env python
from mrjob.job import MRJob
import re
import simplejson as json
#import cjson
from local import textP
class CountWords(MRJob):
    def mapper(self,key,line):
        #text=json.loads(line)
        text= textP.pre_processing_line(line)
        for word in text:
            yield word, 1
    def reducer(self, word, counts):
        yield word, sum(counts)
    def steps(self):
        return [self.mr(mapper = self.mapper, reducer = self.reducer)]
if __name__ == '__main__':
    CountWords.run()
