from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server
import time
from Clean_mail import email_processing
from azure_lang import *

app = Flask(__name__)

def flag_complaints():
    
  
    put_code("Welcome to Complaints Classification Application..!")
    count=0
    add_more = True
    while add_more: 
        
        text=input("Enter text to check Complaint Email",type='text')
        #put_code("Please wait for 5 secs, we are calling the Model for prediction.")
        put_text('Your Entered Text is: ',text)
        
        
        with put_loading():
            put_code("Please wait , we are working on magic to get the model result...")
            res = classify_complaints_3(email_processing(text)[0])
            
            time.sleep(3)  # Some time-consuming operations     
                      
        
        #put_text('Your Entered Text is: ',text)
       
        put_text('------------------------------------------------')
       
        
        put_text("Model Output: ")
        
        
        put_table([
                    {"Entered Text":text,"Complaint Flag":str(res['Flag']),"Sentiment Score":str(res['Score'])}
                ], header=["Entered Text", "Complaint Flag","Sentiment Score"]) 

           
        
        add_more = actions(label="Would you like to search more ?", 
                        buttons=[{'label': 'Yes', 'value': True}, 
                                 {'label':'No', 'value': False}])
        
        count= count+1
        put_text("--------------------------")
        put_text(f"Search History : You have checked for {count} complaints emails | Search results shown above. ")
        
        put_text("--------------------------")
        #clear(scope=- 1) 
      
    put_text("Thank You for using the Complaints Classification Application ..! ")



app.add_url_rule('/complaints_v1', 'webio_view', webio_view(flag_complaints,session_expire_seconds=120),
            methods=['GET', 'POST', 'OPTIONS'])



app.run(host='localhost', port=80)