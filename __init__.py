#import pandas as pd
import logging
import azure.functions as func
import pandas as pd
import numpy as np
import pickle
import torch
from transformers import BertTokenizer, BertModel

model_bert = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

bst = pickle.load(open('MyFunction/xgb_model.pkl', "rb"))

def text_to_vector(text):
            global model_bert
            #text = str(text) if text is not None else ''
            inputs = tokenizer([text], return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = model_bert(**inputs)
            embeddings = outputs.last_hidden_state
            mask = inputs.attention_mask
            masked_embeddings = embeddings * mask.unsqueeze(-1)
            summed = torch.sum(masked_embeddings, 1)
            summed_mask = torch.clamp(mask.sum(1), min=1e-9)
            mean_pooled = summed / summed_mask.unsqueeze(-1)

            return mean_pooled[0].numpy()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
            request_data = req.get_json()

            description = request_data.get('description')
            frame = pd.DataFrame(request_data.get('frame'))

            if description is None or frame is None:
                return func.HttpResponse("Error: The request must include a 'description' and a 'frame'", status_code=400)

            vector = text_to_vector(description)
            frame_vectors = pd.DataFrame([vector], columns=[f'vector_{i}' for i in range(len(vector))])
            frame = pd.concat([frame, frame_vectors], axis=1)

            price = int(bst.predict(frame.values)[0])

            return func.HttpResponse(str(price))
    #func.HttpResponse(str(price))

    except Exception as e:
        
            return func.HttpResponse(f"Error: {str(e)}", status_code=500)

