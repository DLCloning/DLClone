import pandas as pd
import sys

from scipy.stats import spearmanr

folders=["0302", "0403", "0605", "0807"]

unknown_file="/Users/USER/OneDrive - USI/code/005_Copy_vs_Generation/out/24_clone_detection/5_find_unknown_predictions/unknown_predictions.txt"

f = open(unknown_file, "r")
unknown=f.readlines()
f.close()

unknown=[int(k.strip()) for k in unknown]

print(len(unknown))

def format_pvalue(pvalue):
    if "e" not in str(pvalue):
        pv=round(pvalue,3)
        if str(pv) in ["-0.0", "0.0"]:
            pvalue_str=str(pvalue)
            res=""
            for p in pvalue_str:
                if p not in ["-", ".", "0"]:
                    res+=p
                    break
                res+=p
            return res

        return round(pvalue,3)

    parts=str(pvalue).split("e")

    return str(round(float(parts[0]),3))+"e{}".format(parts[1])

def format_value(value):
    v=round(value,3)
    if str(v) in ["-0.0", "0.0"]:
        value_str=str(value)
        res=""
        for p in value_str:
            if p not in ["-", ".", "0"]:
                res+=p
                break
            res+=p
        return res

    return round(value,3)



for f in folders:
    print("processing {}".format(f))
    path_excel="/Users/matteo.ciniselli/OneDrive - USI/code/005_Copy_vs_Generation/out/24_clone_detection/10_create_summary/summary1/{}/{}.xlsx".format(f,f)
    excel_data_df = pd.read_excel(path_excel, sheet_name='Summary')

    # removing the rows corresponding to the unknown token
    excel_data_df = excel_data_df.drop(labels=unknown, axis=0)

    # print(excel_data_df.info())

    # for col in excel_data_df.columns:
    #     print(col)

    cols_to_keep=["CC Test Method", "CC No Masked", "Num Lines", "Num Masked Lines", "Confidence", "Num Clusters Type 1", "Num Clusters Type 2"]

    for c in excel_data_df.columns:
        if c not in cols_to_keep:
            excel_data_df.drop(c, axis=1, inplace=True)

    temp=list()

    for k in excel_data_df["Num Clusters Type 1"]:
        if k > 0:
            temp.append(1)
        else:
            temp.append(0)

    excel_data_df["Num Clusters Type 1"]=temp    

    temp=list()

    for k in excel_data_df["Num Clusters Type 2"]:
        if k > 0:
            temp.append(1)
        else:
            temp.append(0)

    excel_data_df["Num Clusters Type 2"]=temp 

    a=excel_data_df.corr(method='spearman', min_periods=1)

    # print(a)

    for k in cols_to_keep[:-2]:
        curr1=spearmanr(excel_data_df[k], excel_data_df['Num Clusters Type 1'])
        curr2=spearmanr(excel_data_df[k], excel_data_df['Num Clusters Type 2'])
        
        print("{} - {}: {} (pvalue={})".format(k, "Type1", format_value(curr1.correlation), format_pvalue(curr1.pvalue)))
        print("{} - {}: {} (pvalue={})".format(k, "Type2", format_value(curr2.correlation), format_pvalue(curr2.pvalue)))
