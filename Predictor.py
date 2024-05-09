import torch
import pandas as pd

class Predictor():
    def __init__(self, df_source, target=str):  #binary file  #target to func itself #init ONLY ONCE
        self.df_source=df_source
        self.target=target
        self.model=None
        self.tokenizer=None    
        
    def load_model(self):
        import torch
        from transformers import AutoTokenizer, AutoModel
        tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2") #replace with my finetuned model
        model = AutoModel.from_pretrained("cointegrated/rubert-tiny2")         #replace here too
        self.model=model
        self.tokenizer=tokenizer
        
    def embed_bert_cls(self, text):
        t = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**{k: v.to(self.model.device) for k, v in t.items()})
        embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings)
        target_embeds = embeddings[0].cpu().numpy()    
        return target_embeds    
          
    def find_matches(self, n_neighbours=1):
        import numpy as np
        self.load_model()
        target=self.embed_bert_cls(text=self.target)
        self.df_source['embeddings']=self.df_source.vector.apply(lambda x: self.embed_bert_cls(text=x))
        samples=self.df_source['embeddings'].tolist()
        # print(samples)
        from sklearn.neighbors import NearestNeighbors
        neigh = NearestNeighbors(n_neighbors=n_neighbours)
        neigh.fit(samples)
        print(neigh.kneighbors([target]))
        indexes=neigh.kneighbors([target])[1][0]
        distance=neigh.kneighbors([target])[0][0]
        res=self.df_source.iloc[indexes]['vector']
        return indexes, res, distance
    

# df_mts=pd.read_csv('venues_mts.csv', index_col='Unnamed: 0').dropna()
# df_approved=pd.read_csv('df_orgs.csv')    
# predictor_instance=Predictor(df_mts, 'Театр «Практика» г. Москва, переулок Большой Козихинский, дом 30')
# print(predictor_instance.find_matches())