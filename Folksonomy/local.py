import cjson
import re

class textP(object):
    @staticmethod
    def pre_processing_line(line):
        line = cjson.decode(line)
        list_name=line#['list_name']
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
        return words  
