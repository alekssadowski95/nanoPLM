from nanoplm import app
from flask import url_for

import webview


if __name__ == '__main__':

    window = webview.create_window('nanoPLM', app)

    try:
        import pyi_splash

        # Update the text on the splash screen
        pyi_splash.update_text("PyInstaller is a great software!")
        pyi_splash.update_text("Second time's a charm!")

        # Close the splash screen. It does not matter when the call
        # to this function is made, the splash screen remains open until
        # this function is called or the Python program is terminated.
        pyi_splash.close()
    except:
        pass

    webview.start(icon='C:/Users/Aleksander/Documents/GitHub/nanoPLM/nanoplm/static/nanoplm-logo.png')