from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Inicializa o cliente OpenAI com a chave da variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(mensagem):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é a Manu, uma assistente simpática e objetiva. Responda como secretária de uma clínica de estética e odontologia, quebrando objeções com gentileza e incentivando o agendamento da avaliação."
            },
            {
                "role": "user",
                "content": mensagem
            }
        ]
    )
    return resposta.choices[0].message.content.strip()

@app.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.form or request.get_json() or {}
        mensagem = data.get("Body", "") or data.get("body", "")
        if not mensagem:
            return "Nenhuma mensagem recebida", 400

        resposta = gerar_resposta(mensagem)
        return resposta

    except Exception as e:
        return f"Erro interno: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
