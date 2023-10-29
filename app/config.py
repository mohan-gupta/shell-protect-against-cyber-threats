import torch

from transformers import AutoTokenizer

DIR = "/content/drive/MyDrive/code_cyber_sec/"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

ROBERTA_MODEL = "deepset/roberta-base-squad2-distilled"
DEBERTA_MODEL = "deepset/deberta-v3-large-squad2"

MAX_LENGTH = 256
STRIDE = 15

ROBERTA_TOKENZIER = AutoTokenizer.from_pretrained(ROBERTA_MODEL)
DEBERTA_TOKENZIER = AutoTokenizer.from_pretrained(DEBERTA_MODEL)