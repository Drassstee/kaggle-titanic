# Kaggle-titanic-ai
Score in kaggle: 0.81818
nickname: drassstee
The aim of the project is simple. You just need to predict who would die(well, died...) when titanic crashed.  
You must implement features which can help with the prediction. Then train the model with these features and predict the outcome.
Send the predictions(csv file) to a kaggle competition platform and get the score.
## Setup
Python version 3.8 or higher  
requirements.txt does not contain versions for dependencies because different Python versions require different versions of dependencies.  
The problem could be solved with conda and its .yml file, but you would need to install it beforehand.  
Thus, i use simple virtual environment which does not need external installing.  
The virtual environment was not included in repository because its size is too large (it is a bad practice to include it).
## How to run
Both commands below create the virtual environment, install needed dependencies, etc.  
So you do not need to do anything (i am making your life easier).
### notebook
```bash
make analysis
```
Open notebook/main.ipynb on port :8891  
then run the cells in notebook one after another
### script python
FOR REFERENCE, THE CONTENT IS THE SAME AS IN THE NOTEBOOK. AUDIT JUST ASKS FOR THE SCRIPT I DO NOT KNOW WHY
```bash
make pipeline
```
In both cases, gender_submissions.csv in "data" folder is created. This csv file is submitted for verification on kaggle-titanic competition platform.
### Results:
Training Accuracy: 85.18518518518519  
Cross validation average score: 83.61173533083645  
They are not needed for the audit. The only score which is needed is kaggle score. Check drassstee's score(mine)  
Here's the link: https://www.kaggle.com/competitions/titanic/leaderboard?search=drassstee  
Min. score required to pass the audit: 78.9  
My score: 0.81818
### Feature Engineering
This is just a copy of explanation in my notebook:  
The features that contributed the most:  
Family_Survival and Surname_Count  
Families generally had a higher chance of survival(because of children, etc).  
The chance was even higher for those who had a better PClass.  
Overall, the feature was created with the assumption that people with  
similar surnames and/or fares_range would be a family, thus, they would have a better  
chance of survival. It worked perfectly. Before this feature, i had features  
Alone/Family_size which helped me to increase my score to 77-78.7, but it was not enough.  
By combining these features with newly created surnames and fares_new(it is just mapping based on range),  
the new feature, Family_Survival was created and raised my score to 80+.  
Surname_Count is a similar feature. It just counts the same surnames with mapping(the assumption was families would have a higher chance of survival  
and rich families generally had higher chances). It raised my score to 0.81818.  

By the way, i did not come up with this myself. I read one comment in Kaggle with the content:   
"The guy raised his score to 83+ just by extracting the surnames". So it helped me.  