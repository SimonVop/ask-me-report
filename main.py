import streamlit as st
from Authent import * 
from Extraction import Extract
from tempfile import NamedTemporaryFile
from Embedding import *
import json 

try: 

    st.set_page_config(page_title="Ask Me Reports", page_icon="💡", layout="wide")   

    col1a, col2a, col3a = st.columns([2,3,2])

    uploaded_file = st.file_uploader("Please upload File", type='PDF')

 
    
    if uploaded_file is not None:
        # Speichere die Datei temporär
        tempfile_path = f"temp_{uploaded_file.name}"
        with open(tempfile_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    load_data = open("embedded.json")
    embedds_load = json.load(load_data)  
    print(embedds_load['Report'][0])
    if tempfile_path == embedds_load['Report'][0]:       
        embeddings_dataset = Dataset.from_dict(embedds_load)
        embeddings_dataset.add_faiss_index('Embeddings')
        question = st.text_input('Please enter your question here:',key=1)
        question_embedding = get_embedding([question]).cpu().detach().numpy()
        score, sample = embeddings_dataset.get_nearest_examples('Embeddings', question_embedding, k=1)

        sample_df = pd.DataFrame.from_dict(sample)
        sample_df['scores'] = score
        sample_df.sort_values('scores', ascending=False, inplace=True)

        for _, row in sample_df.iterrows():
            answer = (f"{row.Text}")
        if question:
        # question_embeddings = create_question_embeddings(question)
        # answer = get_info(question_embeddings, index)
            st.write(answer)
        
    else:
        extraction = Extract(tempfile_path)
        dictonary = extraction.get_text()
        text_dataset = Dataset.from_dict(dictonary)
        index = get_embedding(text_dataset['Text'][0])   

        def cls_pooling(model_output):
            return model_output.last_hidden_state[:,0]

        def get_embedding(text_list):
            encoded_input = tokenizer(text_list, padding = True, truncation = True, return_tensors ="pt")
            encoded_input = {k: v for k,v in encoded_input.items()}
            model_output = model(**encoded_input)
            return cls_pooling(model_output)
        

        embedding_dataset = text_dataset.map(
        lambda x: {"Embeddings": get_embedding(x['Text']).detach().cpu().numpy()[0]}
        ) 
        embedding_dataset.add_faiss_index(column='Embeddings')
        with open ("embedded.json", "w") as data: 
            json.dump({
                "Embeddings": embedding_dataset['Embeddings'],
                "Pages" : embedding_dataset['Page'],
                "Report" : embedding_dataset['Report'],
                "Text" : embedding_dataset['Text']}, data)
        
        question = st.text_input('Please enter your question here:', key = 2)
        st.write(':green[Report ready]')

        question_embedding = get_embedding([question]).cpu().detach().numpy()
        score, sample = embedding_dataset.get_nearest_examples('Embeddings', question_embedding, k=1)

        sample_df = pd.DataFrame.from_dict(sample)
        sample_df['scores'] = score
        sample_df.sort_values('scores', ascending=False, inplace=True)

        for _, row in sample_df.iterrows():
            answer = (f"{row.Text}")

        if question:
            # question_embeddings = create_question_embeddings(question)
            # answer = get_info(question_embeddings, index)
            st.write(answer)

except Exception as e:
    st.error(f"An error occured :{e}")

