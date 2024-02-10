from flask import Flask, request, jsonify

app = Flask(__name__)

# Your spaCy model loading code
import spacy
nlp = spacy.load("model-best")

@app.route('/api/annotate', methods=['POST'])
def annotate_text():
    try:
        data = request.json
        text = data['text']

        # Process the text with the spaCy model
        doc = nlp(text)

        # Extract relevant information from the spaCy Doc object
        entities = [{'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_}
                    for ent in doc.ents]

        # Parse entities and create a structured response with lists
        response = {'mode': [], 'location': [], 'time': []}
        for entity in entities:
            label = entity['label']
            if label == 'MODE':
                response['mode'].append(text[entity['start']:entity['end']])
            elif label == 'LOCATION':
                response['location'].append(text[entity['start']:entity['end']])
            elif label == 'TIME':
                response['time'].append(text[entity['start']:entity['end']])

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
