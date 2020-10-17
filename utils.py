from os import listdir
from os.path import isfile, join

from prettytable import PrettyTable
from collections import Counter

def is_aac(file): 
    return file.endswith(".aac") 

def get_all_files(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def read_text_file(path):
    with open(path) as f:
        text = f.read()
    return text

def get_token_freq(tokens):
    return Counter(tokens)        

def generate_table(wordFreq):
    table = PrettyTable()
    table.field_names = ["Count", "Word"]
    for pair in wordFreq:
        word, count = pair
        table.add_row([count,word])
    return table
