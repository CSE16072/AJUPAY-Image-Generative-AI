# 🎨 AJUPAY - Image Generative AI Pipeline

An end-to-end, modular, zero-cost (excluding serverless cloud execution) Generative AI suite designed to generate high-resolution digital payment gateway UI dashboards, web banners, and visual assets for the **AJUPAY** platform.

Powered by **Amazon Bedrock** and **Stability AI's Stable Image Core** model (`stability.stable-image-core-v1:1`), this repository provides both a **Streamlit Web Dashboard** for interactive asset creation and a **Command-Line Interface (CLI)** for automated scripting.

---

## 📂 Project Directory Structure

```text
AJUPAY/
│
├── samples/                  # Automated archive directory for generated images
│   └── YYYYMMDD-HHMMSS_prompt-slug.png
├── .env                      # Local secret keys (ignored by Git)
├── .env.example              # Environment key template for collaborators
├── .gitignore                # Git exclusions (venv, secrets, cache)
├── app.py                    # Interactive Streamlit Web UI Frontend
├── generate_image.py         # Core Bedrock engine & sample saving helper
├── image.py                  # Command-Line Interface (CLI) runner
├── README.md                 # Complete project documentation
└── requirements.txt          # Python dependencies
```

---

## 🏗️ Architecture & Component Breakdown

1. **`generate_image.py` (Backend Engine & Helper)**
   - Configures the `boto3` client to securely connect to Amazon Bedrock (`bedrock-runtime`).
   - Builds JSON payloads for `stability.stable-image-core-v1:1` including prompts, negative prompts, aspect ratios, and seeds.
   - Contains `save_to_samples()`, which automatically formats filenames with timestamps and prompt slugs, ensuring generated outputs are archived directly into the local `samples/` folder.

2. **`app.py` (Streamlit Web Application)**
   - Provides a modern web UI built with Streamlit.
   - Includes real-time inputs for positive prompts, negative prompts, aspect ratio selections, and random seed adjustments.
   - Automates on-screen image rendering, direct PNG downloads, and immediate archiving to `samples/`.

3. **`image.py` (Command Line Interface)**
   - Terminal wrapper for command-line users or automated cron tasks.
   - Accepts prompt text and flags (`--aspect`, `--seed`, `--negative`) directly via standard command-line flags.

4. **`samples/` (Automated Asset Storage)**
   - Automatically created by the system upon generating the first image.
   - Files are stored with unique, timestamped names (e.g., `20261109-201530_a-futuristic-digital-payment.png`).

---

## 🛠️ Installation & Setup Guide

### 1. Prerequisites
- Python 3.10+ or Python 3.12+ installed on your system.
- An active AWS Account with model access enabled for **Stability AI Stable Image Core** in Amazon Bedrock (`us-west-2` or your preferred region).

### 2. Virtual Environment Setup
Open your terminal inside the project root folder:

**On Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate
```

**On macOS / Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries specified in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to create your active `.env` file:
```bash
cp .env.example .env
```
Open `.env` and fill in your AWS credentials:
```env
AWS_DEFAULT_REGION=us-west-2
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
```

---

## 🚀 How to Run the Project

### Option A: Interactive Streamlit Web UI (Recommended)
To launch the web interface:
```bash
streamlit run app.py
```
- Open your browser at `http://localhost:8501`.
- Enter your UI prompt (e.g., *"A futuristic digital payment gateway UI dashboard with neon blue accents, high resolution"*).
- Choose an aspect ratio (e.g., `16:9`, `1:1`) and set a random seed.
- Click **Generate**. The generated image will automatically render on screen, provide a download link, and save into `samples/`.

### Option B: Command Line Interface (CLI)
Generate images quickly right from your terminal without opening a browser:

```bash
# Default prompt generation
python image.py

# Custom prompt with widescreen aspect ratio
python image.py "AJUPAY mobile app payment success screen design" --aspect 16:9

# Full custom execution with negative prompts and specific seed
python image.py "Neon payment dashboard" --negative "blurry, low quality" --aspect 4:5 --seed 12345
```

---

## ⚙️ Supported Parameters & Aspect Ratios

- **Supported Aspect Ratios:** `1:1`, `16:9`, `9:16`, `4:5`, `5:4`, `3:2`, `2:3`, `21:9`, `9:21`
- **Output Format:** High-Quality PNG (`.png`)
- **Model Endpoint:** `stability.stable-image-core-v1:1` via Amazon Bedrock

---

## 🛡️ Best Practices & Version Control

- **Never commit `.env` or `venv/`**: Ensure `.env` is listed in `.gitignore` to keep AWS access keys secure.
- **Samples Folder**: The `samples/` directory is automatically generated at runtime when your first image is produced.