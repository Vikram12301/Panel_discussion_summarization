from mp3_to_wav import *
from summarizer import *

wav_file_name = mp3_2_wav('/content/Y2Mate.mp3').convert()
rttm_file_name = Diarization(wav_file_name,'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').diarize()
output_csv = rttm_2_df(rttm_file_name).convert()
audio_files = Extractor(output_csv,wav_file_name).extract()
spkr_txt = user_wise_text(audio_files,output_csv).transform()
summary = Overall_Summary(spkr_txt,'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').transform()
print(summary)