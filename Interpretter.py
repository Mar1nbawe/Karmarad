
from transformers import pipeline

def interpretPipeline(sentence):
    pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    return pipe(sentence)

if __name__ == "__main__":
    result = interpretPipeline("Alex is the worst. Really now?")
    print(result)