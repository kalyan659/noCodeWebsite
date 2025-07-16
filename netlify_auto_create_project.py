# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 11:28:38 2025

@author: kalya
"""

import requests
import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
NETLIFY_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN")
# DEPLOY_DIR = "static/output-site"
# NPX_PATH = r"D:\Program Files\npx.CMD"  # Adjust this path if needed


# def create_netlify_site():
#     headers = {
#         "Authorization": f"Bearer {NETLIFY_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     print("📦 Creating Netlify site...")
#     response = requests.post(
#     "https://api.netlify.com/api/v1/sites",
#     headers=headers,
#     json={}  # <- Add this
# )
#     response.raise_for_status()

#     site_data = response.json()
#     site_id = site_data["site_id"]
#     site_name = site_data["name"]
#     print(f"✅ Created Netlify site: {site_name} (ID: {site_id})")

#     return site_id, site_data


# def link_folder_to_netlify(site_id):
#     print("🔗 Linking folder to Netlify site...")
#     result = subprocess.run(
#         [NPX_PATH, 'netlify', 'link', '--id', site_id],
#         cwd=DEPLOY_DIR,
#         capture_output=True,
#         text=True
#     )
#     if result.returncode == 0:
#         print("✅ Folder linked to Netlify site.")
#     else:
#         raise Exception(f"❌ Failed to link folder: {result.stderr}")


# def deploy_to_netlify():
#     print("🚀 Deploying site...")
#     result = subprocess.run(
#         [NPX_PATH, 'netlify', 'deploy', '--dir=.', '--prod', '--message=Auto deploy', '--json'],
#         cwd=DEPLOY_DIR,
#         capture_output=True,
#         text=True
#     )

#     if result.returncode != 0:
#         raise Exception(f"❌ Deployment error: {result.stderr or result.stdout}")

#     try:
#         output = json.loads(result.stdout)
#         url = output.get("url")
#         print(f"🌍 Site deployed at: {url}")
#         return url
#     except json.JSONDecodeError:
#         raise Exception("⚠️ Could not parse Netlify CLI output.")


# def main():
#     site_id, site_info = create_netlify_site()
#     link_folder_to_netlify(site_id)
#     deploy_url = deploy_to_netlify()

#     print(f"\n🎉 Done! Your site is live at: {deploy_url}")


# if __name__ == "__main__":
#     main()


import requests
import uuid
import time


headers = {
    "Authorization": f"Bearer {NETLIFY_TOKEN}",
    "Content-Type": "application/json"
}

def create_site_with_name(name):
    """Try creating a site with the given name once."""
    response = requests.post(
        "https://api.netlify.com/api/v1/sites",
        headers=headers,
        json={"name": name}
    )
    if response.status_code in [200, 201]:
        print(f"✅ Site created successfully: {name}")
        return response.json()
    elif response.status_code == 422:
        print(f"⚠️ Name '{name}' is already taken.")
        return None
    elif response.status_code == 429:
        print("🚫 Rate limit hit. Try again later.")
        raise Exception("Rate limited by Netlify API.")
    else:
        print(f"❌ Unexpected error: {response.status_code}")
        print(response.text)
        response.raise_for_status()

def generate_fallback_name(base_name):
    """Create one fallback name with random suffix."""
    suffix = uuid.uuid4().hex[:6]
    return f"{base_name}-{suffix}"

def create_one_site(base_name):
    """Try creating a single Netlify site. Use fallback once if needed."""
    print(f"🧪 Trying to create site: {base_name}")
    site = create_site_with_name(base_name)
    if site:
        return site

    fallback_name = generate_fallback_name(base_name)
    print(f"🔁 Trying fallback name: {fallback_name}")
    site = create_site_with_name(fallback_name)
    if site:
        return site

    raise Exception("❌ Could not create a Netlify site with base or fallback name.")

if __name__ == "__main__":
    user_input = input("Enter desired site name (e.g. my-cool-site): ").strip().lower()
    site_info = create_one_site(user_input)
    print(f"🌐 Site URL: {site_info['url']}")
