"""Streamlit Web UI for AJUPAY Image Generative AI with automatic samples folder saving."""
import base64
import json
import os
import re
import time
from pathlib import Path

import boto3
import streamlit as st
from dotenv import load_dotenv

# Load environment configuration
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


def generate_image(prompt, negative_prompt, aspect_ratio, seed):
    """Call Amazon Bedrock to generate image bytes."""
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
    """Automatically save the generated image into the samples/ folder."""
    SAMPLES_DIR.mkdir(exist_ok=True)
    filename = f"{time.strftime('%Y%m%d-%H%M%S')}_{slugify(prompt)}.png"
    path = SAMPLES_DIR / filename
    path.write_bytes(image_bytes)
    return path


# --- Streamlit UI Layout ---
st.set_page_config(page_title="AJUPAY Image Generator", page_icon="🎨")
st.title("🎨 AJUPAY AI Image Generator")
st.caption("Powered by Amazon Bedrock and Stability AI Stable Image Core")

prompt = st.text_area(
    "Prompt",
    value="A futuristic digital payment gateway UI dashboard with neon blue accents, high resolution",
    height=100,
)
negative_prompt = st.text_input("Negative prompt (optional)", placeholder="blurry, low quality, text")

col1, col2 = st.columns(2)
aspect_ratio = col1.selectbox("Aspect ratio", ASPECT_RATIOS)
seed = col2.number_input("Seed (0 = random)", min_value=0, max_value=4294967294, value=0)

if st.button("Generate", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating image via Bedrock and saving to samples/..."):
            try:
                # 1. Generate image bytes from Bedrock
                image_bytes = generate_image(prompt, negative_prompt, aspect_ratio, int(seed))
                
                # 2. Automatically archive/save into samples folder
                saved_path = save_to_samples(image_bytes, prompt)
                
                # 3. Display success and image in Streamlit dashboard
                st.success(f"Image successfully saved to: `{saved_path}`")
                st.image(image_bytes, use_container_width=True)
                
                # 4. Provide download button
                st.download_button(
                    "Download PNG",
                    data=image_bytes,
                    file_name="generated_image.png",
                    mime="image/png",
                )
            except Exception as e:
                st.error(f"Generation failed: {e}")