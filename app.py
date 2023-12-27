from dotenv import load_dotenv
import streamlit as sl
import os
from PIL import Image
import google.generativeai as gai

load_dotenv()
gai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = gai.GenerativeModel('gemini-pro-vision')
def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Image was not found")

sl.set_page_config(page_title = 'Invoice Extractor')

sl.header("Invoice Extractor")
input = sl.text_input("Input Desired Prompt: ",key="input")
uploaded_file = sl.file_uploader("Choose an image of the invoice", type=["jpg", "png", "jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    sl.image(image, caption="Uploaded image", use_column_width=True)

submit = sl.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices.
We upload a image of an invoice and you will have 
to answer any questions based on the uploaded image"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    sl.subheader("The Insights are:")
    sl.write(response)


