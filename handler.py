import sys, types
# ---- Patch: disable transparent_background GUI imports ----
sys.modules["transparent_background.gui"] = types.ModuleType("transparent_background.gui")
sys.modules["transparent_background.gui.gui"] = types.ModuleType("transparent_background.gui.gui")
# -----------------------------------------------------------

import io
import base64
from PIL import Image
from transparent_background import Remover
import runpod


def handler(job):
    job_input = job.get("input", {})

    # Expect base64 input instead of file or URL
    input_string = job_input.get("input_string", None)
    jit = job_input.get("jit", False)

    if not input_string:
        return {"status": "error", "message": "No Base64 string provided in input_string."}

    try:
        print("Initializing background remover model...")
        remover = Remover(jit=jit)
        remover.model_name = "InSPyReNet"

        # Decode Base64 → PIL Image
        print("Decoding Base64 input...")
        image_data = base64.b64decode(input_string)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Remove background
        print("Removing background...")
        result = remover.process(image, type="rgba")

        # Encode result → Base64
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        buffer.seek(0)
        output_b64 = base64.b64encode(buffer.read()).decode("utf-8")

        print("Background removed successfully.")
        return {
            "status": "success",
            "message": "Background removed successfully.",
            "output_base64": output_b64
        }

    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}


# Start the RunPod serverless handler
runpod.serverless.start({"handler": handler})
