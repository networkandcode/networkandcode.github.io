---
canonical_url: "https://dev.to/aws-builders/ml-learning-byte-load-split-and-scale-data-1n31"
date: "2023-10-16"
title: "M/L Learning Byte: Load, Split and Scale Data"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fsource.unsplash.com%2Ffeatured%2F%3Fdatascience"
tags: "machinelearning, datascience, python, aws"
categories: "machinelearning, datascience, python, aws"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/ml-learning-byte-load-split-and-scale-data-1n31)**

Let's play with some data in Pandas. I am using a notebook for this purpose that's created inside a Notebook instance in Amazon SageMaker. This post contains some of the preliminary steps we would do before creating or training a model.

![Amazon SageMaker Icon](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k4yci3ph4xlqehmvljs0.png)

In my case the notebook instance was created with just the default settings.
![Create notebook instance button](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f89how5e05vs216eob16.png)

Note that the notebook name should not be in snakecase(for ex. note_book is invalid), just saying as it's common to name variables or files in snakecase format in python.

Click on JupyterLab once the notebook instance is created.
![Open JupyterLab link](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g0idy8qkn9din9o3u4i1.png)

Inside jupyter lab, create a new notebook, I have clicked on the tensorflow conda environment in the launcher.![TensorFlow Conda environment](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/z4x5ca2y2ha8x3tcdwzk.png)



Let's get started...

We are going to create a dataframe in Pandas that should hold the following data:

| Age (years) | Income (thousands) | Hours_Worked | Salary (thousands) |
|-------------|--------------------|--------------|---------------------|
| 32          | 45                 | 50           | 70                |
| 41          | 50                 | 45           | 80                |
| 28          | 30                 | 60           | 60                |
| 35          | 38                 | 55           | 75                |
| 45          | 60                 | 42           | 90                |
| 29          | 32                 | 48           | 65                |
| 37          | 40                 | 35           | 75                |
| 42          | 55                 | 47           | 85                |
| 36          | 48                 | 38           | 80                |
| 31          | 35                 | 52           | 70                |

