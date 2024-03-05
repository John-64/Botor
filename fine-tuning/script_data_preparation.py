import pandas as pd
import jsonlines

dataset = pd.read_csv('fine-tuning/medquad.csv')

ds_one_category = dataset.drop_duplicates(subset=['focus_area'])

ds = ds_one_category.drop(columns=['source'])

domanda = "Answer the question that the user provides you and respond in a technical and precise manner to the medical sector"

ds['system'] = domanda

ds_senza_duplicati = ds.drop_duplicates(subset=['question'])

ds = ds_senza_duplicati.dropna()

nuovo_ordine_colonne = ['system', 'question', 'answer']

dataset = ds[nuovo_ordine_colonne]

messages = []

for index, row in dataset.iterrows():
    messages.append({"messages": [{"role": "system", "content": row['system']}, {"role": "user", "content": row['question']}, {"role": "assistant", "content": row['answer']}]})

with jsonlines.open('fine-tuning/medquad_ft.jsonl', mode='w') as writer:
    for message in messages:
        writer.write(message)