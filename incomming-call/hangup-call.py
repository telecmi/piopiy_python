from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route("/you-have-call",methods=['POST'])
def routecall():

  # Send Route Call JSON  API to PIOPIY 
   hangup={
      "hangup": True
   }

   return jsonify(hangup)

if __name__ == "__main__":
    app.run()
