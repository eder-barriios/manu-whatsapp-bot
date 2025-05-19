from flask import Flask, request
import openai
import os

app = Flask(__name__)

# Chave da OpenAI (definida em "Secrets" no Render como OPENAI_API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar resposta usando o modelo GPT
def gerar_resposta(mensagem):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é a Manu, uma assistente simpática e objetiva. Responda como uma secretária de uma clínica de estética e odontologia, agende avaliações e quebre objeções com gentileza."},
            {"role": "user", "content": mensagem}
        ]
    )
    return resposta['choices'][0]['message']['content'].strip()

# Endpoint que o Twilio vai chamar ao receber uma mensagem no WhatsApp
@app.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.form or request.get_json() or {}
        user_message = data.get("Body", "") or data.get("body", "")
        if not user_message:
            return "Nenhuma mensagem recebida", 400

        response = gerar_resposta(user_message)
        return response

    except Exception as e:
        return f"Erro no servidor: {str(e)}", 500

# Executa localmente (ignorado no Render, mas bom pra testes locais)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