## Dictionary
For this, we would create a dictionary in Python with keys as the column names and wrap that [dictionary](https://www.youtube.com/watch?v=7Rrt7-rnyxM&t=3595s) in the Pandas DataFrame object.


```python
import pandas as pd

salary_dict = {
    'Age (years)': [32, 41, 28, 35, 45, 29, 37, 42, 36, 31],
    'Income (thousands)': [45, 50, 30, 38, 60, 32, 40, 55, 48, 35],
    'Hours_Worked': [50, 45, 60, 55, 42, 48, 35, 47, 38, 52],
    'Salary (thousands)': [70, 80, 60, 75, 90, 65, 75, 85, 80, 70]
}

salary_df = pd.DataFrame(salary_dict)
```

Let's print this dataframe


```python
print(salary_df)
```

       Age (years)  Income (thousands)  Hours_Worked  Salary (thousands)
    0           32                  45            50                  70
    1           41                  50            45                  80
    2           28                  30            60                  60
    3           35                  38            55                  75
    4           45                  60            42                  90
    5           29                  32            48                  65
    6           37                  40            35                  75
    7           42                  55            47                  85
    8           36                  48            38                  80
    9           31                  35            52                  70


Awesome, so it resembles our table, however it also has extra information on the left, which are the indices starting from 0. The last index is 9 which means there are 9+1 = 10 rows. By looking at the data we can say there are 10 rows and 4 columns, we can also get this with the shape attribute, which is useful with big datasets.


```python
print(salary_df.shape)
```

    (10, 4)


## Index
Instead of the default integer indices, we can also set something meaningful if we would like to, for ex. in this case we could set some random person names as indices. And this time let's print the top5 and last5 rows with head and tail respectively.


```python
person_names = ['Ali', 'Sara', 'Ahmed', 'Emily', 'David', 'Olivia', 'Michael', 'Sophia', 'Aryan', 'Neha']

salary_df_with_custom_indices = pd.DataFrame(
    salary_dict,
    index=person_names
)

print(salary_df_with_custom_indices.head())
print(salary_df_with_custom_indices.tail())
```

           Age (years)  Income (thousands)  Hours_Worked  Salary (thousands)
    Ali             32                  45            50                  70
    Sara            41                  50            45                  80
    Ahmed           28                  30            60                  60
    Emily           35                  38            55                  75
    David           45                  60            42                  90
             Age (years)  Income (thousands)  Hours_Worked  Salary (thousands)
    Olivia            29                  32            48                  65
    Michael           37                  40            35                  75
    Sophia            42                  55            47                  85
    Aryan             36                  48            38                  80
    Neha              31                  35            52                  70


## Series
We could also create salary separately as a Series, as it's our label(target), and it's a single column. A series is typically used to represent a single list or column. Note that we usually separate features and labels in datasets for the purpose of training in machine learning. We would want our machine learning model to predict labels based on our features. Sometimes it would just be a single label that we want to predict.


```python
salary_series = pd.Series(
    [70, 80, 60, 75, 90, 65, 75, 85, 80, 70]
)

print(salary_series.head())
```

    0    70
    1    80
    2    60
    3    75
    4    90
    dtype: int64


We could also add custom indices to series, just like we have done for a dataframe, and give the series a name.


```python
salary_series_with_custom_indices = pd.Series(
    [70, 80, 60, 75, 90, 65, 75, 85, 80, 70],
    index=person_names,
    name='Salary (thousands)'
)

print(salary_series_with_custom_indices.head())
```

    Ali      70
    Sara     80
    Ahmed    60
    Emily    75
    David    90
    Name: Salary (thousands), dtype: int64


Instead of displaying the complete table, we can also set how many rows we want to see, for ex. 5. This option not just affects printing dataframes, it also affects other pandas outputs like describe.


```python
pd.set_option('display.max_rows', 5)
print(salary_df)
```

        Age (years)  Income (thousands)  Hours_Worked  Salary (thousands)
    0            32                  45            50                  70
    1            41                  50            45                  80
    ..          ...                 ...           ...                 ...
    8            36                  48            38                  80
    9            31                  35            52                  70
    
    [10 rows x 4 columns]


Let's unset this option back.


```python
pd.set_option('display.max_rows', None)
```

## File
So far, we added data directly in a dataframe, now let's try reading from a file, that's what we usually do. The file can be remote with a URL or local. We would go local this time, let's add our table in a file `salary.csv`.


```python
%%writefile salary.csv
Age(years),Income (thousands),Hours_Worked,Salary (thousands)
32,45,50,70
41,50,45,80
28,30,60,60
35,38,55,75
45,60,42,90
29,32,48,65
37,40,35,75
42,55,47,85
36,48,38,80
31,35,52,70
```

    Overwriting salary.csv


We can create a dataframe out of this and check the column names and shape.


```python
salary_df_from_file = pd.read_csv('salary.csv')
print(salary_df_from_file.columns)
print(salary_df_from_file.shape)
```

    Index(['Age(years)', 'Income (thousands)', 'Hours_Worked',
           'Salary (thousands)'],
          dtype='object')
    (10, 4)


We can check the statistical description of this dataframe with the describe method.

```
print(salary_df_from_file.describe())
```

```
       Age(years)  Income (thousands)  Hours_Worked  Salary (thousands)
count   10.000000           10.000000     10.000000           10.000000
mean    35.600000           43.300000     47.200000           75.000000
std      5.738757            9.989439      7.612855            9.128709
min     28.000000           30.000000     35.000000           60.000000
25%     31.250000           35.750000     42.750000           70.000000
50%     35.500000           42.500000     47.500000           75.000000
75%     40.000000           49.500000     51.500000           80.000000
max     45.000000           60.000000     60.000000           90.000000
```

## Index on file
This time lets add index on the file.



```python
%%writefile salary_with_index.csv
Age(years),Income (thousands),Hours_Worked,Salary (thousands)
Ali,32,45,50,70
Sara,41,50,45,80
Ahmed,28,30,60,60
Emily,35,38,55,75
David,45,60,42,90
Olivia,29,32,48,65
Michael,37,40,35,75
Sophia,42,55,47,85
Aryan,36,48,38,80
Neha,31,35,52,70


```

    Overwriting salary_with_index.csv


So we have added person names as indices to all the rows except the first row. This time, we just need to tell Pandas, the first column i.e. column 0 is meant for index with the index_col argument.


```python
salary_df_from_file = pd.read_csv(
    'salary_with_index.csv',
    index_col=0
)
print(salary_df_from_file.shape)
print(salary_df_from_file.head())
```

    (10, 4)
           Age(years)  Income (thousands)  Hours_Worked  Salary (thousands)
    Ali            32                  45            50                  70
    Sara           41                  50            45                  80
    Ahmed          28                  30            60                  60
    Emily          35                  38            55                  75
    David          45                  60            42                  90


We could slightly change the file by adding a Name column.


```python
%%writefile salary_with_names.csv
Name,Age(years),Income (thousands),Hours_Worked,Salary (thousands)
Ali,32,45,50,70
Sara,41,50,45,80
Ahmed,28,30,60,60
Emily,35,38,55,75
David,45,60,42,90
Olivia,29,32,48,65
Michael,37,40,35,75
Sophia,42,55,47,85
Aryan,36,48,38,80
Neha,31,35,52,70
```

    Overwriting salary_with_names.csv


And we could mention the name column as our index.


```python
salary_df_from_file = pd.read_csv(
    'salary_with_names.csv',
    index_col='Name'
)
print(salary_df_from_file.shape)
print(salary_df_from_file.head())
```

    (10, 4)
           Age(years)  Income (thousands)  Hours_Worked  Salary (thousands)
    Name                                                                   
    Ali            32                  45            50                  70
    Sara           41                  50            45                  80
    Ahmed          28                  30            60                  60
    Emily          35                  38            55                  75
    David          45                  60            42                  90


## Split dataset
We can split the dataset to two subsets one for training(say 80%, frac=0.8) and one for validatiing(say 20%)


```python
# you can set the argument random_state=0 if you want to see the same training
# dataframe each time you run the sample method
train_df = salary_df_from_file.sample(frac=0.8)
val_df = salary_df_from_file.drop(train_df.index)

print(train_df)
print(val_df)
```

             Age(years)  Income (thousands)  Hours_Worked  Salary (thousands)
    Name                                                                     
    Olivia           29                  32            48                  65
    Michael          37                  40            35                  75
    Neha             31                  35            52                  70
    Sophia           42                  55            47                  85
    Sara             41                  50            45                  80
    Ali              32                  45            50                  70
    David            45                  60            42                  90
    Ahmed            28                  30            60                  60
           Age(years)  Income (thousands)  Hours_Worked  Salary (thousands)
    Name                                                                   
    Emily          35                  38            55                  75
    Aryan          36                  48            38                  80


As you see, there is no overalp between the two datasets. Because we dropped the indices of train_df from the original dataframe to get the validation dataset. We can further split these two datasets to features(first 3 columns) and label(last column)


```python
features = ['Age(years)', 'Income (thousands)', 'Hours_Worked']
label = 'Salary (thousands)'

train_df_features = train_df[features]
train_series_labels = train_df[label]

val_df_features = val_df[features]
val_series_labels = val_df[label]
```

Note that we have retreived features as a dataframe with column names, and labels as a series(single column), the name of the column becomes the name of the series.


```python
print(val_df_features)
print('-' * 10)
print(val_series_labels)
print('-' * 10)
print(type(val_df_features))
print(type(val_series_labels))
```

           Age(years)  Income (thousands)  Hours_Worked
    Name                                               
    Emily          35                  38            55
    Aryan          36                  48            38
    ----------
    Name
    Emily    75
    Aryan    80
    Name: Salary (thousands), dtype: int64
    ----------
    <class 'pandas.core.frame.DataFrame'>
    <class 'pandas.core.series.Series'>


## Scale and Save
Let's do some scaling on each feature column and save it as a new dataframe. Note that it's usual to do some scaling or normalization on data when we train models, so that values for each feature fall in a similar range.


```python
# for simplicity, assigning the dataframe to a short variable

def scale(df):
    # this uses the standard formula for min-max scaling
    min_max_scaled_df = (df - df.min()) / (df.max() - df.min())
    return (min_max_scaled_df)


scaled_train_df_features = scale(train_df_features)
scaled_val_df_features = scale(val_df_features)

print(scaled_train_df_features.head())
print(scaled_val_df_features)
```

             Age(years)  Income (thousands)  Hours_Worked
    Name                                                 
    Olivia     0.058824            0.066667          0.52
    Michael    0.529412            0.333333          0.00
    Neha       0.176471            0.166667          0.68
    Sophia     0.823529            0.833333          0.48
    Sara       0.764706            0.666667          0.40
           Age(years)  Income (thousands)  Hours_Worked
    Name                                               
    Emily         0.0                 0.0           1.0
    Aryan         1.0                 1.0           0.0


So all the values are now between 0 and 1. We can save this to a new csv file with the to_csv method.


```python
scaled_train_df_features.to_csv('train_features.csv')
scaled_val_df_features.to_csv('test_features.csv')
```

Let's view the file content.


```python
!cat train_features.csv
!cat test_features.csv
```

    Name,Age(years),Income (thousands),Hours_Worked
    Olivia,0.058823529411764705,0.06666666666666667,0.52
    Michael,0.5294117647058824,0.3333333333333333,0.0
    Neha,0.17647058823529413,0.16666666666666666,0.68
    Sophia,0.8235294117647058,0.8333333333333334,0.48
    Sara,0.7647058823529411,0.6666666666666666,0.4
    Ali,0.23529411764705882,0.5,0.6
    David,1.0,1.0,0.28
    Ahmed,0.0,0.0,1.0
    Name,Age(years),Income (thousands),Hours_Worked
    Emily,0.0,0.0,1.0
    Aryan,1.0,1.0,0.0


Note that commas are added as delimiter by default.

The files we have created or interacting with should show up in the files pane.
![Notebook screenshot](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zgyt21rr1szaahp16jwb.png)

Alright, that's the ends of this post, so we have seen how to load data with Pandas, split the data and scale the features, which are usually done in a Machine learning lifecycle. Thanks for reading !!!

To avoid billing without usage, ensure you are stopping the notebook instance with the stop option.
![Stop notebook instance](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3bqpn7wrtfy5hsd5j01d.png)
