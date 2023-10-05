from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import torch

# funasr安装:

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer_asr-en-16k-vocab4199-pytorch', # 英文版本
    # model='damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch', # 中文版本
    model_revision="v1.0.1" # 英文版本要加这个、
    )

def audio_to_text(audio_wav_path):
    """
    Params: [wav_path]
    return: Text
    """
    rec_result = inference_pipeline(audio_in=audio_wav_path)
    return rec_result

def generateAudioText(audio):
    """
    Params: [wav_path]
    return: text_str
    """
    # Paraformer读入音频并生成文本
    res = audio_to_text(audio)
    return res['text']