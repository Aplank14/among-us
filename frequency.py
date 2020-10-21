# importing libraries 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

from prettytable import PrettyTable

from collections import Counter

from utils import get_all_files
from utils import read_text_file
from utils import get_token_freq
from utils import generate_table

class ProcessText():

    def __init__(self):
        allWords = stopwords.words('english')
        allWords.extend(["i'm", "okay", "that's", "like", "yeah"])
        self.stop_words = set(allWords) - {"with"}
        self.speakers = {}
        self.allSpeakers = Counter()
        self.totalWords = {}

    def tokenize(self, words):
        words = words.lower()
        #tokens = word_tokenize(words)
        tokens = words.split(" ")
        return self.filter_stop_words(tokens)

    def filter_stop_words(self, wordList):
        return [w for w in wordList if not w in self.stop_words] 

    def print_results(self):
        
        # Print every players top 10 most common words
        for speaker, count in self.speakers.items():
            wordFreqPairs = count.most_common(10)
            table = generate_table(wordFreqPairs)
            print(f"\n{speaker}:")
            print(table)
        
        totalWords = PrettyTable()
        totalWords.field_names = ["Words", "Player"]
        totalWords.sortby = "Words"
        totalWords.reversesort = True
        for player, count in self.totalWords.items():
            totalWords.add_row([count, player])
        print(f"\nTotal Words by Player")
        print(totalWords)

        table = generate_table(self.allSpeakers.most_common(20))
        print(f"\nMost Common Words:")
        print(table)


    def analyze_text(self):
        
        textFiles = get_all_files('recognized')

        for textFile in textFiles:
            words = read_text_file(f"recognized/{textFile}")
            name = textFile.split(".")[0]
            if name.find("-") > 0:
                name = name[name.find("-")+1:]

            tokens = self.tokenize(words)
            wordFreq = get_token_freq(tokens)

            self.speakers[name] = wordFreq
            self.totalWords[name] = len(words)
            self.allSpeakers.update(tokens)

if __name__ == '__main__': 
    p1 = ProcessText()
    p1.analyze_text()    
    p1.print_results()
