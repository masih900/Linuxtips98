from flask import Flask, render_template_string, request, jsonify
import threading, time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>AI Chat</title></head>
<body style="font-family:sans-serif;max-width:600px;margin:auto;padding-top:50px;text-align:center;">
  <h1>Small AI Chat</h1>
  <textarea id="prompt" rows="4" style="width:80%;font-size:16px;" placeholder="Type something..."></textarea><br><br>
  <button onclick="generate()" style="font-size:16px;padding:10px 20px;">Generate</button>
  <pre id="output" style="text-align:left;background:#f4f4f4;padding:15px;margin-top:20px;white-space:pre-wrap;"></pre>

  <script>
    async function generate() {
      const prompt = document.getElementById('prompt').value;
      const out = document.getElementById('output');
      out.textContent = 'Thinking...';
      const res = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt})
      });
      const data = await res.json();
      out.textContent = data.text || data.error;
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Loading tiny model...")
tokenizer = AutoTokenizer.from_pretrained("Xenova/distilgpt2")
model = AutoModelForCausalLM.from_pretrained("Xenova/distilgpt2")
print("Model loaded.")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run():
    app.run(host="0.0.0.0", port=5000)

thread = threading.Thread(target=run, daemon=True)
thread.start()
time.sleep(2)

from google.colab import output
output.eval_js("google.colab.kernel.proxyPort(5000)")
