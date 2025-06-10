# test_models.py

import google.generativeai as genai

# Substitua pela sua chave real
genai.configure(api_key="GEMINI_API_KEY")

models = genai.list_models()

print("Modelos disponíveis:")
for model in models:
    print("-", model.name)
