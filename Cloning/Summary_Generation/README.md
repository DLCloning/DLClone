
# SUMMARY 1

## FIELDS

This summary contains the following information about the predictions:
Prediction ID	# ID of the prediction (from 0 to 15742). We have one row for each prediction in the test set
Is Perfect Prediction	# if the model correctly predicted the current prediction
CC Test Method	# cyclomatic complexity of the test method that contain the current block we masked
CC No Masked		# cyclomatic complexity of the test method (without the masked block) that contain the current block we masked
Num Lines # number of lines of the test method
Num Masked Lines	# number of line we masked (from 2 to 6)
Has Unknown Token	 # True if predicting this specific instance has generated an unknown token for at least one of the models (0807, 0605, 0403, 0302)
Confidence	 the confidence of the model for this prediction
Prediction	 # generated prediction
Target	# oracle
Num Clusters Type 1	 # number of clusters of type 1 that contain that prediction. 2 means that this prediction is present in 2 different clusters
Tot Cluster Type 1	# total number of clusters of type 1 found by Simian
Average Size Clusters Type 1	# average number of pretraining, training method or prediction blocks present in the clusters
Tot Elements Pretraining Type 1 # sum of number of elements of pretraining each cluster of type 1
Tot Elements Finetuning Type 1 # sum of number of elements of finetuning each cluster of type 1
Num Clusters Type 2	 # number of clusters of type 2 that contain that prediction. 2 means that this prediction is present in 2 different clusters
Tot Cluster Type 2	# total number of clusters of type 2 found by Simian
Average Size Clusters Type 2 # average number of pretraining, training method or prediction blocks present in the clusters
Tot Elements Pretraining Type 2 # sum of number of elements of pretraining each cluster of type 2
Tot Elements Finetuning Type 2 # sum of number of elements of finetuning each cluster of type 2

## COMMANDS

```
nohup python3 2_create_summary1.py --input "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/predictions" --CC "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/CC.txt" --length "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/num_lines.txt" --masked_and_method "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/test_masked_and_method.txt" --mask_length "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/test_length.txt" --perfect_predictions "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/perfect_predictions" --prediction_and_target "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/prediction_and_target" --output_folder "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/summary1" --unknown_token "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/unknown_predictions.txt"  --confidence "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/confidence" &
```

# SUMMARY 2

This summary contains the following information:
Filter Level: the filter level applied (0302, ..)	
Perfect Predictions: the total number of perfect predictions
Total Number of Prediction: the total number of blocks we want to predict (15742)
Type 1 Clones: the number of predictions (up to 15742) that appear in at least one clone (if 500 it means that among the 15742 predictions, 500 are cloned)
Type 1 Clones In Oracle: the number of oracles (up to 15742) that appear in at least one clone (if 500 it means that among the 15742 oracles, 500 are cloned)	
Type 1 Clones PP: number of PERFECT prediction that appear in at least one clone
Type 1 Clones PP Only Pretrain: number of PERFECT prediction that appear in at least one clone involving only methods from pretrain	
Type 1 Clones PP Only Finetuning: number of PERFECT prediction that appear in at least one clone involving only methods  methods from finetuning	
Type 1 Clones PP Pretrain and Finetuning: number of PERFECT prediction that appear in at least one clone involving methods from finetuning	 and pretrain
Type 1 Clones WP: number of WRONG prediction that appear in at least one clone
Type 1 Clones WP OnlyPretrain: number of WRONG prediction that appear in at least one clone involving only methods from pretrain
Type 1 Clones WP OnlyFinetuning: number of WRONG prediction that appear in at least one clone involving only methods from finetuning
Type 1 Clones WP Pretrain and Finetuning: number of WRONG prediction that appear in at least one clone involving methods from finetuning	 and pretrain

There are the same fields involving Type 2 rather than Type 1 clones.

We have two different versions of summary 2: _False and _True
_False consider all the cases, while _True consider only the case without the unknown token.

```
nohup python3 -u 3_create_summary2.py --input "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/predictions" --oracle "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/oracle" --CC "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/CC.txt" --length "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/num_lines.txt" --masked_and_method "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/test_masked_and_method.txt" --mask_length "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/test_length.txt" --perfect_predictions "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/perfect_predictions" --prediction_and_target "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/prediction_and_target" --output_folder "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/summary2" --unknown_token "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/unknown_predictions.txt"  --confidence "/home/USER/005_Copy_vs_Generation/24_clone_detection/10_create_summary/files/confidence" &
```

# PACKAGES
openpyxl
lxml