import torch.nn as nn

from transformers import AutoConfig, RobertaModel, DebertaV2Model

from config import ROBERTA_MODEL, DEBERTA_MODEL

class RobertaQA(nn.Module):
    def __init__(self, ):
        super().__init__()
        self.roberta_config = AutoConfig.from_pretrained(ROBERTA_MODEL, add_pooling_layer=False)
        self.roberta = RobertaModel(self.roberta_config, add_pooling_layer=False)
        self.dropout = nn.Dropout(0.2)
        self.linear = nn.Linear(768, 2)

    def forward(self, input_ids, attention_mask):
        outputs = self.roberta(input_ids, attention_mask)

        #(batch_size, num_tokens, embedding_size)
        hn = outputs['last_hidden_state']
        drop_hn = self.dropout(hn)

        #(batch_size, num_tokens, 256)
        logits = self.linear(drop_hn)

        start_logits, end_logits = logits.split(1, dim = -1)
        start_logits, end_logits = start_logits.squeeze(-1), end_logits.squeeze(-1)

        return start_logits, end_logits
    

class DebertaQA(nn.Module):
    def __init__(self, ):
        super().__init__()
        self.deberta_config = AutoConfig.from_pretrained(DEBERTA_MODEL)
        self.deberta = DebertaV2Model(self.deberta_config)
        self.dropout = nn.Dropout(0.2)
        self.linear = nn.Linear(1024, 2)

    def forward(self, input_ids, attention_mask, token_type_ids):
        outputs = self.deberta(input_ids, attention_mask, token_type_ids)

        #(batch_size, num_tokens, embedding_size)
        hn = outputs['last_hidden_state']
        drop_hn = self.dropout(hn)

        #(batch_size, num_tokens, 256)
        logits = self.linear(drop_hn)

        start_logits, end_logits = logits.split(1, dim = -1)
        start_logits, end_logits = start_logits.squeeze(-1), end_logits.squeeze(-1)

        return start_logits, end_logits