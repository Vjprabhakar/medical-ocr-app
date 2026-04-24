import streamlit as st
import pandas as pd
from google import genai
from PIL import Image
import io
import json

# 1. Setup New Client
# The new SDK uses the 'client' pattern
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Medical Register Extractor v2.5", layout="wide")
st.title("📋 Medical Register Data Extractor")
st.write("Using Gemini 2.5 Flash for high-accuracy handwriting extraction.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Register Photo', width=500)
    
    if st.button("Extract Data Dynamically"):
        with st.spinner("Analyzing with Gemini 2.5..."):
            # 2. Define the Prompt
            prompt = """
            Analyze this medical register. Extract the data and return it ONLY as a JSON list of objects.
            Each object must have these keys: 
            "Sl_No", "Name", "Age", "Sex", "Ward", "Unit", "IP_No", "Diagnosis", "Operation", "Surgeon", "Nurses", "Anaesthesiologist", "Anaesthesia_Type", "Duration", "Remarks".

            Rules:
            1. If a cell is empty, use null.
            2. If text spans multiple lines in one cell, combine them into one string.
            3. Ensure "Diagnosis" and "Operation" are clearly separated.
            """
            
            try:
                # 3. Call the New 2.5 Flash Model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt, image]
                )
                
                # Clean the response and parse JSON
                raw_json = response.text.replace("```json", "").replace("```", "").strip()
                data_list = json.loads(raw_json)

                # Convert directly to DataFrame
                df = pd.DataFrame(data_list)
                st.dataframe(df)

                # 5. Excel Export
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                
                st.download_button(
                    label="📥 Download Excel File",
                    data=output.getvalue(),
                    file_name="extracted_medical_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error: {e}")