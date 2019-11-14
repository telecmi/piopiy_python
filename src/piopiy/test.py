from action import Action


test = Action()
test.playMusicName('murugan.mp3')
test.playMusicURL('http://example.com/invalid.wav')
test.forward([98943, 9677697], 4471316044, {
    'ring_type': 'group', 'duration': 300, 'timeout': 20, 'loop': 5})
test.hangup()
test.record()
test.input('http://telecmi.com')
print(test.PCMO())
