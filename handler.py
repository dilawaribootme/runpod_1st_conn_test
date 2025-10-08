import os
import runpod
import subprocess
from pathlib import Path
import requests

def download_file(url, filename):
    """Download a file from URL to local filename."""
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return filename

def handler(job):
    job_input = job.get("input", {})

    input_video = job_input.get("input_video", "trialdu.mp4")
    bg_video = job_input.get("bg_video", "bg.mp4")

    # Support URLs
    if input_video.startswith("http"):
        input_video = download_file(input_video, "input.mp4")
    if bg_video.startswith("http"):
        bg_video = download_file(bg_video, "background.mp4")

    command = ["python", "main_bg_remover.py"]
    try:
        print("Running background remover...")
        subprocess.run(command, check=True)

        output_path = Path("last.mp4")
        if output_path.exists():
            return {"status": "success", "output": str(output_path)}
        else:
            return {"status": "error", "message": "Output video not found."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Processing failed: {e}"}

runpod.serverless.start({"handler": handler})
