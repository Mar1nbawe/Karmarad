
import torch
import nltk
import torch_directml
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
from Classes import AI
from Classes.Interpretter_Result import Inter_Result
from Funcs.endpoint_funcs import interpretter_endpoint, Parse_interpretter_name
from System.event_manager import EventManager
from System.karma_calculator import Calculate_Karma
from nltk.sentiment.vader import SentimentIntensityAnalyzer

dml = torch_directml.device()

model_name = "google/flan-t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
model.to("cpu")

def generate_flan_t5_response(prompt: str, max_tokens: int = 512) -> str:

    prompt = """You are a model skilled with summarization.
    change all pronouns like "I", "We", to "They" and change the message accordingly. 
Summarize the following text in a clear, concise paragraph, 
without missing key details.
Make sure the summary is easy enough to understand and isn't overly detailed.  \n
Text:""" + prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    print(prompt)
    # Generate output
    outputs = model.generate(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=max_tokens,
        do_sample=True,            # Optional: for more diverse responses
        top_k=50,                  # Optional: limit sampling to top k tokens
        top_p=0.95,                # Optional: nucleus sampling
        temperature=0.1            # Optional: controls randomness
    )

    # Decode and return the result
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def parse_result_pipeline(prompt):
    inter_result = Inter_Result("", "", )

    try:
        sentiment_result = interpretPipeline(prompt)
        summarize_response = generate_flan_t5_response(prompt)
        inter_result.summarize = summarize_response
        inter_result.sentiment_response = sentiment_result

    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"An error occurred while parsing the result: {e}")

    return inter_result

# def interpretPipeline(sentence):
#     pipe = pipeline("text-classification", model="delarosajav95/tw-roberta-base-sentiment-FT")
#     print(pipe(sentence))
#     return pipe(sentence)

def interpretPipeline(sentence):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(sentence)
    return sentiment['compound']


def run_interpretter(character: AI, event_manager: EventManager):
    while True:
        user_input = input("Enter a sentence to interpret (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        try:

            sentiment = interpretPipeline(user_input)
            result = parse_result_pipeline(user_input)
            print(f"Summarization: {result.summarize}")
            print(f"Sentiment Compound: {result.sentiment_response}")
            sentiment_label = "Positive" if sentiment > 0.05 else "Negative" if sentiment < -0.05 else "Neutral"
            if sentiment >= 0.05 or sentiment <= -0.05:
                karma_result = Calculate_Karma(sentiment, 1)
                character.adjust_karma(karma_result)
                event_manager.gossip(victim=character, karma=karma_result, action=sentiment_label)  # Continue later
        except Exception as e:
            print(f"An error occurred: {e}")


# run_interpretter()