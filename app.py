from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import pad_sequences

app = Flask(__name__)

encoder_model = load_model("encoder_model.keras")
decoder_model = load_model("decoder_model.keras")

with open("encoder_tokenizer.pkl","rb") as f:
    encoder_tokenizer = pickle.load(f)

with open("decoder_tokenizer.pkl","rb") as f:
    decoder_tokenizer = pickle.load(f)

with open("config.pkl","rb") as f:
    config = pickle.load(f)

input_maxln = config["input_mxlen"]
output_maxln = config["output_mxlen"]


def translate(sentence):

    sequence = encoder_tokenizer.texts_to_sequences([sentence])

    sequence = pad_sequences(sequence,
                             maxlen=input_maxln,
                             padding="post")

    states = encoder_model.predict(sequence, verbose=0)

    start = decoder_tokenizer.word_index["<start>"]
    end = decoder_tokenizer.word_index["<end>"]

    target_seq = np.array([[start]])

    translated = []

    while True:

        output, h, c = decoder_model.predict(
            [target_seq] + states,
            verbose=0
        )

        token = np.argmax(output[0, -1, :])

        if token == end:
            break

        word = decoder_tokenizer.index_word.get(token, "")

        if word:
            translated.append(word)

        target_seq = np.array([[token]])
        states = [h, c]

        if len(translated) > output_maxln:
            break

    return " ".join(translated)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate_api():

    text = request.json["text"]

    prediction = translate(text)

    return jsonify({
        "translation": prediction
    })


if __name__ == "__main__":
    app.run(debug=True)