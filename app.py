from flask import Flask, render_template, send_from_directory
from mcinfo import MCInfo, ServerWatcher
from file_fetcher import get_file_icon, list_static_files
# import dotenv
import os



MC_SERVERS = []
UPDATE_DELAY = 5
STATIC_PATH = "static"


env_servers = os.getenv("MC_SERVERS") # space seperated server ips
if env_servers:
    MC_SERVERS = env_servers.split(" ")



app = Flask(__name__)
mcstatus = MCInfo()
watcher = ServerWatcher()
print("WATCHING:")
print(MC_SERVERS)
watcher.start_watcher(MC_SERVERS, 5)

# Start the background thread to update server info


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/downloads')
def downloads():
    files = {}
    for filename in list_static_files(STATIC_PATH):
        files[filename] = get_file_icon(filename)
    return render_template("downloads.html", files=files)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", servers=watcher.get_sorted_cache())

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(STATIC_PATH, filename, as_attachment=True)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)











