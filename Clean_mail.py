

# import alll required libs
import pandas as pd
import http.client, urllib.request, urllib.parse, urllib.error, base64
import re


# Function to extract text above signature
def extract_above_signature(text):
    if len(text)>5:
        text_copy = text
        #print(text_copy)
        pointers = ['Thanks','Best Regards' ,'Name :','Kind Regards','Kind  regards,','Best','Regards','sincerely','respectfully','thanks','regards,','Yours faithfully','regards,', 'disclaimer','Description:','--','Sent ','Sent from']
        locations = [text_copy.find(p) for p in pointers]
        #print(locations)
        if max([l for l in locations])>-1:
            nearest = min([l for l in locations if l>-1])
            #print(nearest)
            text = text[:nearest]
            
    text=text.replace('#',' denotesnumber ')
    text=text.replace('$',' moneydollar ')
    text=text.replace('? ',' askingquestion ')
    
    #print(text)
    return text
# Function to extract text below greetings
def extract_below_greeting(text):
    if len(text)>5:
        text_copy = text
        #print(text_copy)
        pointers = ['Hi Team','Dear Sir','Dear Madam','Description of issue :','Hi Sir/Madam','Hi ','Hi Madam','event:','Good afternoon','Good Morning','Good morning','Morning ','Subject:','Learn why this is important']
                   
        locations = [text_copy.find(p) for p in pointers]
        #print(locations)
        if max([l for l in locations])>-1:
            nearest = min([l for l in locations if l>-1])
            #print(nearest)
            text = text[nearest:]
    return text



# Function for cleaning text
def clean_data(text):
    text=text.replace('\\r',' ')
    text=text.replace('\\n',' ')
    
    text=text.replace('\r',' ')
    text=text.replace('\n',' ')
    text=text.replace('\\t',' ')
    text=text.replace('\t',' ')
    text=text.replace('\\xa0',' ')
    #text=text.replace('')
    
    while '  ' in text:
        text=text.replace('  ',' ')
    
    return text

# function for preprocessing text
def preprocess_data(text):
    # remove email id
    cleanr = re.compile('\S*@\S*\s?')
    text = re.sub(cleanr, ' ', text)
        
    # remove url 
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, ' ', text)
    text = re.sub(r'http\S+', ' ', text)
    
    # remove emojis
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    text=regrex_pattern.sub(r'',text)

    #limit only to letters
    #text=re.sub('[^A-Za-z ]+',' ', text)
    
    # Lower Case
    
    
    while '  ' in text:
        text=text.replace('  ',' ')
    
    return text


# Function to clean PII using azure language service
def clean_pii(text):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient
    )

   
    credential = AzureKeyCredential("")
    endpoint=""      
    
    text_analytics_client = TextAnalyticsClient(endpoint, credential)

    text_analytics_client = TextAnalyticsClient(endpoint, credential)
      
    result = text_analytics_client.recognize_pii_entities([text])
    redacted_text = [doc.redacted_text for doc in result if not doc.is_error]
    print("Inside PII")
    return redacted_text


# Function to call all the above function in sequence
def email_processing(text):
    text = extract_above_signature(text)
    #text = extract_below_greeting(text)
    text = clean_data(text)
    text = preprocess_data(text)
    text = extract_below_greeting(text)
    text = clean_pii(text)
 
    return text



