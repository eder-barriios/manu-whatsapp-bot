from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(mensagem):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é a Manu, uma assistente simpática e objetiva. Responda como secretária da clínica, agende avaliações e quebre objeções com gentileza."},
                {"role": "user", "content": mensagem}
            ]
        )
        return resposta['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Desculpe, pode reformular sua pergunta de forma mais específica?."

@app.route("/bot", methods=["POST"])
def bot():
    try:
        user_message = request.form.get("Body", "")
        resposta = gerar_resposta(user_message)

        # Formato TwiML esperado pelo Twilio
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{resposta}</Message>
</Response>"""

        return Response(twiml_response, mimetype="application/xml")

    except Exception as e:
        erro = f"Erro interno: {str(e)}"
        print(erro)
        return Response(f"<Response><Message>{erro}</Message></Response>", mimetype="application/xml")
