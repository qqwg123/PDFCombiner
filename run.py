from app import create_app
import webbrowser
import os

app = create_app()

if __name__ == '__main__':
    # Open browser when running directly
    webbrowser.open("http://127.0.0.1:5000")
    app.run()