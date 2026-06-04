import os
import webbrowser

from django.apps import AppConfig


class GalleryConfig(AppConfig):
    name = 'gallery'
    def ready(self):
        # This check prevents the broadcast from running twice 
        # (once for the main process and once for the reloader)
        if os.environ.get('RUN_MAIN') == 'true':
            self.send_broadcast()
    def send_broadcast(self):
        # --- YOUR BROADCAST LOGIC HERE ---
        print("Server is live at 0.0.0.0:8000! ")
        webbrowser.open('http://10.10.13.82:8000/admin/gallery/photo/')