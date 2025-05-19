from flask import Flask, request
from openai import OpenAI
import os

app = Flask(__name__)

# Inicializa o cliente da nova versão da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(mensagem):
    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é a Manu, uma secretária simpática e objetiva. Sua missão é responder clientes da clínica com gentileza, esclarecer dúvidas e agendar avaliações."},
                {"role": "user", "content": mensagem}
            ]
        )
        return resposta.choices[0].message.content.strip()

    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

@app.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.form or request.get_json() or {}
        user_message = data.get("Body") or data.get("body", "")
        
        if not user_message:
            return "Nenhuma mensagem recebida", 400

        resposta = gerar_resposta(user_message)
        return resposta, 200

    except Exception as e:
        return f"Erro no servidor: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
