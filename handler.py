import runpod
import subprocess
import requests
import os
import time

LLAMA_PORT = 3098
LLAMA_URL = f"http://127.0.0.1:{LLAMA_PORT}"

def start_llama_server():
    cmd_args = os.environ.get("LLAMA_SERVER_CMD_ARGS", "")
    cmd = f"/app/llama-server --port {LLAMA_PORT} --host 127.0.0.1 {cmd_args}"
    subprocess.Popen(cmd, shell=True)
    
    # Wait until server is ready
    for _ in range(120):
        try:
            r = requests.get(f"{LLAMA_URL}/health")
            if r.status_code == 200:
                print("llama-server ready!")
                return
        except:
            pass
        time.sleep(1)
    raise Exception("llama-server failed to start")

def handler(job):
    job_input = job["input"]
    endpoint = job_input.get("endpoint", "v1/chat/completions")
    payload = job_input.get("body", {})
    
    r = requests.post(f"{LLAMA_URL}/{endpoint}", json=payload)
    return r.json()

start_llama_server()
runpod.serverless.start({"handler": handler})
