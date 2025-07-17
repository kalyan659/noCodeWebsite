# # -*- coding: utf-8 -*-
# """
# Created on Tue Jul 15 23:01:36 2025

# @author: kalya
# """
#---------------------------local streamlit works------------------------------------
# import streamlit as st
# import os
# import uuid
# import requests
# import subprocess
# from dotenv import load_dotenv
# from generator import call_ollama, save_code
# from llm_openrouter import generate_website
# from shutil import which

# # === Streamlit UI ===
# st.set_page_config(page_title="LLM Website Generator", layout="wide")
# st.title("🧠 LLM Website Generator and Deployer")
# # === Load .env Variables ===
# load_dotenv()

# # === Constants ===
# NETLIFY_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN") or st.secrets.get("NETLIFY_AUTH_TOKEN")

# DEPLOY_DIR_LOCAL = os.path.abspath("static/output-site")
# #NPX_PATH = r"D:\Program Files\npx.CMD"  # Adjust if on Linux/macOS
# NPX_PATH = which("npx")
# #print("npx path:", npx_path)



# prompt = st.text_area("Enter your prompt", height=200)

# custom_name = st.text_input("Custom site name (optional, lowercase, no spaces):")

# if st.button("Generate Website"):
#     if not prompt:
#         st.warning("Please enter a prompt.")
#     else:
#         full_prompt = prompt + '''
#         Output only the full working HTML document including embedded CSS and JavaScript — no explanations, 
#         no markdown, just the code. It should be a single-page website with a hero banner, about section, 
#         gallery section, and contact form. In about section write 10 lines according to topic of prompt. 
#         Our Gallery section upto 6 photos. Our photographer section up to 6 photos with photographer name. 
#         Add copyright of year © 2025.
#         '''
#         try:
#             with st.spinner("Generating website from LLM..."):
#                 result = generate_website(full_prompt)
#                 save_code(result)

#             st.success("✅ Website code generated and saved!")

#             html_file = os.path.join(DEPLOY_DIR_LOCAL, "index.html")
#         except Exception as e:
#             st.error("Failed to load generated HTML."+ str(e))
#         if os.path.exists(html_file):
#             st.markdown("### 🔍 Preview")
#             with open(html_file, "r", encoding="utf-8") as f:
#                 st.components.v1.html(f.read(), height=700, scrolling=True)
#         else:
#             st.error("Failed to load generated HTML.")

# # === Deployment Section ===
# if st.button("🚀 Deploy to Netlify"):
#     def create_site_with_name(name):
#         response = requests.post(
#             "https://api.netlify.com/api/v1/sites",
#             headers={
#                 "Authorization": f"Bearer {NETLIFY_TOKEN}",
#                 "Content-Type": "application/json"
#             },
#             json={"name": name}
#         )
#         if response.status_code in [200, 201]:
#             return response.json()
#         elif response.status_code == 422:
#             return None
#         else:
#             raise Exception(response.text)

#     def generate_fallback_name(base_name):
#         suffix = uuid.uuid4().hex[:6]
#         return f"{base_name}-{suffix}"

#     def link_folder_to_netlify(site_id):
#         import traceback

#         with open("netlify_debug.log", "a") as log:
#             log.write(f"Linking site ID: {site_id}\n")
#             log.write(f"Deploy folder: {DEPLOY_DIR_LOCAL}\n")
#             log.write(f"Using NPX_PATH: {NPX_PATH}\n")

#         try:
#             result = subprocess.run(
#                 [NPX_PATH, 'netlify', 'link', '--id', site_id],
#                 cwd=DEPLOY_DIR_LOCAL,
#                 check=True,
#                 capture_output=True,
#                 text=True
#             )

#             with open("netlify_debug.log", "a") as log:
#                 log.write("Link stdout:\n" + result.stdout + "\n")
#                 log.write("Link stderr:\n" + result.stderr + "\n")

#             stdout_lower = result.stdout.lower()
#             return ("linked" in stdout_lower) or ("already linked" in stdout_lower)

