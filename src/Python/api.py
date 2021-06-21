import os
import webview
import json


class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def set_window_size(self, width, height):
        window = webview.windows[0]
        window.resize(width, height)

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(content)

    def ls(self):
        return os.listdir('.')

    def get_avail_destinations(self):
        dicts = [{"name": "Jool"}, {"name": "Mun"}, {
            "name": "Minmus"}, {"name": "Kerbin"}, {"name": "Leo"}]
        return dicts
