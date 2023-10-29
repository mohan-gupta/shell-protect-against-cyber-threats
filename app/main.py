import numpy as np

import torch

from model import RobertaQA, DebertaQA
from config import ROBERTA_TOKENZIER, DEBERTA_TOKENZIER, DEVICE
from predict import predict

roberta = RobertaQA()
roberta.load_state_dict(torch.load("../model/roberta_qa1.bin", map_location=DEVICE))
roberta.to(DEVICE)

deberta = DebertaQA()
deberta.load_state_dict(torch.load("../model/deberta_qa.bin", map_location=DEVICE))
deberta.to(DEVICE)

def get_span(text):
    roberta_preds = predict(roberta, ROBERTA_TOKENZIER, text)
    deberta_preds = predict(deberta, DEBERTA_TOKENZIER, text, token_ids=True)
    
    preds = (roberta_preds["score_span"], deberta_preds["score_span"])
    
    scores = [pred[0] for pred in preds]
    spans = [pred[1] for pred in preds]
    
    span_idx = np.argsort(scores)[::-1][0]
    span = spans[span_idx]
    
    return span

if __name__ == "__main__":
    text = input()
    res = get_span(text)
    print(res)