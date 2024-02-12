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

        # Parse entities and create a structured response
        response = {}
        for entity in entities:
            label = entity['label']
            if label == 'FROM':
                response['from'] = text[entity['start']:entity['end']]
            elif label == 'TO':
                response['to'] = text[entity['start']:entity['end']]
            elif label == 'TIME':
                response['time'] = text[entity['start']:entity['end']]
            elif label == 'MODE':
                response['mode'] = text[entity['start']:entity['end']]

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
