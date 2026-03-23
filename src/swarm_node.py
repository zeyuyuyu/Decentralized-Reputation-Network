import socket
import threading
import time
import json
from typing import Dict, Set

class SwarmNode:
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.peers: Dict[str, float] = {}  # addr -> last_seen timestamp
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.heartbeat_interval = 5.0
        self.peer_timeout = 15.0

    def start(self):
        self.running = True
        # Start listener thread
        threading.Thread(target=self._listen, daemon=True).start()
        # Start heartbeat thread
        threading.Thread(target=self._heartbeat, daemon=True).start()
        # Start cleanup thread
        threading.Thread(target=self._cleanup_peers, daemon=True).start()

    def stop(self):
        self.running = False
        self.sock.close()

    def _listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                msg = json.loads(data.decode())
                
                if msg['type'] == 'heartbeat':
                    self.peers[f'{addr[0]}:{addr[1]}'] = time.time()
                elif msg['type'] == 'discovery':
                    # Send back our peer list
                    response = {
                        'type': 'peers',
                        'peers': list(self.peers.keys())
                    }
                    self.sock.sendto(json.dumps(response).encode(), addr)
                    
            except Exception as e:
                print(f'Error in listener: {e}')

    def _heartbeat(self):
        while self.running:
            try:
                msg = {
                    'type': 'heartbeat',
                    'timestamp': time.time()
                }
                # Broadcast to all known peers
                for peer in list(self.peers.keys()):
                    host, port = peer.split(':')
                    self.sock.sendto(json.dumps(msg).encode(), (host, int(port)))
            except Exception as e:
                print(f'Error in heartbeat: {e}')
            time.sleep(self.heartbeat_interval)

    def _cleanup_peers(self):
        while self.running:
            try:
                current_time = time.time()
                # Remove peers that haven't sent a heartbeat recently
                self.peers = {
                    addr: last_seen 
                    for addr, last_seen in self.peers.items()
                    if current_time - last_seen < self.peer_timeout
                }
            except Exception as e:
                print(f'Error in cleanup: {e}')
            time.sleep(self.heartbeat_interval)

    def discover_peers(self, bootstrap_nodes: Set[str]):
        """Attempt to discover peers through bootstrap nodes"""
        msg = {
            'type': 'discovery'
        }
        for node in bootstrap_nodes:
            try:
                host, port = node.split(':')
                self.sock.sendto(json.dumps(msg).encode(), (host, int(port)))
            except Exception as e:
                print(f'Error discovering peers through {node}: {e}')

    def get_active_peers(self) -> Set[str]:
        """Return set of currently active peers"""
        return set(self.peers.keys())

    def broadcast(self, data: bytes):
        """Broadcast data to all known peers"""
        msg = {
            'type': 'data',
            'payload': data.decode()
        }
        for peer in list(self.peers.keys()):
            try:
                host, port = peer.split(':')
                self.sock.sendto(json.dumps(msg).encode(), (host, int(port)))
            except Exception as e:
                print(f'Error broadcasting to {peer}: {e}')