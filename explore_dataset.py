import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time 
import json
from define_variable import DefineVariables


#This class contains the functions which helps the user to evaluate the bicycle data



class ExploreDataset():
    def __init__(self,project_json_file,reference_json_file):
        self.project_file=project_json_file
        self.reference_file=reference_json_file
        self.variable=DefineVariables()


# This function is used to load the JSON file.
    
    def read_JSON_data(self):
        self.project_file=open(self.project_file)
        self.reference_file=open(self.reference_file)
        self.project_data=json.load(self.project_file)
        self.reference_data=json.load(self.reference_file)
        self.project_file.close()
        self.reference_file.close()
        return self.project_data,self.reference_data

# In order to extract the relavent information from the dataset
# such as the annotator user id, annotation times, work package sizes,
# number of highly disagree responses, and so on, the below function iterates over the dataset
# and extracts the corresponsing information

    def evaluate_project_data(self,project_data):
        start_time = time.time()
        self.annotators_user_data=[]
        self.annotation_times=[]
        self.work_package_size=[]
        self.highly_disagree_responses=0
        self.cannot_solve_responses=[]
        self.corrupt_data_responses=[]
        for project_id,value in project_data[self.variable.results][self.variable.root_node][self.variable.results].items():
            positive_responses=[]
            negative_responses=[]
            for annotation_result in value[self.variable.results]:
                self.work_package_size.append(annotation_result[self.variable.work_package_size])
                self.annotators_user_data.append(annotation_result[self.variable.user][self.variable.vendor_user_id])
                self.annotation_times.append(annotation_result[self.variable.task_output][self.variable.duration_ms])
                if annotation_result[self.variable.task_output][self.variable.answer]==self.variable.yes:
                    positive_responses.append(annotation_result[self.variable.task_output][self.variable.answer])
                elif annotation_result[self.variable.task_output][self.variable.answer]==self.variable.no:
                    negative_responses.append(annotation_result[self.variable.task_output][self.variable.answer])
                elif annotation_result[self.variable.task_output][self.variable.cant_solve]==True:
                    self.cannot_solve_responses.append(annotation_result[self.variable.task_output])
                elif annotation_result[self.variable.task_output][self.variable.corrupt_data]==True:
                    self.corrupt_data_responses.append(annotation_result[self.variable.task_output])
            if len(positive_responses)==len(negative_responses):
                self.highly_disagree_responses+=1
        return self.annotators_user_data,self.annotation_times,self.work_package_size,self.highly_disagree_responses, self.cannot_solve_responses,self.corrupt_data_responses
                
# Below function is used to extract annotation number, annotator worksize package, number of can't solve and corrupt responses
    def get_annotator_number(self):
        annotator_numbers=np.unique(np.array(self.annotators_user_data))
        return annotator_numbers
    
    def get_annotator_package(self):
        work_package_size=np.unique(np.array(self.work_package_size))
        return work_package_size
    
    def get_cant_solve_responses(self):
        return self.cannot_solve_responses

    def get_corrupt_data_responses(self):
        return self.corrupt_data_responses

# This function gets the estimated the evaluated estimated time statistics

    def get_annotation_time_statistics(self,annotation_times):
        mean_annotation_time=sum(annotation_times)/len(annotation_times)
        minimum_annotation_time=min(annotation_times)
        maximum_annotation_time=max(annotation_times)
        return mean_annotation_time,minimum_annotation_time,maximum_annotation_time

# This function is used to evaluate the reference dataset. This in turn gives the total number of 
# true and false responses.
    
    def evaluate_reference_dataset(self):
        reference_dataset=pd.DataFrame.from_dict(self.reference_data,orient=self.variable.index_orient).reset_index()
        reference_dataset=reference_dataset.rename(columns={self.variable.index_column:self.variable.image_id})
        counts=reference_dataset[self.variable.is_bicycle].value_counts()
        count_percentage=reference_dataset[self.variable.is_bicycle].value_counts(normalize=True).mul(100)
        return counts,count_percentage,reference_dataset

# This function evaluates the number of good and bad annotators for each image by comparing with the reference dataset.
    
    def get_good_bad_annotators(self,project_data,reference_data):
        project_dataset=pd.DataFrame.from_dict(project_data[self.variable.results][self.variable.root_node][self.variable.results],orient=self.variable.index_orient).reset_index()
        project_dataset=project_dataset.rename(columns={self.variable.index_column:self.variable.project_root_node_input_id})
        combined_dataset=pd.concat([project_dataset,reference_data],axis=1)
        good_annotators_data=[]
        bad_annotators_data=[]
        bad_annotators_count=[]
        good_annotators_count=[]
        for row in combined_dataset.iterrows():
            reference_response=row[1][self.variable.is_bicycle]
            bad_annotations=[]
            good_annotations=[]
            for response in row[1][self.variable.results]:
                annotators_response_data=response[self.variable.task_output][self.variable.answer]
                annotators_user_data=response[self.variable.user][self.variable.vendor_user_id]
                if (annotators_response_data==self.variable.yes and reference_response==True) or (annotators_response_data==self.variable.no and reference_response==False):
                    good_annotations.append(annotators_user_data)
                else:
                    bad_annotations.append(annotators_user_data)
            good_annotators_count.append(len(np.unique(np.array(good_annotations))))
            bad_annotators_count.append(len(np.unique(np.array(bad_annotations))))
            good_annotators_data.append(np.unique(np.array(good_annotations)))
            bad_annotators_data.append(np.unique(np.array(bad_annotations)))
        return good_annotators_count,bad_annotators_count,good_annotators_data,bad_annotators_data,project_dataset

# This function finally appends the project dataset, reference dataset, good and bad annotation count.

    def get_final_dataset(self,good_annotators_count,bad_annotators_count,reference_dataset,project_dataset):
        good_annotators_data=pd.DataFrame(good_annotators_count,columns={self.variable.good_annotations_count})
        bad_annotators_data=pd.DataFrame(bad_annotators_count,columns={self.variable.bad_annotations_count})
        final_dataset=pd.concat([project_dataset,reference_dataset,good_annotators_data,bad_annotators_data],axis=1)
        return final_dataset

    


    

    





