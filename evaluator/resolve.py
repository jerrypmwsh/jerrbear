from jsonpath_ng import parse
import requests
import json


SCALAR_TARGET_TYPES = {'string': str, 'integer': int, 'float': float}

def resolve(dynamic_value, target_type: str):
    extract = dynamic_value["extract"]
    if extract["type"] == "http":
        r: requests.Response = requests.request(extract["method"], extract["ref"])
        body = r.json() if extract["response_type"] == "json" else r.text()
    transform = dynamic_value["transform"]
    if transform["type"] == "json_path":
        jsonpath_expr = parse(transform["query"])
        matches = [match.value for match in jsonpath_expr.find(body)]
        if not matches:
            raise RuntimeError("Error tranforming to correct target type")
        if len(matches) > 1 and target_type in SCALAR_TARGET_TYPES:
            raise RuntimeError("Error, cannot have multiple matches for a scalar type")
        else:
            return SCALAR_TARGET_TYPES[target_type](matches[0])


if __name__ == "__main__":
    URL = "https://ghibliapi.herokuapp.com/films"
    evaluate = {
    "extract": {"type": "http", "method": "GET", "ref": URL, "response_type": "json"},
    "transform": {
        "type": "json_path",
        "query": "$.[0].title",
    },
    }   
    print(resolve(evaluate, "string"))
    evaluate = {
        "extract": {"type": "http", "method": "GET", "ref": URL, "response_type": "json"},
        "transform": {
        "type": "json_path",
        "query": "$.[0].rt_score",
        },
    } 
    print(resolve(evaluate, "integer"))
    
