from dotenv import load_dotenv
import os
from groq import Groq
import streamlit as st

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if api_key is None:
    api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

def generate_recommendations(destination,tci,temperature,humidity,precipitation,temp_z,rh_z,precip_z):


    prompt = f"""
You are a tourism climate advisor.

Based on the following location and climate information, generate exactly THREE practical recommendations for tourists.

Climate Information:
Destination: {destination}
Tourism Climate Index (TCI): {tci}
Temperature: {temperature} °C
Humidity: {humidity} %
Rainfall: {precipitation} mm

Temperature Z-Score: {temp_z}
Humidity Z-Score: {rh_z}
Rainfall Z-Score: {precip_z}

Rules:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT explain anything.
- Each recommendation should be one short sentence.
- Maximum 20 words per recommendation.

Return exactly this format:

{{
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user","content": prompt}],
        temperature=0.4
    )

    try:
        result = json.loads(response.choices[0].message.content)
        return result["recommendations"]
    except Exception:
        return [
            "Unable to generate recommendations at the moment.",
            "Please try again later.",
            "Check the weather information for manual planning."
        ]

