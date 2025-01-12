import torch
import torch_directml
from transformers import BertTokenizer, AutoModelForSequenceClassification, AutoTokenizer, BertForMaskedLM,  AutoModelForTokenClassification

# Initialize DirectML device
dml = torch_directml.device()


classification_tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
classification_model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

# Load the sentiment analysis model and tokenizer
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
try:
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_tokenizer = AutoTokenizer.from_pretrained(model_name)
except OSError as e:
    print(f"Error loading sentiment model: {e}")
    exit(1)

# Load the BERT base model and tokenizer
model_name = "bert-base-uncased"
try:
    bert_tokenizer = BertTokenizer.from_pretrained(model_name)
    bert_model = BertForMaskedLM.from_pretrained(model_name)
except OSError as e:
    print(f"Error loading model: {e}")
    exit(1)

# Move the models to the DirectML device
sentiment_model.to(dml)
bert_model.to(dml)
classification_model.to(dml)

# Initialize entities and previous inputs
entities = {}
previous_inputs = []

while True:
    user_input = input("Continue the conversation. Type 'exit' to quit: ")
    if user_input.lower() == "exit":
        break

    # Perform NER
    classification_input = classification_tokenizer(user_input, return_tensors="pt")
    classification_input = {key: value.to(dml) for key, value in classification_input.items()}
    with torch.no_grad():
        classification_outputs = classification_model(**classification_input)

    tokens = classification_outputs.convert_ids_to_tokens(classification_input['input_ids'][0])
    predictions = classification_outputs.logits.argmax(-1).squeeze().tolist()
    for token, prediction in zip(tokens, predictions):
        if classification_model.config.id2label[prediction] != "O":
            label = classification_model.config.id2label[prediction]
            if label == "B-LOC" or label == "I-PER":
                entities[token] = token
                print(f"Entity: {token}")

    previous_inputs.append(user_input)
    context = " ".join(previous_inputs[-5:])
    masked_context = context + " The person I am talking about is [MASK]."

    # Tokenize the input text and move to DirectML device for sentiment analysis
    sentiment_inputs = sentiment_tokenizer(user_input, return_tensors="pt")
    sentiment_inputs = {key: value.to(dml) for key, value in sentiment_inputs.items()}

    with torch.no_grad():
        sentiment_outputs = sentiment_model(**sentiment_inputs)

    sentiment_scores = sentiment_outputs.logits.softmax(dim=-1)
    sentiment = torch.argmax(sentiment_scores, dim=1).item()
    sentiment_labels = ['negative', 'neutral', 'positive']

    print(f"The sentiment of the text is {sentiment_labels[sentiment]}")

    # Tokenize the input text and move to DirectML device for BERT
    bert_inputs = bert_tokenizer(masked_context, return_tensors="pt")
    bert_inputs = {key: value.to(dml) for key, value in bert_inputs.items()}

    with torch.no_grad():
        bert_outputs = bert_model(**bert_inputs)

    # Process NER results
    mask_token_index = (bert_inputs['input_ids'] == bert_tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
    predicted_index = torch.argmax(bert_outputs.logits[0, mask_token_index], dim=-1)
    predicted_token = bert_tokenizer.convert_ids_to_tokens(predicted_index.item())

    print(f"Predicted token for [MASK]: {predicted_token}")

    for i, score in enumerate(sentiment_scores[0]):
        print(f"{sentiment_labels[i]}: {score.item() * 100:.2f}%")