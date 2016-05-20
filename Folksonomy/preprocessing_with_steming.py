import cjson
import re
from copy import deepcopy
from nltk import PorterStemmer
from nltk.corpus import stopwords
from library.file_io import FileIO
'''
this function will tokenize, steming, (and remove the common noise).
'''
class ReadFile:
    @staticmethod
    def ReadJson():
        line = cjson.decode(line)
        user_id=line['user_id']
        tags=line['tags']
        for tag in tags:
            yield user_id,tag

class Preprocessing:
    stoplist_=["a", "secondli", "all", "consid", "whoever", "everybodi", "four", "go", "mill", "evermor", "caus", "seem", "whose", "certainli", "to", "doe", "th", "under", "sorri", "sent", "veri", "everi", "yourselv", "did", "forth", "list", "fewer", "tri", "p", "round", "someday", "say", "ten", "till", "d", "past", "like", "notwithstand", "further", "hope", "even", "what", "appear", "brief", "goe", "sup", "new", "mustn", "rd", "ever", "thin", "hasn", "full", "respect", "never", "here", "let", "other", "alon", "along", "fifteen", "ahead", "k", "allow", "amount", "howbeit", "usual", "que", "chang", "that", "hither", "via", "follow", "mere", "put", "nineti", "viz", "yourself", "use", "from", "would", "contain", "two", "next", "few", "call", "therefor", "taken", "themselv", "thru", "until", "more", "know", "becom", "herebi", "herein", "everywher", "particular", "known", "must", "me", "none", "f", "thi", "oh", "anywher", "nine", "can", "mr", "my", "exampl", "indic", "give", "neverf", "near", "someth", "want", "need", "end", "thing", "rather", "six", "how", "low", "instead", "needn", "okay", "haven", "may", "after", "eighti", "differ", "hereupon", "such", "third", "whenev", "amid", "appreci", "q", "one", "so", "specifi", "keep", "thirti", "help", "undo", "inde", "over", "move", "mainli", "soon", "whilst", "through", "look", "fifi", "still", "it", "befor", "thank", "thenc", "somewher", "inward", "ll", "actual", "better", "thanx", "our", "might", "versu", "then", "them", "someon", "somebodi", "therebi", "underneath", "cours", "they", "half", "not", "now", "nor", "get", "name", "alway", "reason", "didn", "whither", "l", "each", "found", "went", "side", "mean", "everyon", "directli", "do", "eg", "weren", "ex", "beyond", "out", "furthermor", "sinc", "forti", "re", "serious", "got", "thereupon", "given", "quit", "whereupon", "besid", "ask", "anyhow", "inasmuch", "backward", "couldn", "g", "could", "caption", "w", "ltd", "henc", "onto", "think", "first", "alreadi", "thereaft", "done", "anoth", "thick", "miss", "aw", "littl", "their", "twenti", "top", "system", "least", "anyon", "too", "hundr", "mostli", "exactli", "took", "immedi", "regard", "somewhat", "kept", "believ", "herself", "than", "daren", "b", "unfortun", "gotten", "zero", "i", "r", "were", "toward", "minu", "anyway", "and", "alongsid", "beforehand", "mine", "unlik", "have", "seen", "saw", "clearli", "rel", "abroad", "thoroughli", "latter", "abl", "asid", "thorough", "also", "take", "which", "begin", "unless", "though", "ani", "who", "most", "eight", "but", "noth", "whi", "sub", "forev", "don", "especi", "nobodi", "noon", "sometim", "m", "amoungst", "definit", "neverless", "normal", "came", "particularli", "show", "find", "fifth", "hadn", "outsid", "should", "onli", "hi", "abov", "de", "overal", "truli", "cannot", "nearli", "despit", "dure", "him", "is", "qv", "h", "cri", "twice", "she", "x", "where", "ignor", "see", "comput", "are", "best", "said", "away", "current", "pleas", "behind", "variou", "between", "probabl", "neither", "across", "avail", "we", "recent", "howev", "nd", "come", "both", "c", "last", "mani", "whereaft", "accord", "against", "selv", "s", "becam", "com", "otherwis", "among", "co", "afterward", "whatev", "her", "non", "moreov", "throughout", "meantim", "describ", "second", "three", "been", "whom", "much", "interest", "likewis", "hardli", "empti", "correspond", "latterli", "concern", "els", "former", "those", "myself", "novel", "these", "bill", "valu", "n", "will", "while", "ain", "shall", "there", "seven", "almost", "wherev", "sincer", "thu", "cant", "vs", "in", "ie", "if", "inc", "etc", "perhap", "insofar", "make", "same", "wherein", "sever", "shan", "fairli", "upon", "lower", "off", "wherebi", "nevertheless", "whole", "nonetheless", "well", "anybodi", "obvious", "without", "y", "the", "con", "your", "lest", "just", "less", "be", "downward", "presum", "front", "greet", "ye", "yet", "unto", "farther", "had", "except", "ha", "adj", "ought", "around", "possibl", "whichev", "five", "part", "dare", "hereaft", "mayb", "necessari", "either", "therein", "twelv", "becaus", "old", "often", "twitter", "some", "back", "self", "sure", "ourselv", "happen", "provid", "for", "bottom", "opposit", "per", "everyth", "tend", "t", "sensibl", "nowher", "although", "sixti", "by", "on", "about", "ok", "anyth", "of", "v", "o", "whenc", "plu", "consequ", "or", "own", "formerli", "into", "within", "due", "down", "appropri", "mightn", "couldnt", "eleven", "aren", "amidst", "accordingli", "inner", "way", "forward", "wa", "himself", "elsewher", "enough", "amongst", "somehow", "with", "he", "made", "whether", "insid", "up", "tell", "place", "below", "un", "z", "gone", "later", "associ", "certain", "am", "doesn", "an", "meanwhil", "as", "right", "at", "et", "fill", "again", "hasnt", "entir", "no", "wherea", "when", "detail", "late", "you", "realli", "regardless", "welcom", "upward", "ago", "e", "togeth", "hello", "itself", "u", "apart", "far", "seriou", "onc"]
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
    def pre_processing_line(self,line):
        line = cjson.decode(line)
        list_name=line['list_name']
        #split TexasAggies ->Texas Aggies
        list_name=list_name.strip()
        name_split=re.split(r'\W+|_|\d+',list_name)
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
                words += cur_letter
                prev_letter = cur_letter
            words = words.split(' ')
            for word in words:
                word=PorterStemmer().stem_word(word)
                new_list.append(word.lower())
        ###################################
        #if no tag exist,neglect this line#
        ###################################
        if new_list==[]:
            return 0
        line['tag']=[word for word in new_list if word not in self.stoplist_]
        #line['tag']=new_list
        #print new_list
        del line['list_name']
        del line['_id']
        #print line
       
        #    del line['list_name']
        #     print line
        return line          
    def processing_file(self,filename,outputfile):
        for line in open(filename):
            try:
                newline=self.pre_processing_line(line)
                #print newline
                if newline==0:
                    continue
                FileIO.writeToFileAsJson(newline, outputfile)
            except Exception as e:
                print e

if __name__=='__main__':
    inputfile='/mnt/chevron/wei/listdata/list_creator_user_location.json'
    outputfile='/spare/wei/folk/list_creator_user_location_withstemming'
    a=Preprocessing()
    a.processing_file(inputfile,outputfile)
    
