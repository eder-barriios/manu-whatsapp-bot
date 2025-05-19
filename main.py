from flask import Flask, request
from openai import OpenAI
import os

app = Flask(__name__)

# Inicializa o cliente com a chave da variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(mensagem):
    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é a Manu, uma secretária simpática e objetiva. Responda como assistente de uma clínica de estética e odontologia. Agende avaliações e quebre objeções com gentileza."
                },
                {
                    "role": "user",
                    "content": mensagem
                }
            ]
        )
        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print("Erro ao gerar resposta:", e)
        return "Desculpe, ocorreu um erro ao processar sua mensagem."

@app.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.form or request.get_json() or {}
        mensagem = data.get("Body") or data.get("body")
        if not mensagem:
            return "Mensagem vazia", 400

        resposta = gerar_resposta(mensagem)
        return resposta, 200

    except Exception as e:
        print("Erro no endpoint /bot:", e)
        return f"Erro interno: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
