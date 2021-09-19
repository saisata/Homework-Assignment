from explore_dataset import ExploreDataset
from define_variable import DefineVariables
import argparse
import matplotlib.pyplot as plt
import numpy as np


def plot_duration_statistics(data):
    fig1, ax1 = plt.subplots(figsize=(20,20))
    ax1.boxplot(np.array(data))
    ax1.set_ylabel('duration times')
    ax1.set_title('Duration time statistics')
    plt.show()

def plot_box_plots(data):
    fig1, ax1 = plt.subplots(figsize=(20,20))
    ax1.boxplot(np.array(data))
    ax1.set_ylabel('number of bad annotations')
    ax1.set_title('Bad Annotation Statistics')
    plt.show()

def get_good_annotation_statistics(final_dataset):
    variable=DefineVariables()
    return final_dataset[variable.good_annotations_count].describe()
    

def get_bad_annotation_statistics(bad_annotations_count):
    variable=DefineVariables()
    return final_dataset[variable.bad_annotations_count].describe()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Home Assignment')
    parser.add_argument('--project_file', type=str, help='Input project data json file')
    parser.add_argument('--reference_file', type=str, help='reference data json file')
    args = parser.parse_args()
    evaluator=ExploreDataset(args.project_file, args.reference_file)
    project_data,reference_data=evaluator.read_JSON_data()
    annotators_user_data,annotators_times,work_package_size, \
        highly_disagree_reponses,cannot_solve_responses,\
            corrupt_data_responses=evaluator.evaluate_project_data(project_data)
    number_of_annotators=evaluator.get_annotator_number()
    amount_of_work=evaluator.get_annotator_package()
    cant_solve_responses=evaluator.get_cant_solve_responses()
    currupt_data_responses=evaluator.get_corrupt_data_responses()
    mean_annotation_time,minimum_annotation_time,maximum_annotation_time=evaluator.get_annotation_time_statistics(annotators_times)
    reference_data_count,reference_data_percentage,reference_dataset=evaluator.evaluate_reference_dataset()
    good_annotators_count,bad_annotators_count,good_annotators_data,bad_annotators_data,project_dataset \
        =evaluator.get_good_bad_annotators(project_data,reference_dataset)
    final_dataset=evaluator.get_final_dataset(good_annotators_count, bad_annotators_count,reference_dataset,project_dataset)

    print(f'1a. The total number of annotators are {len(np.unique(np.array(annotators_user_data)))}')
    print(f'1b. The mean, minimum and maximum duration times are {mean_annotation_time}, {minimum_annotation_time} and {maximum_annotation_time}')
    plot_duration_statistics(annotators_times)
    print(f'1c. There are different work packages sizes that are assigned to different annotators \
    The range of various work package sizes ranges from {min(np.unique(np.array(work_package_size)))} to {max(np.unique(np.array(work_package_size)))}')
    print(f'1d. There are in total {highly_disagree_reponses} in the dataset. Highly disagree responses comes when \
    there are equal number of positive and negative responses in each task in the dataset.')

    print(f'2. The number of cannot solve resonse are {len(cant_solve_responses)} and the number of corrupt data responses\
    {len(corrupt_data_responses)} . In each of questions, each annotator has utilized this option and did not provide \
    any answer to the actual question.')
    print(f'3. Yes, the  reference set is well balanced. The distrubution of data is as follows: \
    {reference_data_count} \
    and its corresponding percentage is \
    {reference_data_percentage}')

    print(f'4. Finally with respect to the reference dataset, the number of good and bad annotators are found in the \
    the actual dataset. The overall good annotators statistics are \
    {get_good_annotation_statistics(final_dataset)} \
    and bad annotators statistics are \
    {get_bad_annotation_statistics(final_dataset)}. \
    The final dataset looks as follows : \
    {final_dataset}.')
    # plot_box_plots(good_annotators_count)
    # plot_box_plots(bad_annotators_count)
    # plot_notmal_distribution(good_annotators_count)
    # plot_notmal_distribution(bad_annotators_count)

    
    


