### ALEX KING
### *final project* part 1
### feature analysis of training data

## features: sentiment analysis, text length, normalized word count, NP bigram normalized count, JJ+NP bigram normalized count

import re , os , csv, nltk, spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

allfiles = os.listdir("Movie Reviews")

# Start counter and big loop to iterate over the files
counter = dict()
for filename in allfiles:
    title = filename[0:10]
    with open(os.path.join("Movie Reviews", filename)) as inputfile:
        content = inputfile.read()
        content = re.sub(r'<.*?>', " ", content)    # Removes weird symbols
        content = content.lower()
        tokens = nltk.word_tokenize(content)        # tokenizes all the words
        tagged = nltk.pos_tag(tokens)               # POS tags
        word_count = len(content)                   # Finds word count
# Bigram Counter
        for i in range(len(tagged)-1):
            first = tagged[i]
            second = tagged[i+1]
            if first[1] == "NN" or first[1] == "NNS":
                if second[1] == "NN" or second[1] == "NNS":
                    np_gram = (f"{first[0]} {second[0]}")
                    counter[np_gram] = counter.get(np_gram, 0) + 1
            if first[1] == "JJ":
                if second[1] == "NN" or second[1] == "NNS":
                    jj_gram = f"{first[0]} {second[0]}"
                    counter[jj_gram] = counter.get(jj_gram, 0) + 1
# Sentiment Analysis
        sentiment_score = SentimentIntensityAnalyzer().polarity_scores(content)
        pos = sentiment_score['pos']


        print(pos)
        print(sentiment_score('compound'))

### Write count stuff to files after they are sorted by a LAMBDA.
counter = list(counter.items())
counter = sorted(counter, key = lambda x:x[1], reverse=True)
print("printing...")
with open(title + "_features.csv", mode="w") as outfile:
    outfile.write(f"{'Sentiment: '} \t {sentiment_score} \n")
    outfile.write(f"{'Word Count:'} \t {str(word_count)} \n")
    outfile.write(f"{'Bigrams:'} \t {'Frequency:'} \n")
    for k, v in counter:
        outfile.write(f"{k}\t{v}\n")
print("Done!")
