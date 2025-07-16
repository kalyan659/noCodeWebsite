# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 11:00:29 2025

@author: kalyanbrat
"""

import requests
import os
from dotenv import load_dotenv
import streamlit as st

# Load .env only for local development
load_dotenv()

# Check env first, fallback to Streamlit secrets
API_KEY = os.getenv("open_router_llm_api") or st.secrets.get("open_router_llm_api")
if not API_KEY:
    st.error("API key not found! Set it in .env or Streamlit Secrets.")
    st.stop()
else:
    st.error("API key found! ")


# def generate_website(prompt):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json",
#     }
 
#     data = {
#         # qwen/qwen-2.5-coder-32b-instruct:free
#         # deepseek/deepseek-chat-v3-0324:free
#         "model": "qwen/qwen-2.5-coder-32b-instruct:free",
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant for website generation."},
#             {"role": "user", "content": prompt}
#         ]
#     }

#     response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
#     # Parse response correctly
#     response_json = response.json()
#     content = response_json["choices"][0]["message"]["content"]

#     print(content)  # Optional for debugging
#     return content
def generate_website(prompt):
    import requests

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "qwen/qwen-2.5-coder-32b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for website generation."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        st.write("🔄 Sending request to OpenRouter...")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        st.write("🌐 HTTP Status:", response.status_code)
        st.code(response.text)

        response.raise_for_status()
        response_json = response.json()

        content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not content:
            raise ValueError("⚠️ LLM returned no content.")

        return content

    except Exception as e:
        st.error(f"🚨 LLM API error: {e}")
        if API_KEY:
            st.write(API_KEY[:4])
        st.stop()



if __name__ == '__main__':
    prompt =  ''' Output only the full working HTML document including embedded CSS and JavaScript 
    — no explanations, no markdown, just the code. It should be a single-page website with a hero banner, 
    about section, gallery section, and contact form. In about section write 10 lines according to topic
    of prompt. Our Gallery section upto 6 photos.Our phograpgaer section upto 6 photos with photograpger name. Add copyright of year © 2025. '''
                

    generate_website(prompt)





