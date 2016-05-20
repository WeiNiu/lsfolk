#!/usr/bin/python
# -*- coding: utf-8 -*-
import cjson
import re
from copy import deepcopy
from nltk import PorterStemmer
from nltk.corpus import stopwords
from library.file_io import FileIO
from pattern.en import singularize,parse
import langid
'''
this function will tokenize, steming, (and remove the common noise).
'''
class ReadFile:
    @staticmethod
    def ReadJson():
        line = cjson.decode(line)
        user_id=line['user_id']
        tags=line['tags']
        tag_non_repeat=[]
        for tag in tags:
            if tag not in tag_non_repeat:
                tag_non_repeat.append(tag)
                yield user_id,tag
            else:pass

class Preprocessing:
    
    stoplist_=['ifollow','follow','tweeter','person','people','friend','tweet','aaa','',"a","b","c","d","e","f","g","h","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","favorite", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "computer", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "its", "itself", "keep", "ll", "last", "latter", "latterly", "least", "less", "list", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "twitter", "two", "un", "under", "until", "up", "upon", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "able", "abroad", "according", "accordingly", "actually", "adj", "ago", "ahead", "ain", "allow", "allows", "alongside", "amid", "amidst", "anybody", "anyways", "apart", "appear", "appreciate", "appropriate", "aren", "aside", "ask", "asking", "associated", "available", "away", "awfully", "backward", "backwards", "begin", "believe", "best", "better", "brief", "came", "caption", "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "couldn", "course", "currently", "dare", "daren", "definitely", "described", "despite", "did", "didn", "different", "directly", "does", "doesn", "doing", "don", "downwards", "eighty", "end", "ending", "entirely", "especially", "et", "evermore", "everybody", "ex", "exactly", "example", "fairly", "far", "farther", "fewer", "fifth", "followed", "following", "follows", "forever", "forth", "forward", "furthermore", "gets", "getting", "given", "gives", "goes", "going", "gone", "got", "gotten", "greetings", "hadn", "half", "happens", "hardly", "hasn", "haven", "having", "hello", "help", "hi", "hither", "hopefully", "howbeit", "ignored", "immediate", "inasmuch", "inc", "indicate", "indicated", "indicates", "inner", "inside", "insofar", "instead", "inward", "just", "k", "keeps", "kept", "know", "known", "knows", "lately", "later", "lest", "let", "like", "liked", "likely", "likewise", "little", "look", "looking", "looks", "low", "lower", "mainly", "make", "makes", "maybe", "mean", "meantime", "merely", "mightn", "minus", "miss", "mr", "mrs", "mustn", "nd", "near", "nearly", "necessary", "need", "needn", "needs", "neverf", "neverless", "new", "ninety", "non", "nonetheless", "normally", "notwithstanding", "novel", "obviously", "oh", "ok", "okay", "old", "ones", "opposite", "ought", "outside", "overall", "particular", "particularly", "past", "placed", "plus", "possible", "presumably", "probably", "provided", "provides", "que", "quite", "qv", "rd", "really", "reasonably", "recent", "recently", "regarding", "regardless", "regards", "relatively", "respectively", "right", "round", "said", "saw", "say", "saying", "says", "second", "secondly", "seeing", "seen", "self", "selves", "sensible", "sent", "seriously", "seven", "shall", "shan", "somebody", "someday", "somewhat", "soon", "sorry", "specified", "specify", "specifying", "sub", "sup", "sure", "taken", "taking", "tell", "tends", "th", "thank", "thanks", "thanx", "thats","theirs", "theres",  "thing", "things", "think", "thirty", "thorough", "thoroughly", "till", "took", "tried", "tries", "truly", "try", "trying", "twice", "underneath", "undoing", "unfortunately", "unless", "unlike", "unlikely", "unto", "upwards", "use", "used", "useful", "uses'", "a", "using", "usually", "v", "value", "various", "versus", "viz", "vs", "want", "wants", "way", "welcome", "went", "weren", "whichever", "whilst", "yes", "zero"]
    '''
    wiki_stop_words_ = [u'wiki', u'http', u'org', u'svg', u'www', u'wikipedia',
        u'edit', u'com', u'wikimedia', u'common', u'index', u'png', u'php',
        u'w', u'upload', u'titl', u'thumb', u'action', u'go', u'file', u'jpg',
        u'html', u'section', u'en', u'retriev', u'wa', 'articl', u'histori',
        u'list', u'unit', u'templat', u'flag', u'intern']
    '''
    def __init__(self,
                *args,
                **kwargs):
        #super(GetWordFreq, self).__init__(*args, **kwargs)
        self.steming=False
        #self.stoplist_=stoplist_
     #   for word in self.wiki_stop_words_:
     #       self.stopset_.add(word)
     #       pass
    def pre_processing_line(self,line,out1):
        line = cjson.decode(line)
        list_name=line['list_name']
        #split TexasAggies ->Texas Aggies
        list_name=list_name.strip()
        name_split=re.split(r'\W+|_|0|1|2|3|4|5|6|7|8|9',list_name)
        #out1=open('non_en','w')
        #try:
        #    prev_letter = text[0]
        #except:
        #    print text
        new_list=[]
        for text in name_split:
            if text=='':
                continue
            words=''
            try:
                prev_letter = text[0]
            except:
                print text
            word_length = len(text)
            words += prev_letter
            for i in range(1, len(text)):
                cur_letter = text[i]
                if cur_letter.isupper() and prev_letter.islower():
                    words += ' '
                if len(words)<3:
                    words+= cur_letter
                #
                else:
                    if cur_letter==words[-1] and cur_letter==words[-2]:
                        pass
                    else:
                        words += cur_letter
                #
                prev_letter = cur_letter
           # print words
           #new part, only english tag and sigular nouns.
           
            #language=langid.classify(words)[0]
            #print language
            #if language!='en' :#and language!='fr':
            #    print language
            #    print>>out1, [words,language]
            #    return 0
            
            words = words.split(' ')
            #print words
            for word in words:
                word1=deepcopy(word)
                word1=word1.lower()
                word_info=parse(word1).split()[0][0][1]
                #if word_info=='VBZ':
                #    print word1.lower()
                #    print singularize(word1.lower())
                #word2=word1
                #if word1=='famou':
                #    print word, word_info
                if word_info=='NNS'  or word_info=='RB' or word_info=='VBZ':
                    #if word1=='famous' or word1=='business':
                    #    print word1, word_info,1
                    word1=singularize(word1)
                    #if word1=='famou':
                    #    print "singular",word2
                #if word1=='star':
                #    print wo
                word1=word1.lower()
                if word1=='stars':
                    print 'wrong',word,word_info
                #if word1=='busine':
                #    print word2,word_info
                new_list.append(word1)
        ###################################
        #if no tag exist,neglect this line#
        ###################################
        #if new_list==[]:
        #    return 0
        if 'stars' in new_list:
            print 'sssss',new_list
             
        line['tag']=[word for word in new_list if word not in self.stoplist_]
        if line['tag']==[]:
            return 0
        #print line
        #print line['tag']
        del line['list_name']
        del line['_id']
        #print line
        #new_list_name=newlist.lower()
        if self.steming==True:
            stems=[]
            for word in new_list:
                stem=PorterStemmer().stem_word(word)
                stems.append(stem)
            line['tag']=stems
        #    del line['list_name']
        #     print line
        return line          
    def processing_file(self,filename,outputfile):
        out1=open('non_en1','w')
        for line in open(filename):
            try:
                newline=self.pre_processing_line(line,out1)
                #print newline
                if newline==0:
                    continue
                FileIO.writeToFileAsJson(newline, outputfile)
            except Exception as e:
                print e

if __name__=='__main__':
    inputfile='/spare/wei/folk/data/list_creator_user_location.json'#'/mnt/chevron/wei/listdata/list_creator_user_location.json'
    outputfile='/spare/wei/folk/list_creator_user_location_all_new'
    a=Preprocessing()
    a.processing_file(inputfile,outputfile)
    