#         except subprocess.CalledProcessError as e:
#             with open("netlify_debug.log", "a") as log:
#                 log.write("CalledProcessError:\n")
#                 log.write(e.stdout or "")
#                 log.write(e.stderr or "")
#                 log.write(traceback.format_exc())
#                 log.write("\n")
#             return False

#         except Exception as e:
#             with open("netlify_debug.log", "a") as log:
#                 log.write("Exception:\n" + traceback.format_exc() + "\n")
#             return False


#     def deploy_to_netlify(site_id):
#         import traceback

#         try:
#             result = subprocess.run(
#                 [NPX_PATH, 'netlify', 'deploy', '--dir', DEPLOY_DIR_LOCAL, '--prod', '--site', site_id],
#                 check=True,
#                 capture_output=True,
#                 text=True
#             )
#             with open("netlify_debug.log", "a") as log:
#                 log.write("Deploy stdout:\n" + result.stdout + "\n")
#                 log.write("Deploy stderr:\n" + result.stderr + "\n")

#             return result.stdout

#         except subprocess.CalledProcessError as e:
#             with open("netlify_debug.log", "a") as log:
#                 log.write("Deploy CalledProcessError:\n")
#                 log.write(e.stdout or "")
#                 log.write(e.stderr or "")
#                 log.write(traceback.format_exc())
#                 log.write("\n")
#             raise e

#         except Exception as e:
#             with open("netlify_debug.log", "a") as log:
#                 log.write("Deploy Exception:\n" + traceback.format_exc() + "\n")
#             raise e


#     try:
#         with st.spinner("Deploying..."):
#             if custom_name:
#                 site = create_site_with_name(custom_name)
#                 if not site:
#                     fallback_name = generate_fallback_name(custom_name)
#                     st.info(f"Custom name taken. Using fallback: `{fallback_name}`")
#                     site = create_site_with_name(fallback_name)
#             else:
#                 site = {
#                     "id": "ae97f241-1b9a-4d19-8314-f4c838eff87c",
#                     "url": "https://kalyanwebsite.netlify.app"
#                 }

#             site_id = site["id"]
#             url = site["url"]

#             if not link_folder_to_netlify(site_id):
#                 st.error("Failed to link folder to Netlify.")
#             else:
#                 output = deploy_to_netlify(site_id)
#                 st.success("✅ Deployed!")
#                 st.markdown(f"[🌍 View your website here]({url})", unsafe_allow_html=True)

#     except Exception as e:
#         st.error(f"❌ Deployment failed: {e}")

#=========================== cloud streamlit works ===================================
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 23:01:36 2025

