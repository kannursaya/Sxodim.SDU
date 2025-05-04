from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# API Key for OpenAI (or environment variable)
api_key = "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"
client = OpenAI(api_key=api_key)

# Store chat history for the session
chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    chat_history.append({"role": "user", "content": user_message})

    # Get AI response from OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=chat_history,
            temperature=1,
            top_p=1,
        )
        ai_message = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": ai_message})

        return jsonify({"reply": ai_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
