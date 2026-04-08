import os
import subprocess
import sys
import time
from pyngrok import ngrok

NGROK_TOKEN = os.environ.get('NGROK_AUTHTOKEN') or os.environ.get('NGROK_AUTH_TOKEN')
if not NGROK_TOKEN:
    raise RuntimeError(
        'ngrok auth token not found. Set NGROK_AUTHTOKEN or NGROK_AUTH_TOKEN in your environment.'
    )

ngrok.set_auth_token(NGROK_TOKEN)

# Start Flask app in a background process
flask_process = subprocess.Popen([sys.executable, 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait briefly to ensure the server starts
time.sleep(3)

# Create a public HTTP tunnel to the local Flask port
public_url = ngrok.connect(5000, bind_tls=True)
print(f"Public URL: {public_url}")
print("Press Ctrl+C to stop the tunnel and Flask app.")

try:
    flask_process.wait()
except KeyboardInterrupt:
    print('Stopping tunnel and Flask app...')
    ngrok.disconnect(public_url)
    flask_process.terminate()
    flask_process.wait()
