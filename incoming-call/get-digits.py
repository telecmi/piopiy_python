from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route("/you-have-call",methods=['POST'])
def routecall():

    did = request.form['did']
    caller = request.form['from']
    print(did)
    print(caller)
  # Send Route Call JSON  API to PIOPIY 
    getdigits = {
      "get": {
        "min":1,
        "max":3,
        "retry":3,
        "post":"http://example.com/nextivr",
        "start":"http://example.com/table.wav",
        "invalid":"http://example.com/invalid.wav"
      }
    }

    return jsonify(getdigits)

if __name__ == "__main__":
    app.run()
