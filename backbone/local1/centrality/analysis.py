from mr_analysis import TagCooccur,UserTagDict,TagUserDict,TrueCosine1,TrueCosine2
from library.mrjobwrapper import ModifiedMRJob
from library.twitter import getDateTimeObjectFromTweetTimestamp
from library.mrjobwrapper import runMRJob
from datetime import datetime
from dateutil.relativedelta import relativedelta
hdfs_input_folder = 'hdfs:///user/zcheng/data/expert_detection/mongodb_export/%s/'
#analysis_folder = '/mnt/chevron/wei/hashtags/%s/'
analysis_folder = '/spare/wei/folk/%s'
wei_hdfs_input_folder ='hdfs:///user/wei/folk/%s'
list_creator_user_location=wei_hdfs_input_folder%'hou_tagging_u3_5'#'list_creator_user_location_u30_100'#'ny_tagging_u5_10'#'list_creator_user_location_en_lt10_4_12'#'list_creator_user_location_nonsingular_100'
f_user_tag_dict=analysis_folder%'user_tag_dict_greater_than_3000'#'user_tag_dict_nonsingular_100'
f_topic_rank=analysis_folder%'topic_rank_nonsingular'
user_tag_dict=wei_hdfs_input_folder%'user_tag_dict_less_than_50_en'
tag_user_dict=wei_hdfs_input_folder%'tag_user_dict_hou'
f_tag_cooccur=analysis_folder%'tag_cooccurence_less_than_50_en'
f_tag_cooccur_1=analysis_folder%'tag_cooccurence_nonsingular1'
f_sifted_tag=analysis_folder%'list_creator_user_location_nonsingular_50'#100
f_tag_user_dict=analysis_folder%'tag_user_dict_hou'
f_cosine_tag=analysis_folder%'cosine_hou'#'cosine_en_lt10_12'
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
    def tag_user_dict(inputfile):
        mr_class = TagUserDict
        output_file = f_tag_user_dict
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':10})
   
    @staticmethod
    def true_cosine(inputfile):
        mr_class =  TrueCosine3
        output_file = f_cosine_tag
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':2})
    @staticmethod
    def true_cosine2(inputfile):
        mr_class =  TrueCosine2
        output_file = f_cosine_tag
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':2})
    
    @staticmethod
    def tag_cooccur(inputfile):
        mr_class =  TagCooccur
        output_file = f_tag_cooccur
        inputfilelist = []
        inputfilelist.append(inputfile)
        runMRJob(mr_class,
                 output_file,
                 inputfilelist,
                 jobconf = {'mapred.reduce.tasks':2})
       
    @staticmethod
    def run():
        input_files_start_time, input_files_end_time = \
                                datetime(2011 ,2 ,1), datetime(2013, 3, 31)
        #for mrjob with single or list of input files.
        input1=list_creator_user_location
        input2=user_tag_dict
        input3=tag_user_dict
#        MRAnalysis.tag_user_dict(input1)
        MRAnalysis.true_cosine2(input3)
#        MRAnalysis.true_cosine(input3)
#        MRAnalysis.user_tag_dict(input1)
#        MRAnalysis.topic_rank(input1)
#        MRAnalysis.tag_cooccur(input2)
#        MRAnalysis.sift_tag(input1)
if __name__=='__main__':
    MRAnalysis.run()   
