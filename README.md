# Panel_discussion_summarization

## My Approach

The input of the file is revieved in .mp3 format
The file is converted to .wav format
An .rttm file is generated using 'pyannote/speaker-diarization@2.1' using hugging face to generate the timestamps of each speaker
This then converted to a csv format
Then the audio files are generated for those timestamps
The text is extracted from each audio file, speaker-wise
The overall summary of the file is then obtained using hugging face's "/knkarthick/MEETING_SUMMARY"


