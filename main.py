from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar resposta via OpenAI
def gerar_resposta(mensagem):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é a Manu, assistente simpática e objetiva. Responda como secretária da clínica de estética e odontologia, agende avaliações e quebre objeções com gentileza."},
                {"role": "user", "content": mensagem}
            ]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print("Erro ao gerar resposta da OpenAI:", str(e))
        return "Desculpe, pode reformular sua pergunta, não entendi."

# Rota para receber mensagens do WhatsApp (Twilio)
@app.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.form or request.get_json()
        user_message = data.get("Body", "") or data.get("body", "")

        if not user_message:
            return "Mensagem vazia recebida.", 400

        resposta = gerar_resposta(user_message)
        return resposta, 200

    except Exception as e:
        print("Erro no endpoint /bot:", str(e))
        return jsonify({"erro": "Falha no servidor", "detalhes": str(e)}), 500

# Rodar localmente (apenas para testes locais, não usado no Render)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
