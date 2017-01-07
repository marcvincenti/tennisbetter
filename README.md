# Tennis bet(ter)

You can run it with :
```
lein clean
lein cljsbuild [auto|once] [dev|prod]
lein ring server-headless
```

## Configuration

Use environment variables :
+ AWS_ACCESS_KEY : your amazon access key
+ AWS_SECRET_ACCESS_KEY : your amazon secret key
+ AWS_DEFAULT_REGION : the region for your model
+ ML_MODEL_ID : The model to request

## Notes

* PATCH -> date format is wrong for the end of 2016
* TODO -> Crawl Bets on (at least) one website
* TODO -> Crawl Pts/Rank for players

## Description

This project aim to teach us machine learning, data science and web development.  
The resulting application provide advices on how to bet on ATP & WTA players.

## Requirements

* JDK 1.7+
* Leiningen 2.x
