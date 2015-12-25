from data_model import *
from rest_handler import *

API_KEY = "52fceca74b13b0ce744e0afa1f6bef177b32fd3a"

if __name__ == "__main__" :
    req = Request(API_KEY, "TCS")
    req.request()
    c = 1
