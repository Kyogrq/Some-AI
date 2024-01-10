import spacy
from spacy.matcher import Matcher

def complex_chatbot():
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    # Define patterns for specific topics
    patterns = [
        [{"LOWER": "python"}],
        [{"LOWER": "machine"}, {"LOWER": "learning"}],
        [{"LOWER": "data"}, {"LOWER": "science"}]
    ]

    matcher.add("Topic", patterns)

    knowledge_base = {
        "python": "Python is a high-level programming language known for its readability and versatility.",
        "machine learning": "Machine learning is a subset of artificial intelligence that focuses on building models that can learn from data.",
        "data science": "Data science involves extracting insights and knowledge from structured and unstructured data."
    }

    print("Hello! I'm your advanced chatbot. Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye! Have a great day.")
            break

        # Process user input
        user_doc = nlp(user_input)

        # Check for specific topics
        matches = matcher(user_doc)
        if matches:
            response = generate_topic_response(matches, user_doc)
        else:
            response = generate_default_response(user_doc, knowledge_base)

        print("Bot:", response)

def generate_topic_response(matches, user_doc):
    # Respond based on detected topic
    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "Topic":
            topic = user_doc[start:end].text.lower()
            return f"{knowledge_base.get(topic, 'I have limited knowledge on that')} Anything else you'd like to know?"

    return "I'm not sure what you're referring to. Can you provide more details?"

def generate_default_response(user_doc, knowledge_base):
    # Generate a response based on general understanding
    intents = get_intents(user_doc)
    
    if "greeting" in intents:
        return "Hello! How can I assist you today?"

    return "I'm just a simple chatbot. How can I help you?"

def get_intents(doc):
    # Identify user intents based on key verbs
    intents = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    return intents

# Run the chatbot
complex_chatbot()
