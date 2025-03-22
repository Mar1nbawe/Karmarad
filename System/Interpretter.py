
import torch
import torch_directml
from transformers import pipeline

from Classes.Interpretter_Result import Inter_Result
from Funcs.endpoint_funcs import interpretter_endpoint, Parse_interpretter_name

dml = torch_directml.device()

def parse_result_pipeline(prompt):
    inter_result = Inter_Result("", "", 0)

    result = interpretPipeline(prompt)
    name_track = interpretter_endpoint(prompt)

    inter_result.name = Parse_interpretter_name(name_track)
    inter_result.sentiment_score = result[0]['score']
    inter_result.sentiment_response = result[0]['label']

    return inter_result

def interpretPipeline(sentence):
    pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    return pipe(sentence)

