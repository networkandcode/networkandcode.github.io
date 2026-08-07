---
canonical_url: "https://dev.to/aws-builders/ml-learning-byte-linear-regression-21f9"
date: "2023-10-23"
title: "M/L Learning Byte: Linear Regression"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fsource.unsplash.com%2Ffeatured%2F%3Fmaths"
tags: "machinelearning, python, jupyter, aws"
categories: "machinelearning, python, jupyter, aws"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/ml-learning-byte-linear-regression-21f9)**

Hello :wave:, in this post, we shall see the procedures involved in training a simple linear model with Keras API in TensorFlow. Note that we will not optimize the model by training it iteratively with different parameters, we will focus more on some of the standard steps involved. You may check this [post](https://dev.to/aws-builders/ml-learning-byte-load-split-and-scale-data-1n31):page_facing_up: for a refresher on some of the pandas methods we use here. Ready to go!!!

## Sagemaker Studio Lab
I'll be doing this exercise on the Amazon [Sagemaker Studio Lab](https://studiolab.sagemaker.aws):free:, you can request for an account there and once it's approved you should receive a sign up link, note that the approval expires in 7 days, so you should better signup before that.

I am logging into the studio lab and start a runtime with CPU as the compute type.
![Start runtime](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qsbl332ee02w9o34qos4.png)

Open the project once the runtime is started. Ensure popups are allowed for this site on your browser. The jupyter lab i.e. the Sagemaker studio lab should be opened.

Click the plus icon next to the Getting Started notebook, to see the launcher. From there, I am launching a notebook:notebook_with_decorative_cover: with the sagemaker-distribution environment.
![New notebook](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wroe9dz2zio1re5wy5eh.png)

We will be executing code covered in this post, in the notebook we just launched.

## Dataset
Let's say we have a simple dataset like below(generated with ChatGPT):

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

In easy terms, regression is all about predicting labels/targets(numbers) from one ore more inputs/features(numbers). We say it's linear regression when we could potentially use a linear function to show the relation between the features and labels.

Let's consider `Age, Income and Hours worked` are features and `Salary` is the label that we want to predict. And to start with(baseline) we are assuming this model is linear meaning it should approximately fit a [linear equation](https://en.wikipedia.org/wiki/Linear_algebra)(y = w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + w<sub>3</sub>x<sub>3</sub> + b) meaning you should be able to predict the value of y(Salary) with the values of x<sub>1</sub>(Age), x<sub>2</sub>(Income) and x<sub>3</sub>(Hours_Worked) using the linear equation. However you don't know what the weights(w<sub>1</sub>, w<sub>2</sub>, w<sub>3</sub>) and bias(b) are. That is your model's job to find the best weights and bias, that's when you model is trained or learned.

Usually datasets are quite huge and are loaded from URLs, we have chosen a small dataset here for the purpose of learning the concepts covered in this post in a simpler way.

## File
Add a file in our studio lab, that represents the dataset in CSV format.
```
%%writefile dataset.csv
Age (years),Income (thousands),Hours_Worked,Salary (thousands)
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
```
Writing dataset.csv
```

## Data readiness
Let's load our dataset and shuffle it.
```
import pandas as pd

df = pd.read_csv('dataset.csv')
df = df.sample(frac=1)
```

Let's add extra columns to the dataframe by min-max scaling each of the features.
```
for feature in ['Age (years)', 'Income (thousands)', 'Hours_Worked']:
    df[f'scaled_{feature}'] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())

print(df.head(1))
```
```
 Age (years)  Income (thousands)  Hours_Worked  Salary (thousands)  \
9           31                  35            52                  70   

   scaled_Age (years)  scaled_Income (thousands)  scaled_Hours_Worked  
9            0.176471                   0.166667                 0.68
```

We can now split the dataframe into training(80%) and test(20%) dataframes.
```
train_df = df.sample(frac=0.8)
test_df = df.drop(train_df.index)
```

## Model
We have the data ready. It's time to create the model.

We will be building a [sequential model](https://www.tensorflow.org/guide/keras/sequential_model) for this purpose with just one layer. That layer will have 3 inputs(features) and 1 output(label).
```
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[3])
])
```
Note that sequential models are used in Keras when there are a stack of layers with each layer having one input tensor and one output tensor.

A tensor is nothing but TensorFlow's version of a numpy array with more features, which inturn is similar to a list in Python, but with extra attributes/methods.

In our case, it's 3 features how ever it's only one tensor, think of it like a rectangular matrix with 3 columns. Likewise, though it's only one output/label, it's still one tensor(a single column matrix).

We have created the model, initially our model will have random weights and zero bias. Collectively the weight and bias are reffered to as just weights.
```
w,b = model.weights

tf.print('Initial weights:', w)
tf.print('Initial bias:', b)
```
```
Initial weights: [[0.787701]
 [-0.283494174]
 [0.238811135]]
