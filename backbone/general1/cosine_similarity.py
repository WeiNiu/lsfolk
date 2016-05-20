from __future__ import division
import cjson
import sys
from math import log10,exp,log
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

def utd_to_tud1(user_tag_dict):
    idf={}
    tag_user_dict=defaultdict(dict)
    ucnt=0
    for line in open(user_tag_dict,'r'):
        line=cjson.decode(line)
        #print line 
        ucnt+=1
        idf[str(line[0])]=len(line[1])
        #new idf
        #idf=0
        for key,value in line[1].iteritems():
            tag_user_dict[key][str(line[0])]=value
            #if value>0.1:
            #    idf[str(line[0])]=idf.get(str(line[0]),0)+1
    N=len(tag_user_dict)#number of tags
    print N
    for key,value in tag_user_dict.iteritems():
        for uid,cnt in value.iteritems():
            tag_user_dict[key][uid]*=log10(N/idf[uid])
            #print key,uid
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
        #print key,value
        tag_user_list.append([key,value])
        #print key,value
    return tag_user_list,ucnt

            
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

def rbf_kernel(infile,outfile):
    tag_list=utd_to_tud(infile)
    #print tag_list
    print len(tag_list)
    delta=0
    vector_diff_dict={}
    sumdist=0
    cnt=0
    for i in range(len(tag_list)):
        cur=tag_list[i]
        for j in range(i+1,len(tag_list)):
            com=tag_list[j]
            union=set(cur[1].keys()).union(set(com[1].keys()))
            vecdiff2=0
            for key in union:
                vecdiff2+=(cur[1].get(key,0)-com[1].get(key,0))**2
            if vecdiff2<1.2:
                cnt+=1
                sumdist+=vecdiff2**0.5
                vector_diff_dict[cur[0]+'_'+com[0]]=vecdiff2
        #        print vecdiff2,cur[0],com[0]
        #centrality[cur[0]]=centrality.get(cur[0],0)+cosine
        #centrality[com[0]]=centrality.get(com[0],0)+cosine
    delta=sumdist/cnt
    print delta**2
    for key in vector_diff_dict:
        vector_diff_dict[key]=round(exp(-(vector_diff_dict[key]/(2*delta**2))),4)
        #print vector_diff_dict[key]
    outfile=open(outfile,'w')
    outfile.write(cjson.encode(vector_diff_dict))

            
def pmi(infile,outfile):
    tag_list,ucnt=utd_to_tud1(infile)
    delta=0
    pmi_dict={}
    #sumdist=0
    for i in range(len(tag_list)):
        cur=tag_list[i]
        curset=set(cur[1].keys())
        for j in range(i+1,len(tag_list)):
            com=tag_list[j]
            comset=set(com[1].keys())
            jointp=curset.intersection(comset)
            #print jointp

            #print len(jointp),len(cur[1]),len(com[1])
            prob=len(jointp)/(len(cur[1])*len(com[1]))
            #print prob,cur[0],com[0]
            if len(jointp)>=3 and prob>50:
                #print prob,cur[0],com[0]
                pmi_dict[cur[0]+'_'+com[0]]=round(log(prob),4)
        #vecdiff2=0
        #for key,value in cur[1].iteritems():
        #    vecdiff2+=(value-com[1].get(key,0))**2
            
        #vector_diff_dict[cur[0]+'_'+com[0]]=vecdiff2
        #centrality[cur[0]]=centrality.get(cur[0],0)+cosine
        #centrality[com[0]]=centrality.get(com[0],0)+cosine
    
    outfile=open(outfile,'w')
    outfile.write(cjson.encode(pmi_dict))

def main():
    infile=sys.argv[1]
    outfile=sys.argv[2]
    #raw_term_cosine(infile,outfile)
    #tfidf_cosine(infile,outfile)
    #pmi(infile,outfile)
    rbf_kernel(infile,outfile)

if __name__ == '__main__':
    main()
