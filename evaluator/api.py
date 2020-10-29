from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/data")
def data_response():
    return jsonify([{"title": "Book report number 1", "score": "100"}])


@app.route("/")
def transomer_response():
    URL = "http://localhost:5000/data"
    return {
        "container": {
            "params": {
                "global": {
                    "assignment": "",
                    "reportScore": "",
                    "static": "shock",
                }
            }
        },
        "resolvers": [
            {
                "target": {
                    # path starts from params.
                    "query": "$.global.assignment",
                    "type": "string"
                },
                "extract": {
                    "type": "http",
                    "method": "GET",
                    "ref": URL,
                    "response_type": "json",
                },
                "transform": {
                    "type": "json_path",
                    "query": "$.[0].title"
                },
            },
            {
                "target": {"query": "$.global.reportScore", "type": "integer"},
                "extract": {
                    "type": "http",
                    "method": "GET",
                    "ref": URL,
                    "response_type": "json",
                },
                "transform": {
                    "type": "json_path",
                    "query": "$.[0].score",
                },
            },
        ],
    }
