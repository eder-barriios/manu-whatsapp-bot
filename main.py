from flask import Flask, request
import openai
import os

app = Flask(__name__)

# Verifica se a chave da OpenAI foi carregada corretamente
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("❌ ERRO: OPENAI_API_KEY não encontrada no ambiente!")

def gerar_resposta(mensagem):
    print("📨 Mensagem recebida para gerar resposta:", mensagem)
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é a Manu, uma assistente simpática e objetiva. Responda como uma secretária de uma clínica de estética e odontologia, agende avaliações e quebre objeções com gentileza."},
            {"role": "user", "content": mensagem}
        ]
    )
    conteudo = resposta['choices'][0]['message']['content'].strip()
    print("✅ Resposta gerada:", conteudo)
    return conteudo

@app.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.form or request.get_json() or {}
        print("🔔 Dados recebidos:", data)

        user_message = data.get("Body") or data.get("body")
        if not user_message:
            print("⚠️ Nenhuma mensagem encontrada no corpo da requisição.")
            return "Mensagem vazia", 400

        resposta = gerar_resposta(user_message)
        return resposta

    except Exception as e:
        print("❌ Erro no endpoint /bot:", str(e))
        return f"Erro interno: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
