import json
import rdp_parser
from tok import *

def cmp_json(a,b):
    return a == json.loads(b)
