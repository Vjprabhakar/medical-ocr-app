import google.generativeai as genai
genai.configure(api_key="AIzaSyBif6BQHNGS363jr9krFCvZB21so3n2cEQ")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model found: {m.name}")
except Exception as e:
    print(f"Error: {e}")