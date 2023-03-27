import json
def ty(**kwargs):
    return kwargs

def dp(*args, **kwrgs):
    if not args:
        args = ({})
    return json.dumps(args[0] | kwrgs)

def dp_print(*args, **kwrgs):
    if not args:
        args = ({})
    a = json.dumps(args[0] | kwrgs, indent=4)
    print(a)
    return a