"""Shared helper: generate an image with Amazon Bedrock and save it to samples/."""
import base64
import json
import os
import re
import time
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "stability.stable-image-core-v1:1"
REGION = os.getenv("AWS_DEFAULT_REGION", "us-west-2")
SAMPLES_DIR = Path(__file__).parent / "samples"
ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:5", "5:4", "3:2", "2:3", "21:9", "9:21"]

_client = None


def get_client():
    global _client
    if _client is None:
        _client = boto3.client("bedrock-runtime", region_name=REGION)
    return _client


def slugify(text, max_len=40):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].strip("-") or "image"


def generate_image(prompt, negative_prompt="", aspect_ratio="1:1", seed=0):
    """Return PNG bytes for the given prompt."""
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "seed": seed,
        "output_format": "png",
    }
    if negative_prompt.strip():
        payload["negative_prompt"] = negative_prompt.strip()

    response = get_client().invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )
    body = json.loads(response["body"].read())

    if not body.get("images"):
        raise RuntimeError(f"No image returned. Reason: {body.get('finish_reasons')}")
    return base64.b64decode(body["images"][0])


def save_to_samples(image_bytes, prompt):
    """Save image into samples/ and return its path."""
    SAMPLES_DIR.mkdir(exist_ok=True)
    filename = f"{time.strftime('%Y%m%d-%H%M%S')}_{slugify(prompt)}.png"
    path = SAMPLES_DIR / filename
    path.write_bytes(image_bytes)
    return path


def list_samples():
    """Newest first."""
    if not SAMPLES_DIR.exists():
        return []
    return sorted(SAMPLES_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)