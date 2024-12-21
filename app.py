from flask import Flask, request, jsonify
import speech_recognition as sr
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    language = request.form.get('language', 'en-US')
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            print(f"Listening... Speak now in {language}!")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language=language)
            return jsonify({'status': 'success', 'text': text})
        except sr.UnknownValueError:
            return jsonify({'status': 'error', 'message': 'Sorry, could not understand the audio.'})
        except sr.RequestError as e:
            return jsonify({'status': 'error', 'message': f'API Error: {e}'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
