from piopiy import Action
from piopiy import RestClient
from piopiy import StreamAction

def main():
  action = Action()
  stream = StreamAction()
  #action.playMusic('telecmi.mp3')
  #action.playMusic('https://telecmi.com/telecmi.mp3')
  # action.call([91989426,9198423],9180357,{ 'timeout': 20, 'loop': 4})
  #action.speak('Hello World')
  # action.setValue('myid1234567890')
  ## action.record()
  ## action.hangup()
  ## action.input('https://telecmi.com/input',{'max_digits': 1, 'timeout': 0})
  ## action.playGetInput('https://telecmi.com/input','https://telecmi.com/s3/music/telecmi.mp3',{'max_digits': 1, 'timeout': 10, 'max_retry': 1})
  action.stream('wss://telecmi.com/stream',{'listen_mode': 'callee', 'voice_quality':'8000', 'stream_on_answer': True})
  print(action.PCMO())
  stream.stream('wss://telecmi.com/stream',{'listen_mode': 'callee', 'voice_quality':'8000', 'stream_on_answer': True})
 
  print(stream.PCMO())

  # piopiy = RestClient(2222347,'xxxxxx')
  #result=piopiy.voice.call(9198333333,91898989,919894, {'timeout': 40, 'loop': 2, 'duration':80,'ring_type':'group'})
  # print(result)
if __name__ == '__main__':
  main()