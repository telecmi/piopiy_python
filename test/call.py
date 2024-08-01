from piopiy import Action
from piopiy import RestClient


def main():
  action = Action()
  action.playMusic('telecmi.mp3')
  action.playMusic('https://telecmi.com/telecmi.mp3')
  action.call([1234567890,1234396168], 1236543210,{ 'timeout': 20, 'loop': 4, 'ring_type': 'group'})
  action.speak('Hello World')
  action.setValue('myid1234567890')
  action.record()
  action.hangup()
  action.input('https://telecmi.com/input',{'max_digits': 1, 'timeout': 0})
  action.playGetInput('https://telecmi.com/input','https://telecmi.com/s3/music/telecmi.mp3',{'max_digits': 1, 'timeout': 10, 'max_retry': 1})

  print(action.PCMO())
 


  print(result['code'])
if __name__ == '__main__':
  main()