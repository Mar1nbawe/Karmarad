
import torch
import torch_directml
from transformers import pipeline

from Classes.Interpretter_Result import Inter_Result
from Funcs.endpoint_funcs import interpretter_endpoint, Parse_interpretter_name
from System.event_manager import EventManager
from System.karma_calculator import Calculate_Karma

dml = torch_directml.device()

def parse_result_pipeline(prompt):
    inter_result = Inter_Result("", "", "", "")

    result = interpretPipeline(prompt)
    name_track = interpretter_endpoint(prompt)
    res = Parse_interpretter_name(name_track)
    inter_result.name = res.name
    inter_result.sentiment_severity = res.sentiment_severity
    inter_result.action = res.action
    inter_result.sentiment_response = result[0]['label']

    return inter_result

def interpretPipeline(sentence):
    pipe = pipeline("text-classification", model="delarosajav95/tw-roberta-base-sentiment-FT")
    print(pipe(sentence))
    return pipe(sentence)



label_mapping = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
while True:

    msg = input("Insert Message")
    a = parse_result_pipeline(msg)
    print(a.sentiment_response)
    print(a.name[0])
    print(a.action)
    print(a.sentiment_severity[0])
    # print(Calculate_Karma(a.sentiment_score, 8))


# print(a.sentiment_score)
# print(Calculate_Karma(a.sentiment_score, 8))