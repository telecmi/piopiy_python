from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route("/you-have-call",methods=['POST'])
def hello():
    did = request.form['did']
    caller = request.form['from']
    print(did)
    print(caller)

   # send Play Audio JSON API to PIOPIY
    play = {
         'play':{
            'url':'http://telecmi.com/music/welcome.wav'
            }
            }

    return jsonify(play)



if __name__ == "__main__":
    app.run()
