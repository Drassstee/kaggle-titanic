import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
import warnings
import os

def run_pipeline():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '../data')
    train_df = pd.read_csv(os.path.join(data_dir, 'train.csv'))
    test_df = pd.read_csv(os.path.join(data_dir, 'test.csv'))
    data = [train_df, test_df]

    for d in data:
        d['Title'] = d.Name.str.extract(r' ([A-Za-z]+)\.', expand=False)
        d['Title'] = d['Title'].replace(['Lady', 'Countess','Capt', 'Col',\
        'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
        d['Title'] = d['Title'].replace('Mlle', 'Miss')
        d['Title'] = d['Title'].replace('Ms', 'Miss')
        d['Title'] = d['Title'].replace('Mme', 'Mrs')
    
    mapping = {"Mr": 1, "Mrs": 2, "Master": 3, "Rare": 4, "Miss": 5}
    for d in data:
        d['Title'] = d['Title'].map(mapping)
        d['Title'] = d['Title'].fillna(0)

    for d in data:
        d['Sex'] = d['Sex'].map( {'female': 1, 'male': 0} ).fillna(0).astype(int)

    test_df['Fare'].fillna(test_df['Fare'].dropna().median(), inplace=True)
    
    for d in data:
        d.loc[d['Fare'] <= 7.0, 'Fare_New'] = 1
        d.loc[(d['Fare'] > 7.0) & (d['Fare'] <= 39.0), 'Fare_New'] = 2
        d.loc[d['Fare'] > 39.0, 'Fare_New'] = 3
        d['Fare_New'] = d['Fare_New'].astype(int)

    freq = train_df.Embarked.dropna().mode()[0]
    for d in data:
        d['Embarked'] = d['Embarked'].fillna(freq)
        d['Embarked'] = d['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)

    for d in data:
        d['Deck'] = d['Cabin'].str[0]
        d['Deck'] = d['Deck'].fillna('U')
        d['Deck'] = d['Deck'].map({'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'T':8, 'U':0})

    for d in data:
        d['Surname'] = d.Name.str.extract('([A-Za-z]+),', expand=False)
        
    le = LabelEncoder()
    le.fit(pd.concat([train_df['Surname'], test_df['Surname']]).astype(str))
    for d in data:
        d['Surname'] = le.transform(d['Surname'].astype(str))

    for d in data:
        d['Family_Group'] = d['Surname'].astype(str) + '_' + d['Fare_New'].astype(str)
        
    train_df['Family_Survival'] = 0.5
    for idx, row in train_df.iterrows():
        family_mask = (train_df['Surname'] == row['Surname']) & (train_df.index != idx)
        if family_mask.sum() > 0:
            train_df.loc[idx, 'Family_Survival'] = train_df.loc[family_mask, 'Survived'].mean()
            
    family_survival_dict = train_df.groupby('Surname')['Survived'].mean().to_dict()
    test_df['Family_Survival'] = test_df['Surname'].map(family_survival_dict).fillna(0.5)

    surname_counts = pd.concat([train_df['Surname'], test_df['Surname']]).value_counts()
    for d in data:
        d['Surname_Count'] = d['Surname'].map(surname_counts)
        d['Surname_Count'] = d['Surname_Count'].fillna(1)

    train_df = train_df.drop(['Name', 'PassengerId', 'Ticket', 'Cabin', 'Fare', 'SibSp', 'Parch','Family_Group', 'Age', 'Surname'], axis=1)
    test_df = test_df.drop(['Name', 'Ticket', 'Cabin', 'SibSp', 'Parch', 'Fare','Family_Group', 'Age', 'Surname'], axis=1)

    X_train = train_df.drop('Survived', axis=1)
    Y_train = train_df['Survived']
    X_test = test_df.drop('PassengerId', axis=1).copy()

    m = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    m.fit(X_train, Y_train)
    
    acc = m.score(X_train, Y_train) * 100
    cv_score = cross_val_score(m, X_train, Y_train, cv=10, scoring='accuracy').mean() * 100
    
    print(f'Training Accuracy: {acc}')
    print(f'Cross validation average score: {cv_score}')

    y_pred = m.predict(X_test)
    
    sub = pd.DataFrame({
        "PassengerId": pd.read_csv(os.path.join(data_dir, 'test.csv'))["PassengerId"],
        "Survived": y_pred
    })
    sub.to_csv(os.path.join(data_dir, 'gender_submission.csv'), index=False)

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    run_pipeline()