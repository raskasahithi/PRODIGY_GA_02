from flask import Flask, request, jsonify, render_template
import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO

# Load Stable Diffusion model on CPU
device = "cpu"
model_id = "runwayml/stable-diffusion-v1-5"

# Ensure model is loaded with torch.float32 for CPU
pipeline = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32  # Use float32 for CPU
)

pipeline.to(device)  # Send model to CPU

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Render index.html from the templates folder
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        # Generate the image
        # Adjust guidance_scale and num_inference_steps as needed
        image = pipeline(prompt, guidance_scale=7.5, num_inference_steps=50).images[0]

        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return jsonify({'image': img_str})

    except Exception as e:
        # Log error to console for debugging
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
