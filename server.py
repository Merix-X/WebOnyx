from flask import Flask, request, jsonify
import OnyxAI  # Tvůj hlavní soubor s AI
import speech_recognition as sr

app = Flask(__name__)

onyx = OnyxAI.OnyxAI()  # Inicializace asistenta

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("query", "")
    response = onyx.TakeCommand()  # Nebo nějaká jiná metoda na zpracování vstupu
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
