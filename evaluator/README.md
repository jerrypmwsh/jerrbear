# Random Thought: What if the value for a field in your API needs to be grabbed at request time?

This project roughly sets up a way to do this using jsonpath. 
`main.py` hits canned APIs in `api.py` and tranforms values 
in the response. This idea could be used in the api server
or a client's response.

The `/` endpoint returns a response structure with a `container` field and a
`resolvers` array. 
```json
{
  "container": {
    "params": {
      "global": {
        "assignment": "",
	"reportScore": "",
	"static": "shock",
      }
    }
  },
  "resolvers": [...]
}
```


A `resolver` is a structure describing how to replace a field in the
`container.params` part of the structure.

```jsonc
{
  "target": { // describes the field to replace
   // path starts from `params`. This is an arbitrary decision for the example.
     "query": "$.global.assignment", // json path for the field to replace,
     "type": "string"
  },
  "extract": { // how to get the data
    "type": "http", // the type of resolver
    "method": "GET", // the http verb to use
    "ref": "http://localhost:5000/data", // the url to hit
    "response_type": "json", // the response type
    },
  "transform": { // how to transform the response to the field value
    "type": "json_path", // type of query
    "query": "$.[0].title" // json path for the value
  },
}
```

To run:
1. install [poetry](https://github.com/python-poetry/poetry#installation) and python 3.9.0
1. poetry shell
1. FLASK_APP=api.py flask run &
1. python main.py

You should see:
```
127.0.0.1 - - [28/Oct/2020 20:45:24] "GET / HTTP/1.1" 200 -
response body: {
    "global": {
        "assignment": "",
        "reportScore": "",
        "static": "shock"
    }
}
127.0.0.1 - - [28/Oct/2020 20:45:24] "GET /data HTTP/1.1" 200 -
127.0.0.1 - - [28/Oct/2020 20:45:24] "GET /data HTTP/1.1" 200 -
resolved body: {
    "global": {
        "assignment": "Book report number 1",
        "reportScore": 100,
        "static": "shock"
    }
}
```

To quit:
1. fg
1. ctrl-c
