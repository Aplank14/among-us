from pydub import AudioSegment 
from pydub.silence import split_on_silence 

import speech_recognition as sr 

import multiprocessing 
import threading

import time

import shutil
import os 

from utils import get_all_files
from utils import is_aac
  
class Speech:
    def __init__(self):
        return

    def recognize_speech(self, path = ""): 

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
            ret = self.process_chunk(chunk, name, i) 
            if ret != None:
                text = f"{text} {ret}"

        # store the text
        with open(f"./recognized/{name}.txt", "w+") as file:
            file.write(text)

        return words

    def process_chunk(self, chunk, name, i):
        # Chunk is less than 2 seconds long              
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

    def analyze_audio(self):

        files = get_all_files('audio_files')
        files = [f for f in files if is_aac(f)]

        # Clear audio_chunks folder
        try: 
            os.mkdir('audio_chunks') 
        except(FileExistsError): 
            shutil.rmtree('audio_chunks')
            os.mkdir('audio_chunks') 

        # Make a directory for the text
        try: 
            os.mkdir('recognized') 
        except(FileExistsError): 
            pass

        start = time.time()

        processes = []
        for file in files:
            p = multiprocessing.Process(target=self.recognize_speech, args=(self,file,))
            processes.append(p)
            p.start()
            
        for process in processes:
            process.join()

        end = time.time()

        print(f"Analyzed audio in {end-start/60} minutes")

if __name__ == '__main__': 
    p1 = Speech()
    p1.analyze_audio()
