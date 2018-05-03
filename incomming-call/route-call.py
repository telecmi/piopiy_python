from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route("/you-have-call",methods=['POST'])
def routecall():

  # Send Route Call JSON  API to PIOPIY 
   queue={
     'record': True,
     'ringblack':'http://telecmi.com/music/test.wav',
     'call':[9894,9439,9696]
   }

   return jsonify(queue)

if __name__ == "__main__":
    app.run()
