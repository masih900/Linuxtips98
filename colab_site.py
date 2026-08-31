from flask import Flask, render_template_string
import threading, time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Hello</title></head>
<body style="font-family:sans-serif;text-align:center;padding-top:50px;">
  <h1>Hello from Colab!</h1>
  <p>This is a simple public site.</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

def run():
    app.run(host="0.0.0.0", port=5000)

thread = threading.Thread(target=run, daemon=True)
thread.start()
time.sleep(2)

from google.colab import output
from pyngrok import ngrok

public_url = ngrok.connect(5000).public_url
print("Public URL:", public_url)
output.eval_js('window.open("' + public_url + '", "_blank");')
