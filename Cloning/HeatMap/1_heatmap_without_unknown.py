import codecs
from typing import List

import re

import os
import csv

import sys
import argparse

import math

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

dataset_size=dict()
dataset_size["Pretrain"]=1850361
dataset_size["VeryWeak"]=796974
dataset_size["Weak"]=671033
dataset_size["Strong"]=445796
dataset_size["VeryStrong"]=239760

order_datasets=["VeryStrong", "Strong", "Weak","VeryWeak"]


def create_heatmap(df):
    # standard heatmap with red colors and scale among 0 and 1
    fig, ax = plt.subplots(figsize=(11, 9), dpi=200)
    # plot heatmap
    res=sb.heatmap(df, cmap="Reds", vmin= 0, vmax=1,
               linewidth=0.3, annot=True, fmt=".1%", annot_kws={"fontsize":15})
    

    # change ticks in the colorbar
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, .25, .50, .75, 1])
    cbar.set_ticklabels(['0%', '25%', '50%', '75%', '100%'])

    # increase size of labels
    res.set_xticklabels(res.get_xmajorticklabels(), fontsize = 20)

    return plt

def create_heatmap_labels(df):
    # create a heatmap with labels that are different from the values
    # to be finished
    labels=df.copy()

    labels['Type 1'] = labels['Type 1'].map(str)  
    labels['Type 2'] = labels['Type 2'].map(str)  

    for col_name, data in labels.items():
        # print("col_name:",col_name, "\ndata:",data)
        for i, d in enumerate(data):
            data[i]=d+"aa"

    fig, ax = plt.subplots(figsize=(11, 9), dpi=200)
    # plot heatmap
    res=sb.heatmap(df, cmap="Greys", vmin= 0, vmax=1,
               linewidth=0.3, annot=labels, fmt="", annot_kws={"fontsize":15})
    
    # change ticks in the colorbar
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, .25, .50, .75, 1])
    cbar.set_ticklabels(['0%', '25%', '50%', '75%', '100%'])

    # increase size of labels
    res.set_xticklabels(res.get_xmajorticklabels(), fontsize = 20)

    return plt


def create_heatmap_black_white(df, colors, xticklabels, yticklabels, figsizex=4, figsizey=4):
    # create a heatmap where we can define the colours for each column and also the name
    # we want to use for the xlabels
    labels=df.copy()


    column_names=df.columns

    for column in column_names:

        labels[column] = labels[column].map(str)  

    for col_name, data in labels.items():
        # print("col_name:",col_name, "\ndata:",data)
        for i, d in enumerate(data):
            data[i]=str(round(round(float(d),3)*100,1))+"%"

    if colors is not None:

        for col_n, (col_name, data) in enumerate(df.items()):
            for i, d in enumerate(data):  
                data[i]=colors[col_n]
  

    fig, ax = plt.subplots(figsize=(figsizex, figsizey), dpi=200)
    # plot heatmap


    res=sb.heatmap(df, cmap="Greys", vmin= 0, vmax=1,
               linewidth=0.3, annot=labels, fmt="", annot_kws={"fontsize":9}, 
               cbar=False, xticklabels=xticklabels, yticklabels=yticklabels, square=True)
    
    res.set_yticklabels(res.get_yticklabels(), rotation = 0, fontsize = 9)
    res.set_xticklabels(res.get_xticklabels(), rotation = 0, fontsize = 9)


    # change ticks in the colorbar
    # cbar = ax.collections[0].colorbar
    # cbar.set_ticks([0, .25, .50, .75, 1])
    # cbar.set_ticklabels(['0%', '25%', '50%', '75%', '100%'])

    # Drawing the frame
    # res.axhline(y = 0, color = 'k', 
    #         linewidth = 1)

    # res.axhline(y = len(column_names), color = 'k',
    #         linewidth = 1)

    # res.axvline(x = 0, color = 'k',
    #         linewidth = 1)

    # res.axvline(x = len(column_names), color = 'k',
    #         linewidth = 1)

    return plt



