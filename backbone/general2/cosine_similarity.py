from __future__ import division
import cjson
import sys
from math import log10
from collections import defaultdict
#args tag_user_dict cosine
#infile='/spare/wei/tag_user_dict_l1'
def raw_term_cosine(infile,outfile):
    #'/spare/wei/local/tag_user_dict_ch3'
    tag_list=[]
    #useless=['and','the','my','of','for']
    for line in open(infile,'r'):
        #line=line.split('\t')[1]
        line=cjson.decode(line)
        tag_list.append(line)
    cosine_dict={}
    centrality={}
    for i in range(len(tag_list)):
        cur=tag_list[i]
        for j in range(i+1,len(tag_list)):
            com=tag_list[j]
            cosine=0
            for key,value in cur[1].iteritems():
                cosine+=value*com[1].get(key,0)
            if cosine>=0.1:
                cosine_dict[cur[0]+'_'+com[0]]=cosine
                centrality[cur[0]]=centrality.get(cur[0],0)+cosine
                centrality[com[0]]=centrality.get(com[0],0)+cosine
    #'/spare/wei/local/cosine_ch3'
    #outfile1='/spare/wei/noise_centrality_0.1_l1'
    outfile=open(outfile,'w')
    outfile.write(cjson.encode(cosine_dict))
    #outfile1=open(outfile1,'w')
    #outfile1.write(cjson.encode(centrality))

def utd_to_tud(user_tag_dict):
    idf={}
    tag_user_dict=defaultdict(dict)
    for line in open(user_tag_dict,'r'):
        line=cjson.decode(line)
        idf[str(line[0])]=len(line[1])
        for key,value in line[1].iteritems():
            tag_user_dict[key][str(line[0])]=value
    N=len(tag_user_dict)
    for key,value in tag_user_dict.iteritems():
        for uid,cnt in value.iteritems():
            tag_user_dict[key][uid]*=log10(N/idf[uid])

    #normalization
    for key,value in tag_user_dict.iteritems():
        sq_sum=0
        for uid,cnt in value.iteritems():
            sq_sum+=cnt*cnt
        sq_sum=sq_sum**0.5
        for uid,cnt in value.iteritems():
            tag_user_dict[key][uid]=cnt/sq_sum
    tag_user_list=[]
    for key,value in tag_user_dict.iteritems():
        tag_user_list.append([key,value])
        #print key,value
    return tag_user_list

#def idf(tag_user_dict):

            
def tfidf_cosine(infile,outfile):
    tag_list=utd_to_tud(infile)
    cosine_dict={}
    centrality={}
    for i in range(len(tag_list)):
        cur=tag_list[i]
        for j in range(i+1,len(tag_list)):
            com=tag_list[j]
            cosine=0
            for key,value in cur[1].iteritems():
                cosine+=value*com[1].get(key,0)
            #print cosine
            if cosine>=0.1:
                cosine_dict[cur[0]+'_'+com[0]]=cosine
                centrality[cur[0]]=centrality.get(cur[0],0)+cosine
                centrality[com[0]]=centrality.get(com[0],0)+cosine
    outfile=open(outfile,'w')
    outfile.write(cjson.encode(cosine_dict))


def main():
    infile=sys.argv[1]
    outfile=sys.argv[2]
    #raw_term_cosine(infile,outfile)
    tfidf_cosine(infile,outfile)

if __name__ == '__main__':
    main()
