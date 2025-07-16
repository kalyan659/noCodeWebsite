# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 13:28:50 2025

@author: kalya
"""

import subprocess
import os
import json
import re
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
NETLIFY_TOKEN = os.getenv("NETLIFY_AUTH_TOKEN")
DEPLOY_DIR_LOCAL = "static/output-site"
NPX_PATH = r"D:\Program Files\npx.CMD"  # Adjust this path if needed




# ----------------END: 

# def deploy_to_netlify(folder='static/output-site'):
#     try:
#         # Deploy with --prod to publish live immediately
#         result = subprocess.run(
#             ['netlify', 'deploy', '--dir', folder, '--prod'],
#             capture_output=True, text=True, check=True
#         )
#         output = result.stdout
        
#         # Extract URL from Netlify CLI output
#         for line in output.splitlines():
#             if 'Website URL:' in line:
#                 url = line.split('Website URL:')[-1].strip()
#                 return url
        
#         return "Deployment succeeded, but no URL found."
#     except subprocess.CalledProcessError as e:
#         return f"Deployment failed:\n{e.stderr}"
# def deploy_to_netlify(folder='static/output-site'):
#     try:
#         netlify_cmd = r"C:\Users\kalya\AppData\Roaming\npm\netlify.cmd"

#         env = os.environ.copy()
#         env["PATH"] += r";D:\Program Files"

#         process = subprocess.Popen(
#             [netlify_cmd, 'deploy', '--dir', folder, '--prod', '--json', '--silent'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             env=env
#         )
#         stdout, stderr = process.communicate()

#         if process.returncode != 0:
#             print("🚨 Netlify deploy error:")
#             print(stderr)
#             return f"Deployment failed: {stderr}"

#         # Look for URL in JSON output
#         try:
#             for line in stdout.splitlines():
#                 if '"url"' in line:
#                     match = re.search(r'"url":\s*"([^"]+)"', line)
#                     if match:
#                         return match.group(1)
#         except Exception as parse_err:
#             return f"Deployment succeeded but parsing failed: {str(parse_err)}"

#         return "Deployment succeeded, but no URL found."

#     except Exception as e:
#         return f"Exception during deployment: {str(e)}"



# def deploy_to_netlify(folder='static/output-site'):
#     try:
#         env = os.environ.copy()
#         netlify_path = r"C:\Users\kalya\AppData\Roaming\npm"
#         env["PATH"] = netlify_path + ";" + env["PATH"]

#         # Use `npx` to ensure correct async context
#         command = f'npx netlify deploy --dir="{folder}" --prod --json --silent'

#         process = subprocess.Popen(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             shell=True,
#             text=True,
#             env=env
#         )

#         stdout, stderr = process.communicate()

#         if process.returncode != 0:
#             print("🚨 Netlify deploy error:")
#             print(stderr)
#             return f"Deployment failed: {stderr}"

#         for line in stdout.splitlines():
#             if '"url"' in line:
#                 try:
#                     data = json.loads(line.strip())
#                     return data['url']
#                 except Exception:
#                     match = re.search(r'"url":\s*"([^"]+)"', line)
#                     if match:
#                         return match.group(1)

#         return "Deployment succeeded, but no URL found."

#     except Exception as e:
#         return f"Exception during deployment: {str(e)}"
# def deploy_to_netlify(auto_link=True):
#     deploy_dir = os.path.abspath("static/output-site")
#     npx_path = r"D:\Program Files\npx.CMD"  # <-- Update to your correct npx path
#     netlify_cmd = [npx_path, "netlify", "deploy", "--dir", deploy_dir, "--prod"]

#     try:
#         result = subprocess.run(
#             netlify_cmd,
#             capture_output=True, text=True, check=True
#         )
#         output = result.stdout

#         for line in output.splitlines():
#             if "Website URL:" in line:
#                 return line.split("Website URL:")[-1].strip()

#         return "Deployment succeeded, but no URL found."

#     except subprocess.CalledProcessError as e:
#         stderr = e.stderr or ""
#         if auto_link and "This folder isn't linked to a project yet" in stderr:
#             subprocess.run([npx_path, "netlify", "init"], check=True)
#             return deploy_to_netlify(auto_link=False)

#         return f"Deployment failed:\n{stderr}"
import os
import wexpect
import subprocess

# def deploy_to_netlify():
#     npx_path = r"D:\Program Files\npx.CMD"  # <- Your npx path here
#     result = subprocess.run(
#         [npx_path, "netlify", "deploy", "--prod", "--dir=static/output-site"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,
#         shell=True
#     )

#     if result.returncode != 0:
#         raise RuntimeError(result.stderr)

#     # Parse the URL from stdout
#     for line in result.stdout.splitlines():
#         if "Production deploy is live" in line:
#             continue
#         if line.strip().startswith("https://") and ".netlify.app" in line:
#             return line.strip()

#     return "Deployment successful, but could not find URL in output."
def deploy_to_netlify():
    npx_path = r"D:\Program Files\npx.CMD"  # <- Your npx path here
    try:
        result = subprocess.run(
            [npx_path, 'netlify', 'deploy', '--dir=static/output-site', '--prod', '--message', 'Auto deploy'],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error during deploy: {e.stderr or str(e)}"
    except FileNotFoundError as e:
        return f"npx not found: {e}"
# def deploy_to_netlify(site_name=None):
#     npx_path = r"D:\Program Files\npx.CMD"  # Your npx path here
#     try:
#         cmd = [
#             npx_path,
#             'netlify',
#             'deploy',
#             '--dir=static/output-site',
#             '--prod',
#             '--message', 'Auto deploy'
#         ]
#         if site_name:
#             cmd += ['--site', site_name]

#         result = subprocess.run(
#             cmd,
#             check=True,
#             capture_output=True,
#             text=True
#         )
#         return result.stdout
#     except subprocess.CalledProcessError as e:
#         return f"Error during deploy: {e.stderr or str(e)}"
#     except FileNotFoundError as e:
#         return f"npx not found: {e}"


# NETLIFY_DIR = "static/output-site"
# TEAM_NAME = "python"  # your Netlify team name here
# SITE_NAME = ""        # leave blank for auto name or specify

# def is_linked():
#     # Netlify creates a `.netlify` folder in your project root when linked
#     return os.path.isdir(".netlify")

# def automate_netlify_link():
#     child = wexpect.spawn('npx netlify link', encoding='utf-8', timeout=60)
    
#     child.expect([
#     r"What would you like to do\?",
#     r"This folder isn't linked to a project yet",
#     r"Choose from a list of your recently updated projects",
#     r"Enter a project ID"
#     ], timeout=120)
#     before = child.before or ''
#     after = child.after or ''
#     print("Current buffer after expect:", before + after)
#     options_text = child.before + child.after
#     lines = options_text.splitlines()
#     option_num = None
#     for i, line in enumerate(lines):
#         if "Create & configure a new project" in line:
#             option_num = i + 1
#             break
#     if option_num is None:
#         raise RuntimeError("Could not find 'Create & configure a new project' option.")
#     child.sendline(str(option_num))

#     child.expect("Team:")
#     child.sendline(TEAM_NAME)

#     child.expect("Project name")
#     child.sendline(SITE_NAME)

#     child.expect("Deploy folder")
#     child.sendline(NETLIFY_DIR)

#     child.expect(wexpect.EOF)

# def deploy_to_netlify():
#     if not is_linked():
#         automate_netlify_link()

#     result = subprocess.run([
#         "npx", "netlify", "deploy",
#         f"--dir={NETLIFY_DIR}",
#         "--prod",
#         "--message", "Automated deploy"
#     ], capture_output=True, text=True)

#     if result.returncode == 0:
#         return result.stdout
#     else:
#         raise RuntimeError(f"Netlify deploy failed:\n{result.stderr}")
