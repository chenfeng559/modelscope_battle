import paddle
from paddlespeech.cli.tts.infer import TTSExecutor
tts = TTSExecutor()

def generateTextAudio(text):
    return tts(text, output='./output/output.wav')

_ = generateTextAudio('你好')
