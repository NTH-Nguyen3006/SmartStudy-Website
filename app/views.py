import requests
from flask import Flask, render_template, request, jsonify
from service.api_base import generateResponse

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/chatbot", methods=['GET' ,"POST"])
def chatbot():
    try:
        if request.method == "GET":
            return render_template("chatbot.html")
        
        else: # post method
            data = request.json
            if data:
                usermesssage = data.get("message", None)
                bot_response = generateResponse(user_message=usermesssage)

            if bot_response.get("error"):
                return jsonify({'message': "Server error"}), 500
            else: 
                bot_text = bot_response['candidates'][0]['content']['parts'][0]["text"]
                return jsonify({'reply': bot_text}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'message': "Server error"}), 500
    
@app.route("/chemical", methods=['GET', "POST"])
def chemical():
    if request.method == "GET":
        data = request.args.get("element", None)
        if data:
            response = requests.get(
                "https://edubot-academy.io.vn/api/chemical?element={}".format(data))
            return jsonify(response.json()), 200

        return render_template("/chemicals.html")
    
@app.route("/engdict", methods=['GET', "POST"])
def engdict():
    if request.method == "GET":
        return render_template("engdict.html")
    
    else:
        data = request.json
        if data: 
            word = data["word"]
            print(word)
            response = requests.post(
                    "https://edubot-academy.io.vn/api/eng-dictionary/", json={"word": word})
            return jsonify(response.json()), 200
            
