import os
import google.generativeai as genaai

genaai.configure(api_key="AIzaSyDq3YUodqagvhTNFGpTVVxHVWeqioRRW90")

for model in genaai.list_models():
    print(model.name, model.supported_generation_methods)
