from pydub import AudioSegment
import csv
import whisper
import requests
from pyannote.audio import Pipeline
import librosa
import soundfile as sf
import os
import pandas as pd


class mp3_2_wav():
    """
    This a class for converting mp3 file to wav file
    Class Members
    ----------
    name  : string
        path of the mp3 file
    """
    def __init__(self,name):
        self.name = name
    def convert(self):
        audio = AudioSegment.from_mp3(self.name)
        name = self.name.split('.')[0]+'.wav'
        audio.export(name, format='wav')
        return name 

class Diarization():
  """
  This class is to identify the start and duration of each speaker throughout the mp3 file
  Class Members
  ----------
  name  : string
        path of the wav file
  token: string
        Hugging face token
  """ 
  def __init__(self,wav_file,token):
    self.token = token
    self.wav_file = wav_file
  
  def diarize(self):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                        use_auth_token=self.token)
    # apply the pipeline to an audio file
    diarization = pipeline(self.wav_file)
    name = self.wav_file.split('.')[0]+'.rttm'
    # dump the diarization output to disk using RTTM format
    with open(name, "w") as rttm:
        diarization.write_rttm(rttm)
    return name

class rttm_2_df():
  """
  This class is to convert the rttm file to csv file
  Class Members
  ----------
  rttm  : string
      path of the rttm file  
  """     
  def __init__(self,rttm):

    self.rttm = rttm

  def convert(self):
    with open(self.rttm, 'r') as input_file:
        # Read the RTTM data into a list of lines
        lines = input_file.readlines()

        # Open the CSV file for writing
        with open('output.csv', 'w') as output_file:
            # Create a CSV writer
            writer = csv.writer(output_file)

            # Iterate over the lines in the RTTM file
            for line in lines:
                # Split the line into fields
                fields = line.split()

                # Write the fields to the CSV file
                writer.writerow(fields)
        return 'output.csv'

class Extractor():
    
  """
  This class saves the audio files speakerwise
  Class Members
  ----------
  csv_name  : string
      path of the rttm file  
  wav_file_name : string
      path of wav file
  """ 
    def __init__(self,csv_name,wav_file_name):
        self.csv_name = csv_name
        self.wav_file_name = wav_file_name

    def extract(self):
        spkrs = pd.read_csv(self.csv_name,header=None)
        df = spkrs[[3,4,7]]
        df.columns=['start','duration','speaker']
        df['end'] = df['start'] + df['duration']
        try:
            os.mkdir('/content/audio_files')
        except:
            pass
        
        for i in range(len(df)):
            start=df.iloc[i]['start']
            duration_1=df.iloc[i]['duration']
            y, sr = librosa.load(self.wav_file_name, offset=start, duration=duration_1)
            sf.write('audio_files/'+str(i)+'.wav', y, sr)
        return 'audio_files'

class user_wise_text():

  """
  This class saves the text speakerwise
  Class Members
  ----------
  audio_files  : string
      path of the audio files durectory
  diarization_csv : string
      path of csv file
  """ 
    def __init__(self,audio_files,diarization_csv):
        self.audio_files = audio_files
        self.diarization_csv = diarization_csv

    def transform(self):
        text=[]
        mean = pd.read_csv(self.diarization_csv,header=None)
        model = whisper.load_model("base")
        for i in range(len(os.listdir(self.audio_files))):
            result = model.transcribe(audio_files+'/'+str(i)+".wav")
            text.append(result['text'])
        
        spkrwise_text = pd.DataFrame({'text':text,'speaker':mean[7]})
        spkrwise_text.to_csv('spkrwise_text.csv',index=False)
        return 'spkrwise_text.csv'