def create_heatmap_black_white_multiple(dfs, colors, xticklabels, yticklabels, titles=None, figsizex=4, figsizey=4, num_rows=1, aspect=0.3):
    # create a heatmap where we can define the colours for each column and also the name
    # we want to use for the xlabels

    num_heatmap=len(dfs)

    num_cols=int(num_heatmap/num_rows)

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols,
                         figsize=(figsizex, figsizey), dpi=1000)

    # width space between subplots
    plt.subplots_adjust(wspace = .1)

    plt.subplots_adjust(hspace = -0.15)

    axes_flatten=axes.flatten()

    # for each dataframe
    for ii, df in enumerate(dfs):

        # create the labels with the value in percentage
        labels=df.copy()

        column_names=df.columns

        for column in column_names:

            labels[column] = labels[column].map(str)  

        for col_name, data in labels.items():
            # print("col_name:",col_name, "\ndata:",data)
            for i, d in enumerate(data):
                data[i]=str(round(round(float(d),3)*100,1))+"%"

        # change the color of the graph (light and dark columns)
        if colors is not None:

            for col_n, (col_name, data) in enumerate(df.items()):
                for i, d in enumerate(data):  
                    data[i]=colors[col_n]
      
        # the ylabels must be shown only for the first graph
        yticklabels_curr=yticklabels
        if ii % num_cols !=0:
            yticklabels_curr=False

        res=sb.heatmap(df, cmap="Greys", vmin= 0, vmax=1,
                   linewidth=0.3, annot=labels, fmt="", annot_kws={"fontsize":6}, 
                   cbar=False, xticklabels=xticklabels, yticklabels=yticklabels_curr, 
                   square=False, ax=axes_flatten[ii])
        
        if ii % num_cols == 0:
            res.set_yticklabels(res.get_yticklabels(), rotation = 0, fontsize = 5)
        res.set_xticklabels(res.get_xticklabels(), rotation = 0, fontsize = 5)

        # set the title for each plot
        axes_flatten[ii].set_title(titles[ii],fontsize=7)

        # reduce the height of the graph
        axes_flatten[ii].set_aspect(aspect=aspect)

    return plt


def create_heatmap_black_white_single(df, colors, xticklabels, yticklabels, figsizex=4, figsizey=4):
    # create a heatmap where we can define the colours for each column and also the name
    # we want to use for the xlabels

    labels=df.copy()

    column_names=df.columns

    for column in column_names:

        labels[column] = labels[column].map(str)  

    for col_name, data in labels.items():
        # print("col_name:",col_name, "\ndata:",data)
        for i, d in enumerate(data):
            data[i]=str(round(round(float(d),3)*100,1))+"%"

    if colors is not None:

        for col_n, (col_name, data) in enumerate(df.items()):
            for i, d in enumerate(data):  
                data[i]=colors[col_n]
  

    fig, ax = plt.subplots(figsize=(figsizex, figsizey), dpi=1000)
    # plot heatmap

    res=sb.heatmap(df, cmap="Greys", vmin= 0, vmax=1,
               linewidth=0.3, annot=labels, fmt="", annot_kws={"fontsize":9}, 
               cbar=False, xticklabels=xticklabels, yticklabels=yticklabels, square=False)
    
    res.set_yticklabels(res.get_yticklabels(), rotation = 0, fontsize = 9)
    res.set_xticklabels(res.get_xticklabels(), rotation = 0, fontsize = 9)

    return plt


