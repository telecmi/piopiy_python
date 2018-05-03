from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route("/you-have-call",methods=['POST'])
def routecall():

  # Send Route Call JSON  API to PIOPIY 
   ivr={
      "ivr": {
        "welcome":{
         "play":{
            "url":"http://example.com/welcome.wav"
         }
        },
        "invalid":{
           "play":{
             "url":"http://example.com/invalid.wav"
                 }
        },
        "retry":3,
        "min":1,
        "max":1,
        "if":{
        1:{
           "http":{
            "url":"http://example.com/next-ivr"
           }
        },
        2:{
          "queue":{
           "call":[9894,967898],
           "ringback":"http://example.com/waiting.wav"
          }
        },
        3:{
          "play":{
            "url": "http://example.com/thanks.wav"
          }
        },
        4:{
          "http":{
            "url" : "http://example.com/get-dtmf"
          }
        },
        9:{
         "repeat": True
        }
        }
      }
   }

   return jsonify(ivr)

@app.route("/next-ivr",methods=['POST'])
def nextivr():

  # Send Route Call JSON  API to PIOPIY 
   ivr={
      "ivr": {
        "welcome":{
         "play":{
            "url":"http://example.com/nextwelcome.wav"
         }
        },
        "invalid":{
           "play":{
             "url":"http://example.com/nextinvalid.wav"
                 }
        },
        "retry":3,
        "min":1,
        "max":1,
        "if":{
        1:{
           "http":{
            "url":"http://example.com/you-have-call"
           }
        },
        2:{
          "queue":{
           "call":[9893,96898],
           "ringback":"http://example.com/waiting.wav"
          }
        },
        3:{
          "play":{
            "url": "http://example.com/thanks.wav"
          }
        },
        9:{
         "repeat": True
        }
        }
      }
   }

   return jsonify(ivr)



@app.route("/get-dtmf",methods=['POST'])
def getdtmf():

  play = {
      "play":{

        "url":"http://example.com/music/thanks.com"
      }
   }
  
  return jsonify(play)



if __name__ == "__main__":
    app.run()
