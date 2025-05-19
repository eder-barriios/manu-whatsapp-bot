from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/bot', methods=['POST'])
def bot():
    try:
        data = request.form or request.get_json() or {}
        user_message = data.get("Body", "") or data.get("body", "")
        if not user_message:
            return Response("<Response><Message>Mensagem não encontrada.</Message></Response>", mimetype="application/xml")

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é a Manu, uma secretária simpática de uma clínica de estética e odontologia. Responda de forma clara, ajude com agendamentos e quebre objeções com gentileza."},
                {"role": "user", "content": user_message}
            ]
        )

        resposta = chat_completion.choices[0].message.content.strip()
        return Response(f"<Response><Message>{resposta}</Message></Response>", mimetype="application/xml")

    except Exception as e:
        return Response(f"<Response><Message>Erro interno: {str(e)}</Message></Response>", mimetype="application/xml")
