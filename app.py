from flask import Flask, render_template
from mcstatus import JavaServer
from dataclasses import dataclass
from typing import List, Optional
import threading
import time
import re

UPDATE_FREQ_SECONDS = 30
SERVERS = [
    "refract.online",
    "mini.refract.online",
    "alt.refract.online",
    "spin.refract.online",
]
server_info_cache = {}


@dataclass
class MinecraftServerInfo:
    online: bool
    address: str
    icon: Optional[str]
    current_players: int
    max_players: int
    motd: str
    player_list: List[str]
    version: str
    server_type: str


def get_server_type_and_version(version_string: str) -> tuple:
    # Default values
    server_type = "Unknown"
    version = "Unknown"

    # Try to extract Minecraft version
    mc_version_match = re.search(r'(\d+\.\d+(\.\d+)?)', version_string)
    if mc_version_match:
        version = mc_version_match.group(1)
    print(version_string)
    # Check for known server types
    if "bukkit" in version_string.lower() or "craftbukkit" in version_string.lower():
        server_type = "Bukkit/CraftBukkit"
    elif "spigot" in version_string.lower():
        server_type = "Spigot"
    elif "paper" in version_string.lower():
        server_type = "Paper"
    elif "forge" in version_string.lower():
        server_type = "Forge"
    elif "fabric" in version_string.lower():
        server_type = "Fabric"
    elif "vanilla" in version_string.lower():
        server_type = "Vanilla"
    elif "sponge" in version_string.lower():
        server_type = "Sponge"
    
    return server_type, version


def fetch_minecraft_server_info(address: str) -> MinecraftServerInfo:
    try:
        server = JavaServer.lookup(address)
        queryResponse = server.async_query()
        status = server.status()
        print(queryResponse.Software.brand)
        

        server_type, version = get_server_type_and_version(status.version.name)
        server_type = queryResponse.Software.brand
        print(server_type)
        
        return MinecraftServerInfo(
            online=True,
            address=address,
            icon=status.icon.split(',')[-1] if status.icon else None,
            current_players=status.players.online,
            max_players=status.players.max,
            motd=status.description,
            player_list=[player.name for player in status.players.sample] if status.players.sample else [],
            version=version,
            server_type=server_type,
        )
    except Exception as e:
        print(f"Error fetching info for {address}: {str(e)}")
        return MinecraftServerInfo(False, address, None, 0, 0, "", [], "Unknown", "Unknown")


def update_server_info():
    while True:
        for server in SERVERS:
            server_info_cache[server] = fetch_minecraft_server_info(server)
        
        time.sleep(UPDATE_FREQ_SECONDS)


def get_sorted_servers():
    return sorted(
        server_info_cache.values(),
        key=lambda s: (not s.online, -s.current_players, s.address)
    )



app = Flask(__name__)

# Start the background thread to update server info
threading.Thread(target=update_server_info, daemon=True).start()

@app.route('/')
def index():
    return render_template("dashboard.html", servers=get_sorted_servers())

if __name__ == "__main__":
    app.run(debug=True)











