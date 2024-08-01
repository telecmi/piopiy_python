from piopiy import Action
from piopiy import RestClient


def main():
  action = Action()
  #action.playMusic('telecmi.mp3')
  #action.playMusic('https://telecmi.com/telecmi.mp3')
  action.call([919894269392,919842357292],918035731371,{ 'timeout': 20, 'loop': 4})
  #action.speak('Hello World')
  # action.setValue('myid1234567890')
  ## action.record()
  ## action.hangup()
  ## action.input('https://telecmi.com/input',{'max_digits': 1, 'timeout': 0})
  ## action.playGetInput('https://telecmi.com/input','https://telecmi.com/s3/music/telecmi.mp3',{'max_digits': 1, 'timeout': 10, 'max_retry': 1})

  # print(action.PCMO())
  
  # print(action.PCMO())

  client = RestClient(2222347,'xxxxxx')
  result=client.voice.call(9198333333,91898989,919894, {'timeout': 40, 'loop': 2, 'duration':80,'ring_type':'group'})
  print(result)
if __name__ == '__main__':
  main()