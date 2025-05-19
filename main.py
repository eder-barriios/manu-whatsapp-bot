from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# Chave da API da OpenAI via variável de ambiente no Render
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar resposta do ChatGPT
def gerar_resposta(mensagem):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é a Manu, uma assistente simpática e objetiva. Responda como secretária de uma clínica de estética e odontologia, agendando avaliações e quebrando objeções com gentileza."
            },
            {
                "role": "user",
                "content": mensagem
            }
        ]
    )
    return resposta["choices"][0]["message"]["content"].strip()

# Rota que será chamada pelo Twilio quando o WhatsApp receber uma mensagem
@app.route("/bot", methods=["POST"])
def bot():
    try:
        data = request.form or request.get_json() or {}
        user_message = data.get("Body", "") or data.get("body", "")
        if not user_message:
            return Response(
                "<Response><Message>Mensagem vazia recebida.</Message></Response>",
                mimetype="application/xml"
            )

        resposta = gerar_resposta(user_message)

        # Monta XML (Twilio exige esse formato)
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{resposta}</Message>
</Response>"""

        return Response(twiml_response, mimetype="application/xml")

    except Exception as e:
        erro = f"Erro interno: {str(e)}"
        print("Erro:", erro)
        return Response(
            f"<Response><Message>{erro}</Message></Response>",
            mimetype="application/xml"
        )

# Executa localmente (Render ignora essa parte)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
