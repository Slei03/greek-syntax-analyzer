from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import spacy
import base64
from spacy import displacy

app = Flask(__name__)
CORS(app, support_credentials=True)

nlp_models = {
    "grc_proiel_lg": None,
    "grc_proiel_sm": None,
}
config = {"punct_chars": [".", ";", "·"]}
""" nlp = spacy.load("grc_proiel_sm")
nlp.add_pipe("sentencizer", config=config, before="parser")
 """
@app.route('/parse', methods=["POST", "GET"])
def parse():
    model = request.args.get('model')
    text = request.args.get('input')
    if model in nlp_models.keys():
        if nlp_models[model] is None:
            nlp_models[model] = spacy.load(model)
            nlp_models[model].add_pipe("sentencizer", config=config, before="parser")
        
        doc = nlp_models[model](text)
        html = displacy.render(doc, style="dep")
        return get_svg_link(html)
    return ""

def get_svg_link(svg: str):
    """Convert an SVG to a base64-encoded image."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    link = f"data:image/svg+xml;base64,{b64}"
    return jsonify({"link": link})

if __name__ == '__main__':
    app.run(debug=True)