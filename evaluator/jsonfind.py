from typing import Any
from jsonpath_ng import parse



def find_and_modify(jsonpath: str, struct: dict, value: Any):
    jsonpath_expr = parse(jsonpath)
    jsonpath_expr.update(struct, value)

if __name__ == "__main__":
    struct = {'foo': 'a'}
    print(struct)
    find_and_modify("$.foo", struct, 'b')
    print(struct)

