from tqdm import tqdm
import numpy as np

import torch

from config import DEVICE, MAX_LENGTH, STRIDE

# first the get the logits
def get_logits(model, tokenizer, text, token_ids=False):
    #tokenizer input data
    input_toks = tokenizer(
        text,
        padding=True,
        truncation="only_first",
        max_length=MAX_LENGTH,
        stride=STRIDE,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,
        return_tensors='pt'
        )

    offsets = input_toks['offset_mapping']
    sample_map = input_toks["overflow_to_sample_mapping"]

    with torch.no_grad():
        #get the logits
        if token_ids:    
            start_logits, end_logits = model(
                input_toks['input_ids'].to(DEVICE),
                input_toks['attention_mask'].to(DEVICE),
                input_toks['token_type_ids'].to(DEVICE)
                )
        else:
            start_logits, end_logits = model(
                input_toks['input_ids'].to(DEVICE),
                input_toks['attention_mask'].to(DEVICE)
                )

        #converting to numpy arrays
        start_logits, end_logits = start_logits.cpu().numpy(), end_logits.cpu().numpy()
      
    return {
        "offset_mapping": offsets,
        "sample_mapping": sample_map,
        "start_logits": start_logits,
        "end_logits": end_logits
    }
    
def get_best_answer(start_logit, end_logit, offset, context, n_best=20):
    #get the top n_best logit indexes for a chunk
    start_idxs = np.argsort(start_logit)[-1:n_best-1:-1]
    end_idxs = np.argsort(end_logit)[-1:n_best-1:-1]

    best_answer = (0.0, "")
    #try all valid combinantions of start and end
    for start_idx in start_idxs:
        if start_idx<0 or offset[start_idx] is None:
            continue
        for end_idx in end_idxs:
            if start_idx>end_idx  or end_idx>len(offset) or offset[end_idx] is None:
                continue

            score = start_logit[start_idx] + end_logit[end_idx]
            start_char, end_char = offset[start_idx][0], offset[end_idx][1]
            span = context[start_char:end_char]

            if best_answer[0]<=score:
                best_answer = (score, span)
                
    return best_answer

def predict(model, tokenizer, text, token_ids=False, n_best=5):
    model.eval()

    pred_data = get_logits(model, tokenizer, text, token_ids)
    
    offsets = pred_data['offset_mapping']
    
    start_logits = pred_data["start_logits"]
    end_logits = pred_data["end_logits"]

    best_answer = (0, "")
    for idx, offset in tqdm(enumerate(offsets), total=len(offsets)):
        pred = get_best_answer(
            start_logit = start_logits[idx], 
            end_logit = end_logits[idx],
            offset = offset,
            context = text,
            n_best = n_best
            )

        #for an example, we will store the answer with max score from all its chunks. 
        if pred[0]>best_answer[0]:
            best_answer = pred

    return {"score_span":np.array(best_answer)}
