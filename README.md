# Kaggle-titanic-ai
Score in kaggle: 0.81818
nickname: drassstee
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