from google.cloud import language_v1
import os

def analyze_text_with_google_nlp(text):
    """
    Analyze text using Google Natural Language API.
    Returns categories based on entity analysis and sentiment.
    """
    client = language_v1.LanguageServiceClient()

    # Prepare the document
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze entities and sentiment
    response = client.analyze_entities(document=document)
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    entities = []
    for entity in response.entities:
        entities.append({
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience
        })

    return entities, sentiment

def generate_soap(transcript):
    """
    Generate SOAP notes from a transcript using Google NLP.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-key.json"
    subjective = []
    objective = []
    assessment = []
    plan = []

    for segment in transcript:
        speaker = segment["speaker"]
        text = segment["text"]

        entities, sentiment = analyze_text_with_google_nlp(text)

        if speaker.lower() == "patient":
            subjective.append(text)
        elif any(entity['type'] == "NUMBER" for entity in entities):
            objective.append(text)
        elif any("diagnosis" in entity['name'].lower() or "infection" in entity['name'].lower() for entity in entities):
            assessment.append(text)
        elif "recommend" in text.lower() or "prescribe" in text.lower():
            plan.append(text)

    return {
        "subjective": " ".join(subjective) if subjective else "No subjective data recorded.",
        "objective": " ".join(objective) if objective else "No objective data recorded.",
        "assessment": " ".join(assessment) if assessment else "No assessment recorded.",
        "plan": " ".join(plan) if plan else "No plan recorded.",
    }

# Example usage
transcript = [
    {"speaker": "Patient", "text": "I’ve been feeling tired and have had a sore throat."},
    {"speaker": "Doctor", "text": "Do you have any fever or other symptoms?"},
    {"speaker": "Patient", "text": "Yes, I had a slight fever yesterday and some fatigue."},
    {"speaker": "Doctor", "text": "It sounds like a viral infection. Rest and hydrate."}
]

soap_note = generate_soap(transcript)
print(soap_note)
