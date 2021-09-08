<<<<<<< HEAD
# LE
# Task description

In the preliminary round of ASC20-21, a cloze style dataset is provided. The dataset is collected from internet and contains multi-level English language exams used in China for high school, and college entrance exams: CET4 (College English Test 4), CET6 (College English Test 6), and NETEM (National Entrance Test of English for MA/MS Candidates). Part of the data comes from public CLOTH dataset [9]. There are 4603 passages and 83395 questions in the training set, 400 passages and 7798 questions in the developer set, and 400 passages and 7829 questions in the test set. The participants should design and train their neural network to achieve the best performance on the test set.



Complete the “Complete Fill-in-the-blank” task using the Bert model
1. introduce the "wordnet" knowledge base as a secondary weight in prediction
2. Use model integration, including Bert, Albert, T-5



In final we reached 92.53% accuracy on dev dataset.

Here is the directory structure :

- LE：Root directory
    - test：A single json file contains answers for test set.
    - script：PyTorch source code here
    - model：PyTorch model here


Because we have used Ensemble Learning strategy,there are many generated files in the ./LE/model and ./LE/script directories.

## model directory
in this directory,there saved all PyTorch model we have trained.

### 	Model integration

​	model_name-all：representing for model trained with full train dataset

​	model_name-n：representing for the no.n base learner model trained with re-sampling dataset. 

### 	Introduction WordNet

​	bert-base-uncased-none：representing for model trained without WordNet

​	bert-base-uncased-wn：representing for model trained with WordNet

## script directory：

we have submitted scripts of three different models.

### 	Model-albert：

​	codes about Albert model

### 	Model-bert：

​	codes about Bert model

### 	Model-t5：

​	codes about T5 model

### 	Result：

​	here are files record scores of base learner for each option.

### 	combination :

​	here are files record results after ranking and combining flies in ./model/result directories

### 	model_ensembles :

​	here are files record options scores after normalization

## test directory：

the result json file on test dataset

## How to reproduct the result：

### dev dataset：

1.  run ./final_dev.sh in ./LE/script/Model-n respectively ,where you can get options scores files after normalization
2.  run ./ensemble_dev.sh in ./LE/script directory,where you can get accuracy about ensembled model on dev dataset.


### test dataset：

1. run ./final_test.sh in ./LE/script/Model-n directory respectively ,where you can get options scores files after normalization.
2. run ./ensemble_test.sh in ./LE/script directory ,where you can get the result json file saved ./LE/test.

### If you want to retrain model 

1. run makeSubData.py in ./LE/script/Model-albert directory make to get resampling subdataset. 
2. run data_utils.py in ./LE/script/Model-n directory to package dataset to .pt file.
3. run ./run.sh in ./LE/script/Model-n directory.
4. cancel the annotation of first line in ./final_dev.sh,run it and you can get the score file from new model.
5. run the steps mentioned above.
=======
# LE
Complete the “Complete Fill-in-the-blank” task using the Bert model
>>>>>>> 59a99b477ec458b74525805da0d6b369041a8afa
