import time
import threading
from dataclasses import dataclass, asdict
from mcstatus import JavaServer
from typing import List, Optional

@dataclass
class ServerInfo:
    online: bool
    address: str
    icon: Optional[str]
    current_players: int
    max_players: int
    motd: str
    player_list: List[str]
    version: str
    server_type: str


class MCInfo:
    def get_server_info(self, address: str) -> ServerInfo:
        try:
            server = JavaServer.lookup(address)
            status = server.status()
            return ServerInfo(
                online=True,
                address=address,
                icon=status.icon.split(',')[-1] if status.icon else None,
                current_players=status.players.online,
                max_players=status.players.max,
                motd=status.description,
                player_list=[player.name for player in status.players.sample] if status.players.sample else [],
                version=status.version.name,
                server_type="Unknown",
            )
        except Exception as e:
            return ServerInfo(False, address, None, 0, 0, "", [], "Unknown", "Unknown")

    def get_sorted_servers(self, address_array):
        server_info_array = []
        for address in address_array:
            try:
                info = self.get_server_info(address)
                server_info_array.append(info)
            except Exception as e:
                print(f"Error fetching info for {address}: {e}")
                server_info_array.append(ServerInfo(False, address, None, 0, 0, "", [], "Unknown", "Unknown"))
        return sorted(
            server_info_array,
            key=lambda s: (not s.online, -s.current_players, s.address)
        )

class ServerWatcher:
    def __init__(self):
        self.mc_info = MCInfo()
        self.cache = []
        self.running = False
        self.thread = None

    def start_watcher(self, server_list, delay_in_seconds):
        if self.running:
            print("Watcher is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._update_loop, args=(server_list, delay_in_seconds))
        self.thread.start()

    def stop_watcher(self):
        if not self.running:
            print("Watcher is not running")
            return

        self.running = False
        if self.thread:
            self.thread.join()

    def get_sorted_cache(self):
        return sorted(
            self.cache,
            key=lambda s: (not s.online, -s.current_players, s.address)
        )

    def _update_loop(self, server_list, delay_in_seconds):
        while self.running:
            self.cache = self.mc_info.get_sorted_servers(server_list)
            time.sleep(delay_in_seconds)