@author: kalya
"""

import streamlit as st
import os
import uuid
import requests
import subprocess
from dotenv import load_dotenv
from generator import call_ollama, save_code
from llm_openrouter import generate_website
from shutil import which

# === Streamlit UI ===
st.set_page_config(page_title="LLM Website Generator", layout="wide")
st.title("🧠 LLM Website Generator and Deployer")
# === Load .env Variables ===
load_dotenv()

# === Constants ===
NETLIFY_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN") or st.secrets.get("NETLIFY_AUTH_TOKEN")

DEPLOY_DIR_LOCAL = os.path.abspath("static/output-site")
#NPX_PATH = r"D:\Program Files\npx.CMD"  # Adjust if on Linux/macOS
NPX_PATH = which("npx")
#print("npx path:", npx_path)



prompt = st.text_area("Enter your prompt", height=200)

custom_name = st.text_input("Custom site name (optional, lowercase, no spaces):")

if st.button("Generate Website"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        full_prompt = prompt + '''
        Output only the full working HTML document including embedded CSS and JavaScript — no explanations, 
        no markdown, just the code. It should be a single-page website with a hero banner, about section, 
        gallery section, and contact form. In about section write 10 lines according to topic of prompt. 
        Our Gallery section upto 6 photos. Our photographer section up to 6 photos with photographer name. 
        Add copyright of year © 2025.
        '''
        try:
            with st.spinner("Generating website from LLM..."):
                result = generate_website(full_prompt)
                save_code(result)

            st.success("✅ Website code generated and saved!")

            html_file = os.path.join(DEPLOY_DIR_LOCAL, "index.html")
        except Exception as e:
            st.error("Failed to load generated HTML."+ str(e))
        if os.path.exists(html_file):
            st.markdown("### 🔍 Preview")
            with open(html_file, "r", encoding="utf-8") as f:
                st.components.v1.html(f.read(), height=700, scrolling=True)
        else:
            st.error("Failed to load generated HTML.")

# === Deployment Section ===
if st.button("🚀 Deploy to Netlify"):
    def create_site_with_name(name):
        response = requests.post(
            "https://api.netlify.com/api/v1/sites",
            headers={
                "Authorization": f"Bearer {NETLIFY_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"name": name}
        )
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 422:
            return None
        else:
            raise Exception(response.text)

    def generate_fallback_name(base_name):
        suffix = uuid.uuid4().hex[:6]
        return f"{base_name}-{suffix}"

    def link_folder_to_netlify(site_id):
        import traceback

        with open("netlify_debug.log", "a") as log:
            log.write(f"Linking site ID: {site_id}\n")
            log.write(f"Deploy folder: {DEPLOY_DIR_LOCAL}\n")
            log.write(f"Using NPX_PATH: {NPX_PATH}\n")

        try:
            result = subprocess.run(
                [NPX_PATH, 'netlify', 'link', '--id', site_id],
                cwd=DEPLOY_DIR_LOCAL,
                check=True,
                capture_output=True,
                text=True
            )

            with open("netlify_debug.log", "a") as log:
                log.write("Link stdout:\n" + result.stdout + "\n")
                log.write("Link stderr:\n" + result.stderr + "\n")

            stdout_lower = result.stdout.lower()
            return ("linked" in stdout_lower) or ("already linked" in stdout_lower)

        except subprocess.CalledProcessError as e:
            with open("netlify_debug.log", "a") as log:
                log.write("CalledProcessError:\n")
                log.write(e.stdout or "")
                log.write(e.stderr or "")
                log.write(traceback.format_exc())
                log.write("\n")
            return False

        except Exception as e:
            with open("netlify_debug.log", "a") as log:
                log.write("Exception:\n" + traceback.format_exc() + "\n")
            return False


    def deploy_to_netlify(site_id):
        import traceback

        try:
            result = subprocess.run(
                [NPX_PATH, 'netlify', 'deploy', '--dir', DEPLOY_DIR_LOCAL, '--prod', '--site', site_id],
                check=True,
                capture_output=True,
                text=True
            )
            with open("netlify_debug.log", "a") as log:
                log.write("Deploy stdout:\n" + result.stdout + "\n")
                log.write("Deploy stderr:\n" + result.stderr + "\n")

            return result.stdout

        except subprocess.CalledProcessError as e:
            with open("netlify_debug.log", "a") as log:
                log.write("Deploy CalledProcessError:\n")
                log.write(e.stdout or "")
                log.write(e.stderr or "")
                log.write(traceback.format_exc())
                log.write("\n")
            raise e

        except Exception as e:
            with open("netlify_debug.log", "a") as log:
                log.write("Deploy Exception:\n" + traceback.format_exc() + "\n")
            raise e


    try:
        with st.spinner("Deploying..."):
            if custom_name:
                site = create_site_with_name(custom_name)
                if not site:
                    fallback_name = generate_fallback_name(custom_name)
                    st.info(f"Custom name taken. Using fallback: `{fallback_name}`")
                    site = create_site_with_name(fallback_name)
            else:
                site = {
                    "id": "ae97f241-1b9a-4d19-8314-f4c838eff87c",
                    "url": "https://kalyanwebsite.netlify.app"
                }

            site_id = site["id"]
            url = site["url"]

            if not link_folder_to_netlify(site_id):
                st.error("Failed to link folder to Netlify.")
            else:
                output = deploy_to_netlify(site_id)
                st.success("✅ Deployed!")
                st.markdown(f"[🌍 View your website here]({url})", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Deployment failed: {e}")

