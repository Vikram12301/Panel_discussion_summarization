# Panel_discussion_summarization

## My Approach

<p> The input of the file is revieved in .mp3 format </p>
<p> The file is converted to .wav format </p>
<p> An .rttm file is generated using 'pyannote/speaker-diarization@2.1' using hugging face to generate the timestamps of each speaker </p>
<p> This then converted to a csv format </p>
<p> Then the audio files are generated for those timestamps </p>
<p> The text is extracted from each audio file, speaker-wise </p>
<p> The overall summary of the file is then obtained using hugging face's "/knkarthick/MEETING_SUMMARY" </p>


## How to run the code?

<p> It is easy to execute the code in google colab by just uploading the .mp3 file and running all the cells</p>

## Results

<p> In CPU it took 45 minutes to execute the entire code for the audio uploaded</p>
<p> In GPU it took less than a minute to execute the entire code for the audio uploaded</p>
