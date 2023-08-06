"""This is a Python-based web server that can be run to
read with Eidos. To run the server, do

    python -m indra.sources.eidos.server

and then submit POST requests to the `localhost:5000/process_text` endpoint
with JSON content as `{'text': 'text to read'}`. The response will be the
Eidos JSON-LD output.
"""

import json
from flask import Flask, request
from indra.sources.eidos.reader import EidosReader


app = Flask(__name__)


@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.json.get('text')
    if not text:
        return {}
    res = er.process_text(text, 'json_ld')
    return json.dumps(res)


if __name__ == '__main__':
    er = EidosReader()
    er.process_text('hello', 'json_ld')
    app.run(host='0.0.0.0')
