import gradio as gr
import os
import time
from Paraformer import *
from paddleTTS import *
from boastLLM import *
from pydub import AudioSegment
AudioSegment.converter = './ffmpeg-2023-09-07-git-9c9f48e7f2-essentials_build/bin/ffmpeg.exe'
AudioSegment.ffmpeg = './ffmpeg-2023-09-07-git-9c9f48e7f2-essentials_build/bin/ffmpeg.exe'
AudioSegment.ffprobe = './ffmpeg-2023-09-07-git-9c9f48e7f2-essentials_build/bin/ffprobe.exe'
os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'

front = {
    'input_audio_path' : None, # 语音输入的wav文件路径
    'audio_to_text' : None, # 通过Paraformer模型识别的文本
    'output_chatbot_text' : None, # chatbot输出的文本
    'output_chatbot_audio' : None, # chatbot输出的语音路径
}

def save_audio_path(audio_path):
    # 保存麦克风输入的路径
    global front
    front['input_audio_path'] = audio_path

def audio_to_llm(history, audio):
    # paraformer语音识别
    global front
    text = generateAudioText(audio)
    front['audio_to_text'] = text
    history = history + [(text, None)]
    return history

def play_audio():
    # 输出llm生成的文字语音
    global front
    # 转换成语音
    text = front['output_chatbot_text']
    audio = generateTextAudio(text)
    front['output_chatbot_audio'] = audio
    return audio

def bot(history):
    # 放入llm
    global front
    input_text = history[-1][0]
    response = generateLLMText(input_text) # 这个是llm的输出
    front['output_chatbot_text']=response
    # response = "**That's cool!**" # 这个是llm的输出
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

def add_text(history, text):
    # 添加对话记录
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)

def Demo():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            bubble_full_width=False,
            # avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
        )

        with gr.Row():
            txt = gr.Textbox(
                scale=4,
                show_label=False,
                placeholder="Enter text and press enter",
                container=False,
            )
            with gr.Blocks():
                with gr.Row():
                    microphone = gr.Audio(source="microphone", type="filepath", label="语音输入", autoplay=False,)
                    submitButton = gr.Button('语音输入')
                with gr.Row():
                    output_audio = gr.Audio(type='filepath', label='语音输出', interactive=True, autoplay=True)
                    output_audio_button = gr.Button('语音输出')

        # 存储麦克风临时路径
        microphone.change(fn=save_audio_path, inputs=[microphone]) 

        # 语音输入
        audio_msg = submitButton.click(fn=audio_to_llm, inputs=[chatbot, microphone], outputs=[chatbot], queue=False).then( 
                        fn=bot, inputs=chatbot, outputs=chatbot
                    )

        # 文本输入
        txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
            fn=bot, inputs=chatbot, outputs=chatbot
        )
        txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)

        # 语音输出
        output_msg = output_audio_button.click(fn=play_audio, inputs=[], outputs=[output_audio])

    demo.queue()
    demo.launch(share=False)

if __name__ == '__main__':
    Demo()