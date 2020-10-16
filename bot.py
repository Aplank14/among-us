# importing libraries 
from pydub import AudioSegment 
from pydub.playback import play
from pydub.silence import split_on_silence 

import speech_recognition as sr 

import multiprocessing 
import threading
import time

import shutil
import os 
from os import listdir
from os.path import isfile, join

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

from prettytable import PrettyTable

from collections import Counter

def get_all_files(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

def recognize_speech(path = ""): 

    audio = AudioSegment.from_file(f"./audio_files/{path}", "aac")

    name = path.split(".")[0]
    if name.find("-") > 0:
        name = name[name.find("-")+1:]
          
    # split track where silence is 0.5 seconds  
    chunks = split_on_silence(audio, 
        # must be silent for at least 2 secondss 
        min_silence_len = 1000, 
        # consider it silent if quieter than -50 dBFS 
        silence_thresh = -60,
        # keep 500ms of trailing silence
        keep_silence=500
    ) 
  
    try: 
        os.mkdir(f"audio_chunks/{name}") 
    except(FileExistsError): 
        pass

    text = ""

    # process each chunk 
    for i, chunk in enumerate(chunks): 
        ret = process_chunk(chunk, name, i) 
        if ret != None:
            text = f"{text} {ret}"

    # store the text
    with open(f"./recognized/{name}.txt", "w+") as file:
        file.write(text)

    return words

def process_chunk(chunk, name, i):
        # Chunk is less than 1 second long              
        if(len(chunk) < 2000):
            return None

        # the filepath to export to
        filepath = f"./audio_chunks/{name}/chunk{i}.wav"

        # export audio chunk with 192k bitrate
        chunk.export(filepath, bitrate ='192k', format ="wav") 
  
        # create a speech recognition object 
        r = sr.Recognizer() 
  
        # recognize the chunk 
        with sr.AudioFile(filepath) as source: 
            audio_listened = r.listen(source) 
  
        try: 
            # try converting it to text 
            rec = r.recognize_google(audio_listened) 
            return rec
  
        # catch any errors. 
        except sr.UnknownValueError: 
            return None

        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 
            return None

def process_text(words):
    words = words.lower()

    #tokens = word_tokenize(words)
    tokens = words.split(" ")
    tokens = filter_stop_words(tokens)

    return tokens

def read_text_file(path):
    with open(path) as f:
        return f.read()

def filter_stop_words(wordList):
    allWords = stopwords.words('english')
    allWords.extend(["i'm", "okay", "that's", "like", "yeah"])
    stop_words = set(allWords) - {"with"}
    filtered = [w for w in wordList if not w in stop_words] 
    return filtered

def get_token_freq(tokens):
    counter = Counter(tokens)        
    wordFreq = counter.most_common(10)
    return wordFreq

def generate_table(wordFreq):
    table = PrettyTable()
    table.field_names = ["Count", "Word"]
    for pair in wordFreq:
        word, count = pair
        table.add_row([count,word])
    return table

if __name__ == '__main__': 
          
    files = get_all_files('audio_files')
    try: 
        os.mkdir('audio_chunks') 
    except(FileExistsError): 
        shutil.rmtree('audio_chunks')
        os.mkdir('audio_chunks') 

    try: 
        os.mkdir('recognized') 
    except(FileExistsError): 
        pass

    start = time.time()

    processes = []
    for file in files:
        p = multiprocessing.Process(target=recognize_speech, args=(file,))
        processes.append(p)
        p.start()
        
    for process in processes:
        process.join()

    end = time.time()

    print(end-start)

    textFiles = get_all_files('recognized')

    totalWords = PrettyTable()
    totalWords.field_names = ["Words", "Player"]
    totalWords.sortby = "Words"
    totalWords.reversesort = True

    totalFreq = Counter()

    for textFile in textFiles:
        words = read_text_file(f"recognized/{textFile}")
        name = textFile.split(".")[0]
        if name.find("-") > 0:
            name = name[name.find("-")+1:]

        tokens = process_text(words)
        wordFreq = get_token_freq(tokens)

        totalFreq.update(tokens)
        totalWords.add_row([len(words), name])

        table = generate_table(wordFreq)
        print(f"\n{name}:")
        print(table)


    table = generate_table(totalFreq.most_common(20))
    print(f"\nMost Common Words:")
    print(table)

    print(f"\nTotal Words by Player")
    print(totalWords)
