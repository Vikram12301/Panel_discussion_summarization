class Overall_Summary():
    """
    This a class for returning the summary of the discussion
    Class Members
    ----------
    spkrwise_df  : string
        path of the speakerwise text datafame 
    token : string
        Hugging face token
    """
    def __init__(self,spkrwise_df,token):
        self.spkrwise_df = spkrwise_df
        self.token = token

    def _fill(self,a,b):
        return b + ':' + a

    def _query(self,payload):
        API_URL = "https://api-inference.huggingface.co/models/knkarthick/MEETING_SUMMARY"
        API_TOKEN = self.token
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def transform(self):
        df = pd.read_csv(self.spkrwise_df)
        df['text'].fillna("", inplace = True)
        df['speech'] = df.apply(lambda x: self._fill(x['text'],x['speaker']),axis=1)
        result = ''''''
        for i in df['speech']:
            result += i
            result += '\n'
        
        output = self._query({
        "inputs": result
        })
        return summary[0]['summary_text']
