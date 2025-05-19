
from flask import Flask, request
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(mensagem):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é a Manu, uma assistente simpática e objetiva. Responda como uma secretária de uma clínica de estética e odontologia, agende avaliações e quebre objeções com gentileza."},
            {"role": "user", "content": mensagem}
        ]
    )
    return resposta['choices'][0]['message']['content'].strip()

@app.route('/bot', methods=['POST'])
def bot():
    data = request.form
    user_message = data.get("Body", "")
    response = gerar_resposta(user_message)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
