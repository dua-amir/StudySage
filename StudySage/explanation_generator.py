import wikipedia

def generate_explanation(topic):
    try:
        summary = wikipedia.summary(topic, sentences=3)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"This topic is broad. Try being more specific: {', '.join(e.options[:5])}"
    except Exception as e:
        return "Sorry, I couldn't fetch a detailed explanation. Try rephrasing." 