def create_heatmap_black_white_multiple_percentage(dfs, colors, xticklabels, yticklabels, titles=None, figsizex=4, figsizey=4, num_rows=1, aspect=0.3):
    # create a heatmap where we can define the colours for each column and also the name
    # we want to use for the xlabels

    num_heatmap=len(dfs)

    num_cols=int(num_heatmap/num_rows)

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols,
                         figsize=(figsizex, figsizey), dpi=1000)

    # width space between subplots
    plt.subplots_adjust(wspace = .1)

    plt.subplots_adjust(hspace = -0.15)

    axes_flatten=axes.flatten()

    # for each dataframe
    for ii, df in enumerate(dfs):

        # create the labels with the value in percentage
        labels=df.copy()

        column_names=df.columns

        for column in column_names:

            labels[column] = labels[column].map(str)  


        for col_name, data in labels.items():
            # print("col_name:",col_name, "\ndata:",data)

            ref_value=0

            for i, d in enumerate(data):
                if i==0:
                    ref_value=round(round(float(d),3)*100,1)

                value=str(round(round(float(d),3)*100,1))+"%"
                if float(ref_value) != 0:
                    increase=(round(round(float(d),3)*100,1)-ref_value)/ref_value
                    if increase<0:
                        value += " ("+ str(round(round(float(increase),3)*100,1))+"%)"
                    else:
                        value += " (+"+ str(round(round(float(increase),3)*100,1))+"%)"


                data[i]=value

        # change the color of the graph (light and dark columns)
        if colors is not None:

            for col_n, (col_name, data) in enumerate(df.items()):
                for i, d in enumerate(data):  
                    data[i]=colors[col_n]
      
        # the ylabels must be shown only for the first graph
        yticklabels_curr=yticklabels
        if ii % num_cols !=0:
            yticklabels_curr=False

        res=sb.heatmap(df, cmap="Greys", vmin= 0, vmax=1,
                   linewidth=0.3, annot=labels, fmt="", annot_kws={"fontsize":6}, 
                   cbar=False, xticklabels=xticklabels, yticklabels=yticklabels_curr, 
                   square=False, ax=axes_flatten[ii])
        
        if ii % num_cols == 0:
            res.set_yticklabels(res.get_yticklabels(), rotation = 0, fontsize = 5)
        res.set_xticklabels(res.get_xticklabels(), rotation = 0, fontsize = 5)

        # set the title for each plot
        axes_flatten[ii].set_title(titles[ii],fontsize=7)

        # reduce the height of the graph
        axes_flatten[ii].set_aspect(aspect=aspect)

    return plt


