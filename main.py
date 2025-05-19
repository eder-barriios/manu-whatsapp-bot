from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(mensagem):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é a Manu, uma assistente simpática e objetiva. Responda como uma secretária de uma clínica de estética e odontologia, agende avaliações e quebre objeções com gentileza."},
            {"role": "user", "content": mensagem}
        ]
    )
    return resposta.choices[0].message.content.strip()

@app.route("/bot", methods=["POST"])
def bot():
    try:
        data = request.form or request.get_json() or {}
        user_message = data.get("Body", "") or data.get("body", "")
        if not user_message:
            return "Nenhuma mensagem recebida", 400
        resposta = gerar_resposta(user_message)
        return resposta
    except Exception as e:
        return f"Erro no servidor: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
