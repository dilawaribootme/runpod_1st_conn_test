import sys, types
# ---- Patch: disable transparent_background GUI imports ----
sys.modules["transparent_background.gui"] = types.ModuleType("transparent_background.gui")
sys.modules["transparent_background.gui.gui"] = types.ModuleType("transparent_background.gui.gui")
# -----------------------------------------------------------

import os
import io
import base64
import requests
from PIL import Image
from transparent_background import Remover
import runpod


def download_file(url, filename):
    """Download a file from a URL to local path."""
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return filename


def handler(job):
    job_input = job.get("input", {})

    input_image = job_input.get("input_image", "check.jpg")  # image path or URL
    jit = job_input.get("jit", False)  # JIT toggle for Remover

    # Download image if a URL is provided
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

        # Convert to Base64 instead of saving to disk
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return {
            "status": "success",
            "message": "Background removed successfully",
            "base64": img_base64
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# Start the RunPod serverless handler
runpod.serverless.start({"handler": handler})
