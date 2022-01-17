
In this step we computed the correlation among some variables.

We used the script in python, but we checked that the same result can be achieved in R.
We decided to evaluate the correlation between:
- CC Test Method: CCN of the entire test method
- CC No Masked: CCN of the entire method without considering the block to predict
- Num Lines: Number of lines of the entire method
- Num Masked Lines: Number of lines of the block to predict
- Confidence: confidence of the T5 model about the prediction
and 
- the presence/non presence of Type1 and Type2 clusters (i.e., if the number of clusters is >0, then we put 1, otherwise 0)

We used Spearman correlation since there are less constraints compared to Pearson (that is generally used for continuous variables)
We reported also the significance of the test (<0.05 => significative)