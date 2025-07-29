import pypresence
import time
from utils.variables import RPC_ID


class RPCManager:
    def __init__(self):
        self.rpc = None
        self.start_time = None

    def rpc_connect(self):
        if self.rpc:
            return False
        try:
            self.rpc = pypresence.Presence(RPC_ID)
            self.rpc.connect()
            self.start_time = time.time()
            self.rpc_update(
                state="Just chillin"
            )
            return True
        except pypresence.exceptions.InvalidPipe:  # Error if discord is closed or internet is disabled
            return False
        except Exception as e:
            return False

    def rpc_update(self, state: str = None, details: str = None, large_image: str = None, large_text: str = None,
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
        except Exception as e:
            return False

    def rpc_close(self):
        if self.rpc:
            self.rpc.close()
            self.rpc = None
