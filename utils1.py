import os
import pytesseract
import cv2
from PIL import Image
import numpy as np
import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

# ✅ Load local Granite model
model_path = "./granite-3.3-2b-instruct"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
    device_map="auto"
)

# ✅ Corrected function to handle attention_mask safely
def get_healthai_response(prompt):
    try:
        # Build the message as a single string from chat template
        messages = [{
            "role": "user",
            "content": f"Summarize this in 2-3 clear, friendly sentences. Avoid <think> tags:\n\n{prompt}"
        }]
        text_prompt = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False
        )

        # Tokenize the resulting text with attention mask
        inputs = tokenizer(
            text_prompt,
            return_tensors="pt",
            return_attention_mask=True
        )
        input_ids = inputs["input_ids"].to(model.device)
        attention_mask = inputs["attention_mask"].to(model.device)

        set_seed(42)

        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=512,
            do_sample=False
        )

        raw_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        cleaned_response = re.sub(r"<think>.*?</think>", "", raw_response, flags=re.DOTALL).strip()

        # Remove echoed prompt if present
        if prompt in cleaned_response:
            cleaned_response = cleaned_response.split(prompt)[-1].strip()

        return cleaned_response

    except Exception as e:
        return f"Error generating response: {e}"




# ✅ OCR extraction function
def extract_text_from_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text
    except Exception as e:
        return f"Error processing image: {e}"