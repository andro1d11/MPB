from pypresence import Presence


class rpc():
    def __init__(self, client_id, window):
        try:
            self.CLIENT_ID = client_id
            self.window = window
            self.connectRPC()
        except:
            self.is_connected = False
            window.logs_listwidget.addItem('Discord RPC error')

    def connectRPC(self):
        try:
            self.RPC = Presence(self.CLIENT_ID)
            self.RPC.connect()
            self.is_connected = True
            self.window.logs_listwidget.addItem('Connected to Discord RPC')
        except:
            self.is_connected = False

    def update(self, text: str = '', state_text: str = ''):
        try:
            if self.is_connected:
                self.RPC.update(
                    large_image='music-notes',
                    details=text,
                    state=state_text)
            else:
                pass
        except:
            self.is_connected = False
