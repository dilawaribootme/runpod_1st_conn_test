import os
import runpod
from PIL import Image
import sys, types
# Patch flet GUI import (skip it completely)
sys.modules["transparent_background.gui"] = types.ModuleType("transparent_background.gui")
from transparent_background import Remover
import requests

def download_file(url, filename):
    """Download a file from URL to local path."""
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return filename

def handler(job):
    job_input = job.get("input", {})

    input_image = job_input.get("input_image", "check.jpg")
    output_name = job_input.get("output_name", "outputfinal.png")
    jit = job_input.get("jit", False)

    # If image provided as URL, download it
    if input_image.startswith("http"):
        input_image = download_file(input_image, "input.jpg")

    if not os.path.exists(input_image):
        return {"status": "error", "message": f"Input file not found: {input_image}"}

    try:
        print(f"Loading image: {input_image}")
        image = Image.open(input_image).convert("RGB")

        print("Removing background...")
        remover = Remover(jit=jit)
        result = remover.process(image, type="rgba")

        print(f"Saving result as: {output_name}")
        result.save(output_name)

        return {"status": "success", "output": output_name}

    except Exception as e:
        return {"status": "error", "message": str(e)}

runpod.serverless.start({"handler": handler})

