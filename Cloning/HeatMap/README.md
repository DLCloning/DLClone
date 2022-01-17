
For creating the heatmap, you can run the following command:
```
python3 1_heatmap_without_unknown.py --excel_folder "/Users/USER/OneDrive - USI/code/005_Copy_vs_Generation/out/24_clone_detection/10_create_summary/summary2"
```
This command excludes all the cases where there is the occurrence of an unknown token in a prediction.
If you want to consider all of them (for the replication package), you can run:

```
python3 1_heatmap_with_unknown.py --excel_folder "/Users/USER/OneDrive - USI/code/005_Copy_vs_Generation/out/24_clone_detection/10_create_summary/summary2"
```

The first graph contains the percentage of type1 and type2 clones between the training datasets and the `predictions` for each filtering, considering clone when at least x lines are copied

The second graph contains the percentage of type1 and type2 clones between the training datasets and the `targets` for each filtering, considering clone when at least x lines are copied

In the third graph we reported the percentage of clones that involve only methods from pretraining, only from finetuning and from both of them.

In the fourth graph we reported the percentage of clones analyzing perfect predictions and wrong predictions.

The fifth and sixth graph are the same as first and second, but we also reported the percentage of increasing (using the strong as base case)


# PACKAGES
pandas
matplotlib
seaborn
numpy
