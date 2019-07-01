# Twitter-Sentiment-Analysis-in-Python

Data Pipeline Architecture of Streaming Twitter Data into Apache Kafka cluster, performing simple sentiment analysis with afinn module, and finally storing the data into MongoDB. The high level architecture is pretty simple and can be seen in the following picture.

![Twitter Sentiment Analysis Pipeline in Python](https://traintestsplit.com/wp-content/uploads/twitterSentimentAnalysisPipeline.png)

## Pipeline Explanation

The pipeline makes use of the twitter streaming API in order to stream tweets in Python in real time, according to specified keywords. The tweets are pushed into a topic in the Kafka cluster by the aforementioned twitter producer. The streaming twitter data are in JSON format. 

A selection of the relevant fields, as well as simple sentiment analysis, are done during the streaming process.

On the other end, a MongoDB consumer consumes the streaming data and stores them in MongoDB for future use. MongoDB was chosen because of the JSON format of the data.
