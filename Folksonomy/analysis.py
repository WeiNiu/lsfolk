from mr_analysis import CountLabel,SP,UserTagDict,TopicRank,TagCooccur,TagCooccur1,SiftTag,SiftTagByTagger,ZJ_inlist,ZJ_list
from library.mrjobwrapper import ModifiedMRJob
from library.twitter import getDateTimeObjectFromTweetTimestamp
from library.mrjobwrapper import runMRJob
from datetime import datetime
from dateutil.relativedelta import relativedelta
hdfs_input_folder = 'hdfs:///user/zcheng/data/expert_detection/mongodb_export/%s/'
#analysis_folder = '/mnt/chevron/wei/hashtags/%s/'
analysis_folder = '/spare/wei/folk/%s'
wei_hdfs_input_folder ='hdfs:///user/wei/folk/%s'
list_creator_user_location=wei_hdfs_input_folder%'list_creator_user_location_all_new'#'hou_tagging_u3_5'#'sf_tagging_u3_5'#'list_creator_user_location_en_lt10_4_12'#'dist_less_than_50_2'#tagger_10'#'list_creator_user_location_nonsingular'#_100'
f_user_tag_dict=analysis_folder%'user_tag_dict_all_new'#ny_u5_10'#'user_tag_dict_en_lt10_for_prob_1_3'#'user_tag_dict_nonsingular_100'
f_topic_rank=analysis_folder%'topic_bg'
user_tag_dict=wei_hdfs_input_folder%'user_tag_dict_new_all'#nonsingular_100'
f_tag_cooccur=analysis_folder%'tag_cooccurence_nonsingular_100'
f_tag_cooccur_1=analysis_folder%'tag_cooccurence_nonsingular1'
f_sifted_tag=analysis_folder%'dallas_tagging_u3_5'#'ny_tagging_u5_10'#'list_creator_user_location_en_lt10_4_12'#100
f_sifted_tag_tagger=analysis_folder%'hou_tagging_u3'#'list_creator_user_location_u30'
f_sp=analysis_folder%'sp_hou_entre'
f_label_cnt=analysis_folder%'cognos_cnt_label_chi'
f_zj_in=analysis_folder%'zj_list'

def getInputFiles(startTime, endTime, folderType='world'):
    current=startTime
    while current<=endTime:
        input_file = hdfs_input_folder%folderType+'%s_%s'%(current.year,
                                                           current.month)
        print input_file
        yield input_file
        current+=relativedelta(months=1)   

class MRAnalysis(object):
    @staticmethod
    def RunJob(mr_class,outputfile,input_file_start_time,input_file_end_time):
        runMRJob(mr_class,
                 outputfile,
                 getInputFiles(input_file_start_time, input_file_end_time),
                 jobconf={'mapred.reduce.tasks':100})
 
    @staticmethod
    def count_freq(input_files_start_time, input_files_end_time):
        mr_class = CountTagTweetFreq
        output_file = f_tagtweetFreq
        MRAnalysis.RunJob(mr_class,
                          output_file,
                          input_files_start_time,
                          input_files_end_time)
    @staticmethod
    def user_tag_dict(inputfile):
        mr_class = UserTagDict
        output_file = f_user_tag_dict
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})
    @staticmethod
    def get_sp(inputfile):
        mr_class = SP
        output_file = f_sp
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 )
    @staticmethod
    def label_cnt(inputfile):
        mr_class = CountLabel
        output_file = f_label_cnt
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 )        
    @staticmethod
    def topic_rank(inputfile):
        mr_class = TopicRank
        output_file = f_topic_rank
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})   
    @staticmethod
    def tag_cooccurence(inputfile):
        mr_class = TagCooccur
        output_file = f_tag_cooccur
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})   
    @staticmethod
    def tag_cooccurence1(inputfile):
        mr_class = TagCooccur1
        output_file = f_tag_cooccur_1
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})   
    @staticmethod
    def sift_tag(inputfile):
        mr_class = SiftTag
        output_file = f_sifted_tag
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})   
    @staticmethod
    def sift_tag_by_tagger(inputfile):
        mr_class = SiftTagByTagger
        output_file = f_sifted_tag_tagger
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})   
     
    @staticmethod
    def zj_inlist(inputfile):
        mr_class = ZJ_inlist
        output_file = f_zj_in
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})   
    @staticmethod
    def zj_list(inputfile):
        mr_class = ZJ_list
        output_file = f_zj_in
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})   
 

    @staticmethod
    def run():
        input_files_start_time, input_files_end_time = \
                                datetime(2011 ,2 ,1), datetime(2013, 3, 31)
        #for mrjob with single or list of input files.
        input1=list_creator_user_location
        input2=user_tag_dict
#        MRAnalysis.user_tag_dict(input1)
#        MRAnalysis.topic_rank(input1)
#        MRAnalysis.tag_cooccurence(input2)
#        MRAnalysis.sift_tag(input1)
#        MRAnalysis.sift_tag_by_tagger(input1)
#        MRAnalysis.get_sp(input1)
#        MRAnalysis.zj_inlist(input1)
        MRAnalysis.zj_list(input1)
#        MRAnalysis.label_cnt(input1)
if __name__=='__main__':
    MRAnalysis.run()   
