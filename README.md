# Twitter-Sentiment-Analysis-in-Python

Data Pipeline Architecture of Streaming Twitter Data into Apache Kafka cluster, performing simple sentiment analysis with afinn module, and finally storing the data into MongoDB. The high level architecture is pretty simple and can be seen in the following picture.

![Twitter Sentiment Analysis Pipeline in Python](https://traintestsplit.com/wp-content/uploads/twitterSentimentAnalysisPipeline.png)

## Pipeline Explanation

The pipeline makes use of the twitter streaming API in order to stream tweets in Python in real time, according to specified keywords. The tweets are pushed into a topic in the Kafka cluster by the aforementioned twitter producer. The streaming twitter data are in JSON format. 

A selection of the relevant fields, as well as simple sentiment analysis, are done during the streaming process. The code is implemented in such a way that the text field of tweets, as well as retweets, is not truncated.

On the other end, a MongoDB consumer consumes the streaming data and stores them in MongoDB for future use. MongoDB was chosen because of the JSON format of the data.

## Code Explanation

The kafkaTwitterStreaming.py script implements the twitter producer.
The kafkaMongoConsumer.py implements the MongoDB consumer.
Finally, the mongoToDf.py script connects to the MongoDB database. Subsequently, it provides the ability to save the data in pandas DataFrame format for further analysis and/or save the data in csv or other formats.

## Instructions on Running the Code

The following steps should be followed in order to run the code:
### Machine Preparation
1. Install and configure Apache Kafka.
2. Install and configure MongoDB.
3. Install and configure Python 3.
### Run the Code
1. Start zookeeper on one terminal.
2. Start kafka on another.
3. Create a kafka topic with desired number of partitions and other configurations.
3. Start mongo on a third terminal.
3. Run the mongodb consumer on one console, specifying the name of the topic you created, on the script.
4. Run the twitter stream producer on a second console, after specifying the desired keyword list to fetch tweets by in the script.
At this point, the tweets should be streaming from twitter into the Kafka topic and subsequently getting stored into MongoDB.