Initial bias: [0]
```

One things to note. TensorFlow is usually known for *Deep Neural Networks(DNN)*. What we have done still follows the same approach we would rather use for neural networks but our model is not deep it just has 1 layer(depth = 1) and not wide either, just 1 unit in the layer(width = 1). And we do not have any activation functions, which are used when we need non linear functions(for ex. [Rectifier function](https://en.wikipedia.org/wiki/Rectifier_(neural_networks))) to map output with input

## Compile
Our model's performance could be calcualted based on a loss function. Mean average loss is one such loss functions used with regression. And there should be a way(algorithm) using which we can evaluate this loss, which is nothing but the optimizer. Adam is one populary used optimizer.

Let's compile our model with these settings.
```
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss='mean_absolute_error'
)
```

## Train
We can finally train(fit) the data and assign it as a variable. We shall keep 20% of the training data as validation data, and determine the loss for each of these sub datasets. I have set verbose as 0, to suppress terminal output while the training happens.
```
features = ['scaled_Age (years)', 'scaled_Income (thousands)', 'scaled_Hours_Worked']
label = 'Salary (thousands)'

history = model.fit(
    train_df[features],
    train_df[label],
    validation_split=0.2,
    verbose=0
)
```

We have done the training, let's see the what the loss is.
```
print(history.history)
```
```
{'loss': [78.85342407226562], 'val_loss': [70.26549530029297]}
```

So the training loss is 79 and the validation loss is 70 approximately. We have a parameter called epoch, that tells for how many full(one full training dataset) iterations did the training happen.
```
print(len(history.epoch))
```
```
1
```
So by default it's just 1 epoch.

Let's try with epoch as 10.
```
history = model.fit(
    train_df[features],
    train_df[label],
    validation_split=0.2,
    verbose=0,
    epochs=10
)

print(history.history)
```
```
{'loss': [78.8173599243164, 78.81478881835938, 78.81220245361328, 78.80962371826172, 78.80704498291016, 78.8044662475586, 78.80188751220703, 78.79930877685547, 78.79672241210938, 78.79415130615234], 'val_loss': [70.24092102050781, 70.23916625976562, 70.23741149902344, 70.23565673828125, 70.23390197753906, 70.23213958740234, 70.23037719726562, 70.22862243652344, 70.22686767578125, 70.22511291503906]}
```

So this time we see the training and validation losses for 10 epochs. We can access just the final training and validation with the last index.
```
print('Final training loss:', history.history['loss'][-1])
print('Final validation loss:', history.history['val_loss'][-1])
```
```
Final training loss: 78.79415130615234
Final validation loss: 70.22511291503906
```
We can see there is no much improvement in the losses with increasing the epochs. Also, the loss was kinda similar in all the epochs. We will try with a higher value, say 1000 epochs.
```
history = model.fit(
    train_df[features],
    train_df[label],
    validation_split=0.2,
    verbose=0,
    epochs=1000
)
print('done')
```
```
done
```

As there are 1000 losses each for training and validation, rather than printing, we can try plotting the losses in each epoch.
```
import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='validation loss')

plt.xlabel('Epoch')
plt.ylabel('Loss')

plt.legend()
```
![Plot loss](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k59lzvp29l75y2c5hnnb.png)

We will see what our final weights and bias are.
```
w, b = model.weights
tf.print(w, b)
```
```
[[1.7877351]
 [0.716494739]
 [1.23881245]] [0.999988]
```

Note that these graphs are not the best, and our example is not the best either, it was quite a small dataset. The aim of this exercise is not to really optimize the training or to get the best loss values, or the weights and bias at which we get the best loss. It was more on knowing the procedures involved in training a simple(one layer, one unit) linear network with TensorFlow.

## Evaluate & Predict
We'll see a couple more steps, first, we can evaluate our model with the test dataset i.e. we see what's the test loss is.
```
model.evaluate(
    test_df[features],
    test_df[label],
    verbose=0
)
```
```
76.93582153320312
```

And predict the values for a new dataset that doesn't have labels. Let's add a new file for the prediction dataset.
```
%%writefile to_predict.csv
Age (years),Income (thousands),Hours_Worked
33,46,49
38,52,44
27,28,59
44,58,43
30,34,51
50,70,30
29,33,47
34,39,56
41,54,41
48,65,36
```
```
Writing to_predict.csv
```

We can scale the features just like we have done for the training data.
```
to_predict = pd.read_csv('to_predict.csv')
to_predict = (to_predict - to_predict.min()) / (to_predict.max() - to_predict.min())
```

We can predict now.
```
print(model.predict(to_predict))
1/1 [==============================] - 0s 38ms/step
[[2.5850587]
 [2.8624647]
 [2.2388005]
 [3.3884692]
 [2.2325983]
 [3.5042179]
 [1.9669406]
 [2.842394 ]
 [3.0016134]
 [3.5197716]]
```

I know the predictions are bad, it's predicting quite low salaries:dollar: compared to the training set.

## Math
Let's see the math used in calculating the predictions. We know the final weights and bias are 1.7877351, 0.716494739, 1.23881245, 0.999988. Let's take the first row from to_predict.
```
print(to_predict.head(1))
```
```
Age (years)  Income (thousands)  Hours_Worked
0      0.26087            0.428571      0.655172
```

Let's do the math with the linear equation. y = w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + w<sub>3</sub>x<sub>3</sub> + b. 
This becomes y = `1.7877351*0.26087 + 0.716494739*0.428571 + 1.23881245*0.655172 + 0.999988` = `2.585058552816369` This kinda matches with the first entry of predictions(2.5850587).

## Summary
So we saw some important :star: steps such as creating, training, evaluating and predicting with a model... We could build upon this knowlegde to try regression with a bigger dataset and optimize our model with low losses, fine tune parameters, yield better predictions, which are kinda iterative in nature and are usually implemented with automated workflows i.e. pipelines.

That's it for the post, thanks for reading!!!
