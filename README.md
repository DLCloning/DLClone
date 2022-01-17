# To What Extent do Deep Learning-based Code Recommenders Generate Predictions by Cloning Code from the Training Set?

This is the replication package of the paper "To What Extent do Deep Learning-based Code Recommenders Generate Predictions by Cloning Code from the Training Set?".
In this empirical study, we specialized the T5 model of a previous work conducted by [Ciniselli et al.](https://github.com/mciniselli/T5_Replication_Package) to understand the T5 tendency of reusing blocks of code seen during the training phase.

# Pipeline

* #### Pre-training

    We re-used the pre-training of [Ciniselli et al.](https://github.com/mciniselli/T5_Replication_Package); Therefore, the following elements have been used as-is without further changes:
    - the pre-training dataset
    - the pre-trained model
    - the tokenizer that has been used both for pre-training and fine-tuning.

* #### Fine-tuning Dataset

    We created four different datasets for the four different thresholds used in our analysis as reported in our paper in Section 2.2 "Study Context: Datasets Construction".
    The four datasets can be found at the following [link](https://zenodo.org/record/5823006#.YdX9eX3MJb8)
    The original algorithm used for filtering near-duplicates can be found at this [link](https://github.com/github/CodeSearchNet/blob/master/src/dataextraction/dedup_split.py)

* ##### Hyper Parameter Tuning

    We performed the hyper-parameter (HP) tuning to find the best model for the fine-tuning using the `Very_Weak` dataset.
    We tested four configurations and trained the model for 100k steps.
    The configurations are the following:
    - constant learning rate (lr = 0.001)
    - Inverse Square Root (warmup_steps = 10000)
    - slanted (cut_fraction=0.1, ratio=32, max_learning_rate=0.01, start_step=0)
    - polynomial learning rate (starter_learning_rate=0.01, end_learning_rate=1e-6, decay_step=10000, power=0.5)
    
    Specifically:
    - `HP_Tuning/pretraining_script` contains the notebook scripts used in [Colab](https://colab.research.google.com/).
    - `HP_Tuning/configuration_files` contains the configuration file for each HP tuning.
    - `HP_Tuning/evaluation` contains the folder with the scripts used to evaluate the performance.

    First, execute `evaluate.ipynb` to generate the predictions for each configuration.
    Then, the execute the following command:
    ```
    python3 perfect_predictions.py --prediction_file "<prediction_file>" --target_file "<target_file>" --length_file "<length_file>"
    ```
    where:
    - **prediction_file** contains the prediction of each mode;
    - **target_file** contains the target 
    - **length_file** contains the file with the number of masked lines for each prediction

    `HP_Tuning/predictions` folder contains the predictions and targets, while `HP_Tuning/length` folder contains the length.

    The HP tuning models can be found [here](https://zenodo.org/record/5823314#.YdYItH3MJb8)
    The result of the four configuration tested in terms of correct prediction are the following:
    | Configuration | Correct Predictions |
    |---------------|---------------------|
    | Slanted       |         583 (3.69%) |
    | Constant      |         522 (3.31%) |
    | ISR           |         567 (3.59%) |
    | Polynomial    |              0 (0%) |
    
* #### Fine-tuning
    
    From our analysis emerged that **Slanted Triangular** is the best HP configuration.
    Thus, we selected this model and fine-tuned it for around 100 epochs, changing the number of steps based on the dataset size.
    The following table shows the number of steps for each dataset
    | Dataset     | Steps |
    |-------------|-------|
    | Very Strong |  152k |
    | Strong      |  275k |
    | Weak        |  400k |
    | Very Weak   |  470k |
    
    The `Finetuning/configuration_file` folder contains the configuration files for each dataset, while `Finetuning/script` is the script for training each model.
    The `Finetuning/evaluation` folder contains the script for evaluating the model (it works in the same way as the Hyper Parameter Tuning script.
    You can find the fine-tuning models [here](https://zenodo.org/record/5823314#.YdYItH3MJb8)
    The `Finetuning/score` folder contains the script for evaluating the score of T5.
    Finally, the `Finetuning/predictions` folder contains the predictions of each model (that have to be used also for the summary creation presented below)

    Each model achieved the following correct predictions:
    | Configuration | Correct Predictions |
    |---------------|---------------------|
    | Very Strong   |         487 (3.09%) |
    | Constant      |         514 (3.27%) |
    | ISR           |         573 (3.64%) |
    | Polynomial    |         576 (3.66%) |

    We also analyzed 50 random predictions for each model to classify them into **Correct** (if the syntax is correct and the code makes sense), **Meaningful** (if the syntax is correct but the code did not make sense, e.g., assigning the same variable to two different values in the next line) and **Meaningless** (if the code has no sense, e.g., repeating multiple time the same instruction)


* #### Clone Detection
    In this step we looked for **duplicates** between pre-training and fine-tuning method and the prediction generated by T5. We removed all comments from pre-training methods (since T5 was fine-tuned without the code comments).
    To complement our analysis, we also checked if the oracle (i.e., the correct block that T5 should predict) has clone snippets with the training set. The results were not reported in the paper but we leave all the data and results in our replication package.
    Then we applied the **Simian Clone Detector** to look for duplicates.
    Since we noticed that Simian performances decreased a lot when the number of files increased, we wrote pretraining and finetuning methods in bunches of 30k methods, using a customized separator between each method (to avoid Simian to find a clone involving lines of two different methods).
    Simian works at **line-level**; hence we formatted all the methods using **IntelliJ formatter**. 
    Please note that we wrote the entire pretraining and finetuning methods, while we also considered the predicted block/oracle block for the other sets (since we're looking for clones that does not consider the input provided to the T5 model).
    The parsed methods can be found [here](https://zenodo.org/record/5833792#.Ydw2wn3MJb8).
    You can find the Type1 code clones running Simian in this way:
    ```
    java -jar simian-2.5.10.jar -threshold=2 files/*.java
    ```
    where **files** folder contains the parsed java files
    For Type2 clones you can simply add `-ignoreIdentifiers` 
    You can find the output of Simian and the found clones with predictions [here](https://zenodo.org/record/5833796#.Ydw6Gn3MJb8) and with the oracle [here](https://zenodo.org/record/5833798#.Ydw63n3MJb8).
    
    Then we processed the Simian output file to extract the desired information.
    You can find the script with a README in `Cloning/Prediction_Simian_Processing` for the clones with predictions and in `Cloning/Oracle_Simian_Processing` 
    
    From the processed files, we generated **two excel summaries** to generate the graphs present in the paper.
    You can find the files (and a detailed README) in `Cloning/Summary_Generation` folder.
    We represented the summary results using the HeatMap. The script with the README can be found in `Cloning/HeatMap`.
    In the paper we reported only the results when excluding the predictions with the **unknown token** (in the `result_without_unknown` subfolder); the results considering every predictions can be found in `result_with_unknown`.
    
    
* #### Extra Details    
    
    To compute the Cyclomatic Complexity Number (CCN) we used [lizard](https://pypi.org/project/lizard/) 1.17.9 version.
    In particular, we execute the following command:

    ```
    lizard all_methods/ > all_methods.txt
    ```
    where **all_methods** is the folder containing all the test methods (or the test method without the block to predict, depending on the analysis we wanted to do)
    
    The results can be found in the `Cloning/Cyclomatic_Complexity` folder (the three values, splitted by **|||** separator, are the ID of the prediction, the CCN of the entire method and the CCN of the method without the block to predict.
    
    To **count the number of lines**, we ignored all the lines with a number of (non-empty) char <=2. You can find them in `Cloning/Summary_Generation/file_needed` folder.
    
    To compute the correlation we used the **spearmanr** function from **scipy.stats**.
    You can find the script, the results and a detailed README in `Cloning/Correlation` folder.
    
    The list of the prediction with the unknown token can be found in `Cloning/Unknown_Predictions`. It contains a list of integers ranging from 0 to 15741. The element 1 implies that the second prediction contains an unknown token in the prediction of at least one of the four trained models.


# Acknowledgment

    We aim to acknowledge:
    - The authors of the "[An Empirical Study on the Usage of Transformer Models for Code Completion](https://github.com/mciniselli/T5_Replication_Package)" for publicly releasing the replication package of their study on which we built our study;
    - The authors and contributors of the [CodeSearchNet](https://github.com/github/CodeSearchNet) project for providing a lightweight implementation of the algorithm used to detect near-duplicates.


# Contributors
    ANONYMOUS AUTHORS

# License
    This software is licensed under the MIT License.

