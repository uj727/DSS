from flask import Flask, request, render_template
from transformers import pipeline
import os
import openai
from googletrans import Translator 

openai.api_key = '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'

app = Flask(__name__)

def translate_text(text,de):#翻譯套件
    translator = Translator()
    result = translator.translate(text, dest=de).text
    return result

def load_model():
    # 設全域變數
    # global classifier
    # # 載入模型
    # classifier = pipeline("sentiment-analysis")
    print("Fininsh loading")

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # 接收post來的句子
        txt_zh = request.values['txt']
        txt_en = translate_text(txt_zh, 'en')#輸入的句子轉英文
        # 預測句子
        response = openai.Completion.create(
             model="curie:ft-ice:dss1211-2022-12-11-14-13-48",
            prompt=txt_en + '->',
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["END"]
)
        re_en = response['choices'][0]['text'] 
        re_zh = translate_text(re_en, 'zh-tw')
        return render_template('index.html', sentence=txt_zh, res=re_zh)
    return render_template('index.html')

if __name__ == '__main__':
    load_model()
    #app.run(host='0.0.0.0')
    app.run()
    