def create_all_heatmaps(excel_folder):

    # index for the heatmap
    index_name = ["Very Strong", "Strong", "Weak", "Very Weak"]

    '''
    data for the first heatmap (percentage type 1 and type 2 clones)
    '''

    dfs=list()

    for num_lines in range(2,6): # from 2 to 6 lines

        path_excel="{}/{}_True.xlsx".format(excel_folder, num_lines) # we ignore the files where we removed the unknown
        excel_data_df = pd.read_excel(path_excel, sheet_name='Summary')

        type1_clones=excel_data_df["Type 1 Clones"].values
        type2_clones=excel_data_df["Type 2 Clones"].values

        total_predictions=excel_data_df["Total Number of Prediction"].values[0] # total number of predictions


        # percentage of prediction in the dataset
        percentage_clones_T1=list()
        percentage_clones_T2=list()

        for x,y in zip(type1_clones, type2_clones):
            percentage_T1=x/total_predictions
            percentage_T2=y/total_predictions
            percentage_clones_T1.append(percentage_T1)
            percentage_clones_T2.append(percentage_T2)


        df = pd.DataFrame({'Type 1': percentage_clones_T1, 'Type 2': percentage_clones_T2},
                          index=index_name)

        dfs.append(df)

        # # create single black and white heatmap

        # plt=create_heatmap_black_white(df, [0.2,0.8], ["Type 1", "Type 2"], ["Very\nStrong", "Strong", "Weak", "Very\nWeak"], 4,4)
        # # plt.title('Percentage for Type 1 and Type 2 clones \nwith at least {} cloned lines'.format(num_lines))
        # plt.savefig('Cluster_{}_lines.png'.format(num_lines))  
   

    plt=create_heatmap_black_white_multiple(dfs, [0.2,0.8], ["Type 1", "Type 2"], ["Very Strong", "Strong", "Weak", "Very Weak"], 
        [">=2 Lines Clones", ">=3 Lines Clones", ">=4 Lines Clones", ">=5 Lines Clones"],
        6,2)
    # plt.title('Percentage for Type 1 and Type 2 clones \nwith at least {} cloned lines'.format(num_lines))
    plt.savefig('Clusters.pdf', bbox_inches='tight',pad_inches = 0.1)   

    '''
    data for the second heatmap (percentage type 1 and type 2 clones for the oracle)
    '''

    dfs=list()

    for num_lines in range(2,6): # from 2 to 6 lines

        path_excel="{}/{}_True.xlsx".format(excel_folder, num_lines) # we ignore the files where we removed the unknown
        excel_data_df = pd.read_excel(path_excel, sheet_name='Summary')


        total_predictions=excel_data_df["Total Number of Prediction"].values[0] # total number of predictions

        type1_clones_in_oracle=excel_data_df["Type 1 Clones In Oracle"].values
        type2_clones_in_oracle=excel_data_df["Type 2 Clones In Oracle"].values

        # percentage of prediction in the dataset after the removal of the once that 
        # already have a clone in the oracle
        percentage_clones_T1_no_oracle=list() 
        percentage_clones_T2_no_oracle=list()

        for x,y in zip(type1_clones_in_oracle, type2_clones_in_oracle):
            percentage_T1=(x)/total_predictions
            percentage_T2=(y)/total_predictions
            percentage_clones_T1_no_oracle.append(percentage_T1)
            percentage_clones_T2_no_oracle.append(percentage_T2)

        df2 = pd.DataFrame({'Type 1': percentage_clones_T1_no_oracle, 'Type 2': percentage_clones_T2_no_oracle},
                          index=index_name)

        dfs.append(df2)  
        
        # # create black and white single heatmap

        # plt=create_heatmap_black_white(df2, [0.2,0.8], ["Type 1", "Type 2"], ["Very\nStrong", "Strong", "Weak", "Very\nWeak"],3,4)
        # # plt.title('Percentage for Type 1 and Type 2 clones\n with at least {} cloned lines excluding oracles'.format(num_lines))
        # plt.savefig('Cluster_{}_lines_no_oracle.png'.format(num_lines)) 


    plt=create_heatmap_black_white_multiple(dfs, [0.2,0.8], ["Type 1", "Type 2"], ["Very Strong", "Strong", "Weak", "Very Weak"], 
        [">=2 Lines Clones", ">=3 Lines Clones", ">=4 Lines Clones", ">=5 Lines Clones"],
        6,2)
    # plt.title('Percentage for Type 1 and Type 2 clones \nwith at least {} cloned lines'.format(num_lines))
    plt.savefig('Clusters_Oracle.pdf', bbox_inches='tight',pad_inches = 0.1) 

    '''
    data for the third heatmap
    '''

    dfs=list()

    for num_lines in range(2,6): # from 2 to 6 lines

        path_excel="{}/{}_True.xlsx".format(excel_folder, num_lines) # we ignore the files where we removed the unknown
        excel_data_df = pd.read_excel(path_excel, sheet_name='Summary')

        columns=["Type 1 Clones PP", 
        "Type 1 Clones PP Only Pretrain", 
        "Type 1 Clones PP Only Finetuning",
        "Type 1 Clones PP Pretrain And Finetuning", 
        "Type 1 Clones WP", 
        "Type 1 Clones WP Only Pretrain", 
        "Type 1 Clones WP Only Finetuning",
        "Type 1 Clones WP Pretrain And Finetuning", 
        "Type 2 Clones PP", 
        "Type 2 Clones PP Only Pretrain", 
        "Type 2 Clones PP Only Finetuning",
        "Type 2 Clones PP Pretrain And Finetuning", 
        "Type 2 Clones WP", 
        "Type 2 Clones WP Only Pretrain", 
        "Type 2 Clones WP Only Finetuning",
        "Type 2 Clones WP Pretrain And Finetuning"]

        dict_result=dict()
        dict_result["T1PT"]=list()
        dict_result["T1FT"]=list()
        dict_result["T1BOTH"]=list()
        dict_result["T2PT"]=list()
        dict_result["T2FT"]=list()
        dict_result["T2BOTH"]=list()

        for i in range(4): # 4 rows
            total_clones_t1=sum_values(excel_data_df, columns, [0,4], i)
            total_clones_t2=sum_values(excel_data_df, columns, [8,12], i)
            total_clones_pretrain_t1=sum_values(excel_data_df, columns, [1,5], i) # perfect+wrong
            total_clones_finetuning_t1=sum_values(excel_data_df, columns, [2,6], i)
            total_clones_both_t1=sum_values(excel_data_df, columns, [3,7], i)
            total_clones_pretrain_t2=sum_values(excel_data_df, columns, [9,13], i)
            total_clones_finetuning_t2=sum_values(excel_data_df, columns, [10,14], i)
            total_clones_both_t2=sum_values(excel_data_df, columns, [11,15], i)


            dict_result["T1PT"].append(total_clones_pretrain_t1/total_clones_t1)
            dict_result["T2PT"].append(total_clones_pretrain_t2/total_clones_t2)
            dict_result["T1FT"].append(total_clones_finetuning_t1/total_clones_t1)
            dict_result["T2FT"].append(total_clones_finetuning_t2/total_clones_t2)
            dict_result["T1BOTH"].append(total_clones_both_t1/total_clones_t1)
            dict_result["T2BOTH"].append(total_clones_both_t2/total_clones_t2)

        # need to change this if the rounding in create_heatmap is changed
        # we want to be sure that the sum is 1 (can be 0.99 for rounding problems)
        for i, (x,y,z) in enumerate(zip(dict_result["T1PT"],dict_result["T1FT"],dict_result["T1BOTH"])):
            v1=round(x,3)
            v2=round(y,3)
            dict_result["T1BOTH"][i]=1-v1-v2

        for i, (x,y,z) in enumerate(zip(dict_result["T2PT"],dict_result["T2FT"],dict_result["T2BOTH"])):
            v1=round(x,3)
            v2=round(y,3)
            dict_result["T2BOTH"][i]=1-v1-v2

        df3 = pd.DataFrame({'T1PT': dict_result["T1PT"], 
                            'T2PT': dict_result["T2PT"],
                            'T1FT': dict_result["T1FT"],
                            'T2FT': dict_result["T2FT"],
                            'T1BOTH': dict_result["T1BOTH"],
                            'T2BOTH': dict_result["T2BOTH"],
                            },
                          index=index_name)        


        dfs.append(df3.copy())

        plt=create_heatmap_black_white_single(df3, [0.2,0.8, 0.2, 0.8, 0.2, 0.8], 
            ["Type 1\nPretrain", "Type 2\nPretrain", "Type 1\nFinetuning", "Type 2\nFinetuning"
            , "Type 1\nBoth", "Type 2\nBoth"]
            , ["Very\nStrong", "Strong", "Weak", "Very\nWeak"], 5.5,1.5)
        # plt.title('Percentage for Type 1 and Type 2 with pretraining and finetuning dataset\n with at least {} cloned lines'.format(num_lines))
        plt.savefig('Cluster_Pretrain_Finetuning{}_lines.pdf'.format(num_lines), bbox_inches='tight',pad_inches = 0.1) 

        # # Black and white scale
        # plt=create_heatmap_black_white(df3, None, ["Type 1\nPretrain", "Type 1\nFinetuning", "Type 2\nPretrain", "Type 2\nFinetuning"])
        # plt.title('Percentage for Type 1 and Type 2 with pretrainig and finetuning dataset with at least {} cloned lines'.format(num_lines))
        # plt.savefig('Cluster_Pretrain_Finetuning{}_lines.png'.format(num_lines)) 


    plt=create_heatmap_black_white_multiple(dfs, [0.2,0.8, 0.2, 0.8, 0.2, 0.8],
     ["Type 1\nPretrain", "Type 2\nPretrain", "Type 1\nFinetuning", "Type 2\nFinetuning"
        , "Type 1\nBoth", "Type 2\nBoth"]
    , ["Very Strong", "Strong", "Weak", "Very Weak"], 
        [">=2 Lines Clones", ">=3 Lines Clones", ">=4 Lines Clones", ">=5 Lines Clones"],
        7,3.5, num_rows=2, aspect=0.4)
    plt.savefig('Clusters_Pt_Ft.pdf', bbox_inches='tight',pad_inches = 0.1) 

    '''
    data for the fourth heatmap
    '''

    dfs=list()

    for num_lines in range(2,6): # from 2 to 6 lines

        path_excel="{}/{}_True.xlsx".format(excel_folder, num_lines) # we ignore the files where we removed the unknown
        excel_data_df = pd.read_excel(path_excel, sheet_name='Summary')

        dict_ppwp=dict()
        dict_ppwp["T1PP"]=list()
        dict_ppwp["T1WP"]=list()
        dict_ppwp["T2PP"]=list()
        dict_ppwp["T2WP"]=list()

        for i in range(4): # 4 rows
            tot_pp=excel_data_df["Perfect Predictions"].values[i]
            tot_type1_clones=excel_data_df["Type 1 Clones"].values[i]
            tot_type2_clones=excel_data_df["Type 2 Clones"].values[i]
            type1_pp=excel_data_df["Type 1 Clones PP"].values[i]
            type1_wp=excel_data_df["Type 1 Clones WP"].values[i]
            type2_pp=excel_data_df["Type 2 Clones PP"].values[i]
            type2_wp=excel_data_df["Type 2 Clones WP"].values[i]

            dict_ppwp["T1PP"].append(type1_pp/tot_type1_clones)
            dict_ppwp["T1WP"].append(type1_wp/tot_type1_clones)
            dict_ppwp["T2PP"].append(type2_pp/tot_type2_clones)
            dict_ppwp["T2WP"].append(type2_wp/tot_type2_clones)

        # need to change this if the rounding in create_heatmap is changed
        # we want to be sure that the sum is 1 (can be 0.99 for rounding problems)
        for i, (x,y) in enumerate(zip(dict_ppwp["T1PP"],dict_ppwp["T1WP"])):
            v1=round(x,3)
            dict_ppwp["T1WP"][i]=1-v1

        for i, (x,y) in enumerate(zip(dict_ppwp["T2PP"],dict_ppwp["T2WP"])):
            v1=round(x,3)
            dict_ppwp["T2WP"][i]=1-v1

        df4 = pd.DataFrame({'T1PP': dict_ppwp["T1PP"], 
                            'T2PP': dict_ppwp["T2PP"],
                            'T1WP': dict_ppwp["T1WP"],                            
                            'T2WP': dict_ppwp["T2WP"],
                            },
                          index=index_name)        

        dfs.append(df4.copy())

        # plt=create_heatmap_black_white(df4, [0.2, 0.8, 0.2, 0.8], 
        #     ["Type 1\nPerfect Pred", "Type 1\nWrong Pred", "Type 2\nPerfect Pred", "Type 2\nWrong Pred"]
        #     , ["Very\nStrong", "Strong", "Weak", "Very\nWeak"],4,4)


        plt=create_heatmap_black_white_single(df4, [0.2, 0.8, 0.2, 0.8], 
            ["Type 1\nCP", "Type 2\nCP", "Type 1\nWP", "Type 2\nWP"]
            , ["Very\nStrong", "Strong", "Weak", "Very\nWeak"],4,1.5)

        # plt.title('heatmap')
        plt.savefig('result_pp_wp_{}lines.pdf'.format(num_lines), bbox_inches='tight',pad_inches = 0.1)  


    plt=create_heatmap_black_white_multiple(dfs, [0.2,0.8, 0.2, 0.8],
     ["Type 1\nCP", "Type 2\nCP","Type 1\nWP",  "Type 2\nWP"]
            , ["Very Strong", "Strong", "Weak", "Very Weak"], 
        [">=2 Lines Clones", ">=3 Lines Clones", ">=4 Lines Clones", ">=5 Lines Clones"],
        5,3, num_rows=2, aspect=0.3)
    plt.savefig('Clusters_CP_WP.pdf', bbox_inches='tight',pad_inches = 0.1) 


    '''
    data for the fifth heatmap (the same as the 1st but with the percentage)
    '''

    dfs=list()

    for num_lines in range(2,6): # from 2 to 6 lines

        path_excel="{}/{}_True.xlsx".format(excel_folder, num_lines) # we ignore the files where we removed the unknown
        excel_data_df = pd.read_excel(path_excel, sheet_name='Summary')

        type1_clones=excel_data_df["Type 1 Clones"].values
        type2_clones=excel_data_df["Type 2 Clones"].values

        total_predictions=excel_data_df["Total Number of Prediction"].values[0] # total number of predictions


        # percentage of prediction in the dataset
        percentage_clones_T1=list()
        percentage_clones_T2=list()

        for x,y in zip(type1_clones, type2_clones):
            percentage_T1=x/total_predictions
            percentage_T2=y/total_predictions
            percentage_clones_T1.append(percentage_T1)
            percentage_clones_T2.append(percentage_T2)


        df = pd.DataFrame({'Type 1': percentage_clones_T1, 'Type 2': percentage_clones_T2},
                          index=index_name)

        dfs.append(df)

        # # create single black and white heatmap

        # plt=create_heatmap_black_white(df, [0.2,0.8], ["Type 1", "Type 2"], ["Very\nStrong", "Strong", "Weak", "Very\nWeak"], 4,4)
        # # plt.title('Percentage for Type 1 and Type 2 clones \nwith at least {} cloned lines'.format(num_lines))
        # plt.savefig('Cluster_{}_lines.png'.format(num_lines))  
   

    plt=create_heatmap_black_white_multiple_percentage(dfs, [0.2,0.8], ["Type 1", "Type 2"], ["Very Strong", "Strong", "Weak", "Very Weak"], 
        [">=2 Lines Clones", ">=3 Lines Clones", ">=4 Lines Clones", ">=5 Lines Clones"],
        12,5)
    # plt.title('Percentage for Type 1 and Type 2 clones \nwith at least {} cloned lines'.format(num_lines))
    plt.savefig('Clusters_percentage.pdf', bbox_inches='tight',pad_inches = 0.1)   

    '''
    data for the sixth heatmap (same as 2nd but with percentages)
    '''

    dfs=list()

    for num_lines in range(2,6): # from 2 to 6 lines

        path_excel="{}/{}_True.xlsx".format(excel_folder, num_lines) # we ignore the files where we removed the unknown
        excel_data_df = pd.read_excel(path_excel, sheet_name='Summary')


        total_predictions=excel_data_df["Total Number of Prediction"].values[0] # total number of predictions

        type1_clones_in_oracle=excel_data_df["Type 1 Clones In Oracle"].values
        type2_clones_in_oracle=excel_data_df["Type 2 Clones In Oracle"].values

        # percentage of prediction in the dataset after the removal of the once that 
        # already have a clone in the oracle
        percentage_clones_T1_no_oracle=list() 
        percentage_clones_T2_no_oracle=list()

        for x,y in zip(type1_clones_in_oracle, type2_clones_in_oracle):
            percentage_T1=(x)/total_predictions
            percentage_T2=(y)/total_predictions
            percentage_clones_T1_no_oracle.append(percentage_T1)
            percentage_clones_T2_no_oracle.append(percentage_T2)

        df2 = pd.DataFrame({'Type 1': percentage_clones_T1_no_oracle, 'Type 2': percentage_clones_T2_no_oracle},
                          index=index_name)

        dfs.append(df2)  
        
        # # create black and white single heatmap

        # plt=create_heatmap_black_white(df2, [0.2,0.8], ["Type 1", "Type 2"], ["Very\nStrong", "Strong", "Weak", "Very\nWeak"],3,4)
        # # plt.title('Percentage for Type 1 and Type 2 clones\n with at least {} cloned lines excluding oracles'.format(num_lines))
        # plt.savefig('Cluster_{}_lines_no_oracle.png'.format(num_lines)) 


    plt=create_heatmap_black_white_multiple_percentage(dfs, [0.2,0.8], ["Type 1", "Type 2"], ["Very Strong", "Strong", "Weak", "Very Weak"], 
        [">=2 Lines Clones", ">=3 Lines Clones", ">=4 Lines Clones", ">=5 Lines Clones"],
        12,5)
    # plt.title('Percentage for Type 1 and Type 2 clones \nwith at least {} cloned lines'.format(num_lines))
    plt.savefig('Clusters_Oracle_Percentage.pdf', bbox_inches='tight',pad_inches = 0.1) 




def sum_values(excel_file, columns, positions, row):
    # print(columns)
    # print(positions)
    # print(row)
    # print(excel_file.info())
    # print(excel_file)
    # sys.exit(0)
    tot=0
    for index in positions:
        column=columns[index]
        tot+=excel_file[column].values[row]

    return tot

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--excel_folder",
        type=str,
        help="folder containing the summary 2 of previous step"
    )

    args = parser.parse_args()

    create_all_heatmaps(args.excel_folder)


