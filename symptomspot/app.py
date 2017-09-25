from flask import request, Flask, jsonify

from symptomspot.extractor import SymptomExtractor

app = Flask(__name__)

extractor = SymptomExtractor()


@app.route('/symptomspot/text', methods=['POST'])
def parse_text():
    text = request.form['text']
    symptoms = extractor.extract(text=text)
    resp = jsonify(symptoms)
    resp.status_code = 200

    return resp


@app.route('/symptomspot/url', methods=['POST'])
def parse_url():
    url = request.form['url']
    symptoms = extractor.extract(url=url)
    resp = jsonify(symptoms)
    resp.status_code = 200

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')
