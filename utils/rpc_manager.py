import pypresence
import time
import threading
from utils.variables import RPC_ID


class RPCManager:
    def __init__(self):
        self.rpc = None
        self.start_time = None
        self._connect_thread = None
        self._connecting = False
        self._stop_event = threading.Event()

    def _blocking_connect(self):
        if self.rpc or self._connecting:
            return False
        self._connecting = True
        try:
            rpc = pypresence.Presence(RPC_ID)
            rpc.connect()
            self.rpc = rpc
            self.start_time = time.time()
            self.rpc_update(state="Just chillin")
            return True
        except pypresence.exceptions.InvalidPipe:  # Error if discord is closed or internet is disabled
            return False
        finally:
            self._connecting = False

    def _connect_loop(self, interval_seconds: int = 10):
        while not self._stop_event.is_set() and not self.rpc:
            try:
                success = self._blocking_connect()
                if success or self.rpc:
                    break
                self._stop_event.wait(interval_seconds)
            except pypresence.exceptions.DiscordNotFound:
                break

    def rpc_connect(self, async_connect: bool = True):
        if self.rpc or self._connecting:
            return False
        if async_connect:
            self._stop_event.clear()
            self._connect_thread = threading.Thread(target=self._connect_loop, kwargs={"interval_seconds": 10}, daemon=True)
            self._connect_thread.start()
            return True
        else:
            return self._blocking_connect()

    def rpc_update(self, state: str = None, details: str = None,
                   large_image: str = None, large_text: str = None,
                   small_image: str = None, small_text: str = None):
        if not self.rpc:
            return False

        try:
            self.rpc.update(
                state=state,
                details=details,
                start=self.start_time,
                large_image=large_image,
                large_text=large_text,
                small_image=small_image,
                small_text=small_text,
            )
            return True
        except Exception:
            return False

    def rpc_close(self):
        self._stop_event.set()
        try:
            if self.rpc:
                self.rpc.close()
        finally:
            self.rpc = None
