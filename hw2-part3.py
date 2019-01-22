import re, nltk, argparse

def get_score(review):
    return int(re.search(r'Overall = ([1-5])', review).group(1))

def get_text(review):
    return re.search(r'Text = "(.*)"', review).group(1)

def read_reviews(file_name):
    """
    Dont change this function.

    :param file_name:
    :return:
    """
    file = open(file_name, "rb")
    raw_data = file.read().decode("latin1")
    file.close()

    positive_texts = []
    negative_texts = []
    first_sent = None
    for review in re.split(r'\.\n', raw_data):
        overall_score = get_score(review)
        review_text = get_text(review)
        if overall_score > 3:
            positive_texts.append(review_text)
        elif overall_score < 3:
            negative_texts.append(review_text)
        if first_sent == None:
            sent = nltk.sent_tokenize(review_text)
            if (len(sent) > 0):
                first_sent = sent[0]
    return positive_texts, negative_texts, first_sent


########################################################################
## Dont change the code above here
######################################################################



def process_reviews(file_name):
    positive_texts, negative_texts, first_sent = read_reviews(file_name)

    # There are 150 positive reviews and 150 negative reviews.
    #print(positive_texts)
    #print(negative_texts)

    # Your code goes here
    plus1character = r"\w+"
    stopwords = nltk.corpus.stopwords.words('english')

    positive_texts = [nltk.sent_tokenize(part) for part in positive_texts]
    positive_texts = [nltk.word_tokenize(sent) for part in positive_texts for sent in part]
    positive_texts = [word for sentence in positive_texts for word in sentence]
    positive_texts = [word.lower() for word in positive_texts if word.lower not in stopwords]
    positive_texts = [word for word in positive_texts if re.match(plus1character, word) is not None]

    negative_texts = [nltk.sent_tokenize(part) for part in negative_texts]
    negative_texts = [nltk.word_tokenize(sent) for part in negative_texts for sent in part]
    negative_texts = [word for sentence in negative_texts for word in sentence]
    negative_texts = [word.lower() for word in negative_texts if word.lower not in stopwords]
    negative_texts = [word for word in negative_texts if re.match(plus1character, word) is not None]

    pos_fd = nltk.FreqDist(positive_texts)
    with open('POSITIVE-unigram-freq.txt', 'w+') as f:
        for tup in pos_fd.most_common():
            f.write(tup[0] + " " + str(tup[1]) + "\n")

    neg_fd = nltk.FreqDist(negative_texts)
    with open('NEGATIVE-unigram-freq.txt', 'w+') as f:
        for tup in neg_fd.most_common():
            f.write(tup[0] + " " + str(tup[1]) + "\n")

    pos_big_fd = nltk.FreqDist(nltk.bigrams(positive_texts))
    with open('POSITIVE-bigram-freq.txt', 'w+') as f:
        for tup in pos_big_fd.most_common():
            f.write(tup[0][0] + " " + tup[0][1] + " " + str(tup[1]) + "\n")

    neg_big_fd = nltk.FreqDist(nltk.bigrams(negative_texts))
    with open('NEGATIVE-bigram-freq.txt', 'w+') as f:
        for tup in neg_big_fd.most_common():
            f.write(tup[0][0] + " " + tup[0][1] + " " + str(tup[1]) + "\n")

    positive_text = nltk.Text(positive_texts)
    positive_text.collocations()

    negative_text = nltk.Text(negative_texts)
    negative_text.collocations()

# Write to File, this function is just for reference, because the encoding matters.
def write_file(file_name, data):
    file = open(file_name, 'w', encoding="utf-8")    # or you can say encoding="latin1"
    file.write(data)
    file.close()


def write_unigram_freq(category, unigrams):
    """
    A function to write the unigrams and their frequencies to file.

    :param category: [string]
    :param unigrams: list of (word, frequency) tuples
    :return:
    """
    uni_file = open("{0}-unigram-freq-n.txt".format(category), 'w', encoding="utf-8")
    for word, count in unigrams:
        uni_file.write("{0:<20s}{1:<d}\n".format(word, count))
    uni_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assignment 2')
    parser.add_argument('-f', dest="fname", default="restaurant-training.data",  help='File name.')
    args = parser.parse_args()
    fname = args.fname

    process_reviews(fname)
