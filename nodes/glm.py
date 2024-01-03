import requests
import json
def chat(prompt,history):
    url='http://region-3.seetacloud.com:56296/'
    data = {'prompt': prompt,'history':history}
    response=requests.post(url, data=json.dumps(data))
    return response.json()['response'],response.json()['history']

def get_intitude(sentence,history):
    url='http://region-3.seetacloud.com:56296/'
    data = {'sentence': sentence}
    index_response=requests.get(url, data=json.dumps(data))
    index=index_response.json()['response']
    result={}
    result['response']=None
    result['history']=None
    result['index']=None
    if index in ['5','6','7','8','9','10']:
        chat_response,chat_history=chat(sentence,history)
        result['response']=chat_response
        result['history']=chat_history
    result['index']=index
    return result