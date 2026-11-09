"""Command-line version: python generate_image.py "your prompt" --aspect 16:9"""
import argparse

from generate_image import ASPECT_RATIOS, generate_image, save_to_samples


def main():
    parser = argparse.ArgumentParser(description="Generate an image with Amazon Bedrock")
    parser.add_argument(
        "prompt",
        nargs="?",
        default="A futuristic digital payment gateway UI dashboard with neon blue accents, high resolution",
    )
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--aspect", default="1:1", choices=ASPECT_RATIOS)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    print("Generating image...")
    try:
        image_bytes = generate_image(args.prompt, args.negative, args.aspect, args.seed)
        path = save_to_samples(image_bytes, args.prompt)
        print(f"SUCCESS! Saved to {path}")
    except Exception as error:
        print(f"Generation failed: {error}")


if __name__ == "__main__":
    main()