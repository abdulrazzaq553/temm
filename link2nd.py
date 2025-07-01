from urlextract import URLExtract
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from collections import Counter

import seaborn as sns


import requests
import json


def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    

    
    # Classify each message based on its polarity
    df['Sentiment_Label'] = df['Sentiment'].apply(
        lambda score: 'Positive' if score > 0 else ('Negative' if score < 0 else 'Neutral')
    )
    
    # Overall sentiment score for the selected user
    avg_sentiment = df['Sentiment'].mean()
    
    sentiment_counts = df['Sentiment_Label'].value_counts()
    
    return avg_sentiment, sentiment_counts, df




def razzaq(file):
    headers = {
        "Authorization": "Bearer ya29.a0AcM612x6DYQHu0I7GzgaqQMqZhAZJowZi9VIVLeUG4NnkSyvRC5RiMidooZufv6VmIMasZ5vhc0J6BOleYvQl-vO5OrK-Mgxi8ETLekcWBzrCvMveEAkI53ZWKDqkiMqvT15JieXpMDZTxukeoNXjDacqV3Y68DtHCtqzBktaCgYKAe4SARASFQHGX2MinJwP176KfWhn7E6UVao5Nw0175"
    }

    para = {
        "name": file.name,  # Use the original file name
    }

    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': file
    }

    response = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )

    return response
def select(selected_user,df):
    if selected_user=='Overall':
        num_message= df['User'].shape[0]
        words=[]
        for mesage in df['Message']:
            words.extend(mesage.split())
        num_words= len(words)
        return num_message,num_words
    else:
        check=df[df['User']==selected_user]
        words=[]
        for mesage in check['Message']:
            words.extend(mesage.split())
        num_words= len(words)
        return check.shape[0],num_words
    
def media_shared(selected,df):
    again=df[df['User']==selected]
    if selected=='Overall':
       overall_len= len(df[df['Message']=='<Media omitted>\n'])   
       return overall_len   
    else:
       sel_len= len(again[again['Message']=='<Media omitted>\n'])     
       return sel_len  
        
urls=URLExtract()
def url(selected,df):
    again=df[df['User']==selected]
    if selected=='Overall':

       links=[]
       for link in df['Message']:
          links.extend(urls.find_urls(link))
       return len(links)
    else:
        links=[]
        for link in again['Message']:
          links.extend(urls.find_urls(link))
        return len(links)

def busy_user(select,df):
    if select=='Overall':
       bar=df['User'].value_counts().head(12)
     
       percent=pd.DataFrame(round((df['User'].value_counts()/df.shape[0])*100,2)).reset_index().rename(columns={'count':'Percentage'})
       percent01=pd.DataFrame(round((df['User'].value_counts()))).rename(columns={'count':'Total'})
    else:
         again=df[df['User']==select]
         bar=again['User'].value_counts().head(12)
         percent=pd.DataFrame(round((again['User'].value_counts()/df.shape[0])*100,2)).reset_index().rename(columns={'count':'Percentage'})
         percent01=pd.DataFrame(round((again['User'].value_counts()))).rename(columns={'count':'Total'})
    return bar,percent,percent01
def days(selected,df):
    if selected=='Overall':
        
       
        days=pd.DataFrame(df.groupby('dayss')['Message'].agg('count')).sort_values('Message',ascending=False).reset_index()
        return days
    else:
        check=df[df['User']==selected]
    
        days2=pd.DataFrame(check.groupby('dayss')['Message'].agg('count')).sort_values('Message',ascending=False).reset_index()
        return days2

def wordscount(selected,df):
    if selected!='Overall':
        df=df[df['User']==selected]

 
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=' '))
    return df_wc



def common_words(selected,df):
    f=open('stop_hinglish.txt','r',encoding='utf-8')
    ok=f.read()
    if selected=='Overall':
       tem=df[df['Message']!='<Media omitted>\n']
       words=[]
       for word in tem['Message']:
           for check in word.lower().split():
               if check  not in ok:
                 words.append(check)
        
       most_common=pd.DataFrame(Counter(words).most_common(20)) 
       return most_common
    
    else:
        check=df[df['User']==selected]
        tem=check[check['Message']!='<Media omitted>\n']
        f=open('stop_hinglish.txt','r',encoding='utf-8')
        ok=f.read()
        
        words=[]
        for word in tem['Message']:
           for check in word.lower().split():
               if check  not in ok:
                  words.append(check)

        
        most_common1=pd.DataFrame(Counter(words).most_common(20))         


        return most_common1
    

