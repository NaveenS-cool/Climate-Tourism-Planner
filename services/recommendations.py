from dotenv import load_dotenv
import os
import json
from groq import Groq
import streamlit as st

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception:
        pass

@st.cache_data(show_spinner=False)
def generate_recommendations(destination,tci,temperature,humidity,precipitation,temp_z,rh_z,precip_z):
    if client is None:
        return [
            "Unable to generate recommendations at the moment.",
            "Please try again later.",
            "Check the weather information for manual planning."
        ]

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

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user","content": prompt}],
            temperature=0.4
        )
        content = response.choices[0].message.content.strip()
        
        # Remove any leading/trailing markdown code block ticks if LLM returned them
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
            
        if content.endswith("```"):
            content = content[:-3]
            
        content = content.strip()
        result = json.loads(content)
        return result["recommendations"]
    except Exception:
        return [
            "Unable to generate recommendations at the moment.",
            "Please try again later.",
            "Check the weather information for manual planning."
        ]

