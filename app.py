from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/process_signal', methods=['POST'])
def process_signal():
    # Because Roblox uses ApplicationUrlEncoded, we read it as a standard form
    # The transmitter passes the parameter string directly into the form dictionary
    
    # Let's see what keys Roblox sent us
    form_data = request.form.to_dict()
    print(f"Raw form data received: {form_data}")
    
    in_value = "00000000"
    
    # Roblox might send the data inside a key named '{"value":"00000000"}' 
    # due to how ApplicationUrlEncoded packages raw text inputs.
    # We safely extract the binary bits here:
    if form_data:
        first_key = list(form_data.keys())[0]
        try:
            # If the key itself is a JSON string, we parse it
            parsed_json = json.loads(first_key)
            in_value = parsed_json.get("value", "00000000")
        except json.JSONDecodeError:
            # Fallback if it sent it as a clean key/value pair
            in_value = request.form.get("value", "00000000")

    print(f"Extracted binary from Roblox: {in_value}")
    
    # NOT GATE LOGIC: Flips 0s to 1s and 1s to 0s
    out_value = "".join(["1" if bit == "0" else "0" for bit in in_value])
    
    # Respond back to the Roblox transmitter
    return jsonify({"value": out_value})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