def emojis(selected,df):
    if selected=='Overall':
       
       emojis = []
       for check in df['Message']:
          for c in check:
             if isinstance(c, str) and ord(c) > 127:
                emojis.extend(c)
       emoji=pd.DataFrame(Counter(emojis).most_common(20))
       return emoji
 
    else:
        check=df[df['User']==selected]
        emojis = []
        for check in check['Message']:
            for c in check:
               if isinstance(c, str) and ord(c) > 127:
                   emojis.extend(c)

        emoji2=pd.DataFrame(Counter(emojis).most_common(20))
        return emoji2
    

def Month(selected,df):
    if selected=='Overall':
        Month=pd.DataFrame(df['NEW_Month'].value_counts()).reset_index()
        return Month

    else:
        check=df[df['User']==selected]
        Month1=pd.DataFrame(check['NEW_Month'].value_counts()).reset_index()
        return Month1

def year(selected,df):
    if selected=='Overall':
        one=pd.DataFrame(df['NEW_Month']+'-'+df['year'])
        df['new']=one
        month=pd.DataFrame(df.groupby('new')['Message'].agg('count')).reset_index()
        return month
    else:
        check=df[df['User']==selected]
        one=pd.DataFrame(check['NEW_Month']+'-'+check['year'])
        check['new']=one
        month21=pd.DataFrame(check.groupby('new')['Message'].agg('count')).reset_index()
        return month21
def daily(selected,df):
    if selected=='Overall':
        time_intervals = {
        '12AM': '12AM-1AM', '1AM': '1AM-2AM', '2AM': '2AM-3AM', '3AM': '3AM-4AM', '4AM': '4AM-5AM', 
        '5AM': '5AM-6AM', '6AM': '6AM-7AM', '7AM': '7AM-8AM', '8AM': '8AM-9AM', '9AM': '9AM-10AM', 
        '10AM': '10AM-11AM', '11AM': '11AM-12PM', '12PM': '12PM-1PM', '1PM': '1PM-2PM', 
        '2PM': '2PM-3PM', '3PM': '3PM-4PM', '4PM': '4PM-5PM', '5PM': '5PM-6PM', 
        '6PM': '6PM-7PM', '7PM': '7PM-8PM', '8PM': '8PM-9PM', '9PM': '9PM-10PM', 
        '10PM': '10PM-11PM', '11PM': '11PM-12AM'
        }
        df['tem']=df['Times'].map(time_intervals)
        month=pd.DataFrame(df.groupby('tem')['Message'].agg('count')).sort_values(by='Message',ascending=False).reset_index()
        return month
    else:
         check=df[df['User']==selected]
         time_intervals = {
        '12AM': '12AM-1AM', '1AM': '1AM-2AM', '2AM': '2AM-3AM', '3AM': '3AM-4AM', '4AM': '4AM-5AM', 
        '5AM': '5AM-6AM', '6AM': '6AM-7AM', '7AM': '7AM-8AM', '8AM': '8AM-9AM', '9AM': '9AM-10AM', 
        '10AM': '10AM-11AM', '11AM': '11AM-12PM', '12PM': '12PM-1PM', '1PM': '1PM-2PM', 
        '2PM': '2PM-3PM', '3PM': '3PM-4PM', '4PM': '4PM-5PM', '5PM': '5PM-6PM', 
        '6PM': '6PM-7PM', '7PM': '7PM-8PM', '8PM': '8PM-9PM', '9PM': '9PM-10PM', 
        '10PM': '10PM-11PM', '11PM': '11PM-12AM'
        }
         check['tem']=check['Times'].map(time_intervals)
         month1=pd.DataFrame(check.groupby('tem')['Message'].agg('count')).sort_values(by='Message',ascending=False).reset_index()
         return month1


def search(select,df):
    if select=='Overall':
        df.drop('new',axis=1,inplace=True)
        df.drop('tem',axis=1,inplace=True)
        return df
    else:
         check=df[df['User']==select]
         
         return check
    
