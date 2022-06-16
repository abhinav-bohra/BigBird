import torch
from torch import nn
from torch.nn import init

from transformers import BertModel, RobertaModel

class MatchSum(nn.Module):
    
    def __init__(self, candidate_num, encoder, hidden_size=768):
        super(MatchSum, self).__init__()
        
        self.hidden_size = hidden_size
        self.candidate_num  = candidate_num
        
        if encoder == 'bert':
            self.encoder = BertModel.from_pretrained('bert-base-uncased')
        else:
            self.encoder = RobertaModel.from_pretrained('roberta-base')

    def forward(self, text_id, candidate_id, summary_id):
        #text_id is chunked --> [bs, n_chunks, max_len] --> [1, 8, 512]
        batch_size = text_id.size(0)
        chunk_size = text_id.size(1)
        
        pad_id = 0     # for BERT
        if text_id[0][0][0] == 0:
            pad_id = 1 # for RoBERTa

        # get document embedding
        outs_list = []
        #Get BERT encoded representations of every chunk
        for i in range(chunk_size):
            chunk_id = text_id[:,i,:]
            input_mask = ~(chunk_id == pad_id)
            outs_list.append(self.encoder(chunk_id, attention_mask=input_mask)[0].squeeze(0)) # last layer
        
        out = torch.stack(outs_list).unsqueeze(0)
        
        #take [cls] token embedding
        doc_emb = out[:, :, 0, :]
        assert doc_emb.size() == (batch_size, chunk_size, self.hidden_size) # [batch_size, hidden_size]
        
        # print("doc_out:", out.shape)
        # print("doc_emb:", doc_emb.shape)

        # get summary embedding
        input_mask = ~(summary_id == pad_id)
        out = self.encoder(summary_id, attention_mask=input_mask)[0] # last layer
        summary_emb = out[:, 0, :]
        assert summary_emb.size() == (batch_size, self.hidden_size) # [batch_size, hidden_size]

        # print("sum_input_mask:", input_mask.shape)
        # print("sum_out:", out.shape)
        # print("sum_emb:", summary_emb.shape)

        # get summary score
        summary_score = torch.cosine_similarity(summary_emb, doc_emb, dim=-1)
        summary_score = summary_score.mean()
    
        # get candidate embedding
        candidate_num = candidate_id.size(1)
        candidate_id = candidate_id.view(-1, candidate_id.size(-1))
        input_mask = ~(candidate_id == pad_id)
        out = self.encoder(candidate_id, attention_mask=input_mask)[0]
        candidate_emb = out[:, 0, :].view(batch_size, candidate_num, self.hidden_size)  # [batch_size, candidate_num, hidden_size]
        assert candidate_emb.size() == (batch_size, candidate_num, self.hidden_size)
        
        # print("can_input_mask:", input_mask.shape)
        # print("can_out:", out.shape)
        # print("can_emb:", candidate_emb.shape)
        # print("candidate_num:", candidate_num)

        # get candidate score
        scores_list = []
        for i in range(chunk_size):              
            chunk_doc_emb = doc_emb[:,i,:].unsqueeze(1)
            # print("chunk_doc_emb:", chunk_doc_emb.shape)
            chunk_doc_emb=chunk_doc_emb.expand_as(candidate_emb)
            # print("chunk_doc_emb:", chunk_doc_emb.shape)
            sc = torch.cosine_similarity(candidate_emb, chunk_doc_emb, dim=-1) # [batch_size, candidate_num]
            assert sc.size() == (batch_size, candidate_num)
            scores_list.append(sc.squeeze(0)) 

        score_all = torch.stack(scores_list).unsqueeze(0)
        score = torch.mean(score_all, dim=1)
        
        # print("score:", score_all.shape)
        # print("score:", score.shape)

        return {'score': score, 'summary_score': summary_score}

