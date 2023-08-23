## Function to get sentiment of the Email
def get_sentiment(text):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    # Enter language service credentials
    endpoint = ""
    key = ""

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    documents = [str(text)]

    result = text_analytics_client.analyze_sentiment(documents, show_opinion_mining=True)
    docs = [doc for doc in result if not doc.is_error]
    
    for idx, doc in enumerate(docs):
        #print(f"Email text :\n {documents[idx]}")
        print(f"Overall sentiment:\n {doc.sentiment}")
        print(f"Confidence Score:\n {doc.confidence_scores}")
        
    return result


## Function to call Azure Custom text classification model

def sample_classify_document_single_label(document):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    
    # Mention the project type and deployment name from azure custom model deployments
    project_name = ""
    deployment_name = ""
    
    # Enter language service credentials
    credential = AzureKeyCredential("")
    endpoint="" 
   
    text_analytics_client = TextAnalyticsClient(endpoint, credential)
        
    poller = text_analytics_client.begin_single_label_classify(
        document,
        project_name=project_name,
        deployment_name=deployment_name
    )
    
       
    document_results = poller.result()
    for doc, classification_result in zip(document, document_results):
        #print("Check0:",classification_result.kind)
        print("\nClassification with Custom Model")
        #print("check2:",classification)
        #print("check3:",classification_result.classifications)

    return classification_result

        

# Classify Complaints function
def classify_complaints_3(text):
    try:
        # Calling the custom model
        result = sample_classify_document_single_label([text])

        # Checking condition for non complaints
        if (dict(result.classifications[0])['category']=='Complaint'):
            flag1='NA'
            # Calling sentiment model to check sentiment
            score = get_sentiment(text.capitalize())
            # The the negative score is mode than negative 0.60 it will retirn complaint else non complaints
            if (score[0].confidence_scores.negative>=0.50):
                flag1 = "Complaint"
            elif (score[0].confidence_scores.positive>=0.60):
                flag1 ="Non Complaint"     
            else:
                flag1 ="Complaint"
            response = {}
            response['Flag'] = flag1
            response['Score'] = str(score[0].confidence_scores)
            
            return response
                

        else:
            # Calling sentiment model to check sentiment
            score = get_sentiment([text])
            # The the negative score is mode than .40 it will retirn complaint else non complaints
            if (score[0].confidence_scores.negative>0.40):
                flag1 =  "Complaint"
            else:
                flag1 =  "Non Complaint" 
            response = {}
            response['Flag'] = flag1
            response['Score'] = str(score[0].confidence_scores)
            
            return response
            

    except Exception as e: 
        print("Exception occured. Error Details : \n",e)
