from transformers import AutoTokenizer, AutoModel
from Authent import *
import pandas as pd
from datasets import Dataset
import faiss

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id)



def cls_pooling(model_output):
    return model_output.last_hidden_state[:,0]

def get_embedding(text_list):
    encoded_input = tokenizer(text_list, padding = True, truncation = True, return_tensors ="pt")
    encoded_input = {k: v for k,v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)

     

def create_question_embeddings(question) -> str: 
        question_embedding = get_embedding([question]).cpu().detach().numpy()
        return question_embedding 

def get_info(score, sample): 
    score, sample = embedding.get_nearest_examples(
    'Embeddings', sample, k=1
    )
    sample_df = pd.DataFrame.from_dict(sample)
    sample_df['scores'] = score
    sample_df.sort_values('scores', ascending=False, inplace=True)

    for _, row in sample_df.iterrows():
        return {row.Text}