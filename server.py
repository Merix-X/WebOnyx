from flask import Flask, request, jsonify
from main import OnyxAI, Audio  # Tvůj hlavní soubor s AI
import speech_recognition as sr

app = Flask(__name__)
recognizer = sr.Recognizer()
onyx = OnyxAI()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("query", "")
    response = OnyxAI.mainloop()
    return jsonify({"response": response})


@app.route('/listen', methods=['GET'])
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return jsonify({"text": text})
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"})
        except sr.RequestError:
            return jsonify({"error": "Speech service not available"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
