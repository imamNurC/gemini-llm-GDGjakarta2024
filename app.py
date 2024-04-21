"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template, request

import base64
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel


# pylint: disable=C0103
app = Flask(__name__)

vertexai.init(project="geminillm-gdg-jkt2024", location="us-west1")
model = GenerativeModel("gemini-1.0-pro-001")
def generate(user_input):
   
    responses = model.generate_content(
        contents=user_input,
        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        },
        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=True,
    )
    
    
    return responses






@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('prompt')
        model_resp = generate(user_input)

        response = ""
        for res in model_resp:
            response += res.text
        return render_template('text.html', response=response)
    else:
        return render_template('text.html')


# def hello():
#     """Return a friendly HTTP greeting."""
#     message = "It's running!"

#     """Get Cloud Run environment variables."""
#     service = os.environ.get('K_SERVICE', 'Unknown service')
#     revision = os.environ.get('K_REVISION', 'Unknown revision')

#     return render_template('index.html',
#         message=message,
#         Service=service,
#         Revision=revision)




if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')