from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route("/you-have-call",methods=['POST'])
def hello():
    piopiy = request.get_json()
    print(piopiy['did'])
    print(piopiy['from'])

   # send Play Audio JSON API to PIOPIY
    play = {

          'url':'http://telecmi.com/music/welcome.wav'
    }

    return jsonify(play)



if __name__ == "__main__":
    app.run()
