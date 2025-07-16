
from flask import Flask, render_template, request, redirect, url_for, jsonify
from generator import call_ollama, save_code
#from deploy import deploy_to_netlify
import webbrowser
import threading
import traceback
import os
import uuid
import requests
import subprocess
from dotenv import load_dotenv
from llm_openrouter import generate_website

load_dotenv()

# === CONFIG ===
NETLIFY_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN")
DEPLOY_DIR_LOCAL = "static/output-site"
NPX_PATH = r"D:\Program Files\npx.CMD"  # Adjust this path if needed

app = Flask(__name__)

# MAIN ROUTE
@app.route('/', methods=['GET', 'POST'])
def index():
    prompt = None
    deployed_url = None
    if request.method == 'POST':
        prompt = request.form['prompt'] 
        prompt = prompt + ''' Output only the full working HTML document including embedded CSS and JavaScript 
        — no explanations, no markdown, just the code. It should be a single-page website with a hero banner, 
        about section, gallery section, and contact form. In about section write 10 lines according to topic
        of prompt. Our Gallery section upto 6 photos.Our phograpgaer section upto 6 photos with photograpger name. Add copyright of year © 2025. '''
                    
        result = generate_website(prompt)
        save_code(result)

        # Optional: open preview in browser (keep this or remove as needed)
        #threading.Timer(1.5, lambda: webbrowser.open_new_tab('/static/output-site/index.html')).start()

    return render_template('index.html', prompt=prompt, deployed_url=deployed_url)
#-----------------START: block of code to create new site based on user input--------------------------
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
        print(f"Site created successfully: {name}")
        return response.json()
    elif response.status_code == 422:
        print(f"Name '{name}' is already taken.")
        return None
    elif response.status_code == 429:
        print("Rate limit hit. Try again later.")
        raise Exception("Rate limited by Netlify API.")
    else:
        print(f"Unexpected error: {response.status_code}")
        print(response.text)
        response.raise_for_status()

def generate_fallback_name(base_name):
    """Create one fallback name with random suffix."""
    suffix = uuid.uuid4().hex[:6]
    return f"{base_name}-{suffix}"

def create_one_site(base_name):
    """Try creating a single Netlify site. Use fallback once if needed."""
    print(f"Trying to create site: {base_name}")
    site = create_site_with_name(base_name)
    if site:
        return site

    fallback_name = generate_fallback_name(base_name)
    print(f"Trying fallback name: {fallback_name}")
    site = create_site_with_name(fallback_name)
    if site:
        return site

    raise Exception("Could not create a Netlify site with base or fallback name.")
#-----------------END: block of code to create new site based on user input------------------------
#-----------------START: link local folder to netlify----------------------
def link_folder_to_netlify(site_id):
    try:
        result = subprocess.run(
            [NPX_PATH, 'netlify', 'link', '--id', site_id],
            cwd=DEPLOY_DIR_LOCAL,
            check=True,
            capture_output=True,
            text=True
        )
        print("Linked to site:", site_id)
        return True
    except subprocess.CalledProcessError as e:
        print("Linking failed:", e.stderr or str(e))
        return False
#-----------------END: link local folder to netlify----------------------
# ----------------START: deploy to netlify --------------------------------
def deploy_to_netlify(site_id):
    try:
        result = subprocess.run(
            [NPX_PATH, 'netlify', 'deploy', '--dir', DEPLOY_DIR_LOCAL, '--prod', '--site', site_id],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr or str(e))
    except FileNotFoundError:
        raise Exception("npx not found")


@app.route('/deploy')
def deploy():
    base_name = request.args.get("site", "").strip().lower()
    
    try:
        if base_name:
            # User gave a name → create and deploy to that site
            site = create_one_site(base_name)
            site_id = site["id"]
            url = site["url"]
        else:
            # No name provided → deploy to your fixed site
            site_id = "ae97f241-1b9a-4d19-8314-f4c838eff87c"  # ← You can find this from Netlify dashboard or API
            url = "https://kalyanwebsite.netlify.app"  # ← Your fixed site URL
        # Link the local folder to the Netlify site ID
        if not link_folder_to_netlify(site_id):
            return jsonify(success=False, error="Failed to link folder to site.")
        # Deploy to selected site
        output = deploy_to_netlify(site_id)

        return jsonify(success=True, url=url, raw_output=output)

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
