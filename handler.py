import runpod

def handler(job):
    job_input = job.get("input", {})

    name = job_input.get("name", "World")
    return f"Hello, {name}! How are you doing today?"

runpod.serverless.start({"handler": handler})


