import re
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

text_generation_zh = pipeline(Tasks.text_generation, 
                        model='damo/nlp_gpt3_kuakua-robot_chinese-large', # 夸夸
                        # model='damo/nlp_gpt3_text-generation_chinese-large',
                    )

#输出函数
def generateLLMText(input):
    input = input+"|"
    result_zh = text_generation_zh(input)
    print(result_zh)
    return result_zh['text'][result_zh['text'].find('|')+1:]

_ = generateLLMText('Hello')