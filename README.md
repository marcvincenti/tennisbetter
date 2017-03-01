# Tennis bet(ter)

You can run it with :
```
lein clean
lein cljsbuild [auto|once] [dev|prod]
lein ring server-headless
```

## Description

This project aim to teach us machine learning, data science and web development.  
The resulting application provide advices on how to bet on ATP & WTA players.

## Configuration

Use environment variables :
+ AWS_ACCESS_KEY : your amazon access key
+ AWS_SECRET_ACCESS_KEY : your amazon secret key
+ ML_MODEL_ID : The model to request
+ ML_MODEL_ENDPOINT : The endpoint of your model

The user must haev the following access :
*AmazonMachineLearningRealTimePredictionOnlyAccess*

## Notes

* TODO -> Crawl Bets on (at least) one website
* REDO -> Front-end (first time using react and I don't think it is a huge success...)

## Requirements

* JDK 1.7+
* Leiningen 2.x
