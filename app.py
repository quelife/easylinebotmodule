from random import randint
from pythainlp import word_tokenize
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_secret = 'e03b6ab892f98d9e35000187a87987a6'
channel_access_token = '7Qm9ky2ZN5SCTfoEip4I8mddUkmYubqC0tw3emoeATzHSn8njDqpRjfD5tFmOnZ7mdzI3w81eu3IIdyb96q+z5EsMFKdxCOfSJ4uVEkK7arXpbJkPItOE6HLqw+sDLttRvScCPWV485Y9fPkyd7ZOgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
food_list = ['กระดูกอ่อนตุ๋นไชเท้ายาจีน',
             'เกาเหลาลูกชิ้นหมู',
             'แกงจืดไข่น้ำ',
             'แกงจืดเต้าหู้ไข่สาหร่าย',
             'แกงจืดแตงกวาสอดไส้',
             'แกงจืดมะระยัดไส้หมูสับ',
             'แกงจืดหมูม้วนสาหร่าย',
             'แกงจืดลูกรอก',
             'ต้มเลือดหมู',
             'ต้มจับฉ่าย',
             'ไก่ตุ๋นฟักมะนาวดอง/เห็ดหอม',
             'ซี่โครงหมูตุ๋นเยื่อไผ่',
             'มะระตุ๋นยาจีนกระดูกหมู',
             'แกงเลียงกุ้งสด',
             'แกงส้มชะอมทอดกุ้ง',
             'ต้มข่าไก่/ปลาสลิด',
             'ต้มโคล้งปลาดุกย่าง/ปลากรอบ',
             'ต้มแซบกระดูกหมูอ่อน',
             'ต้มส้มปลาทับทิม',
             'ต้มยำกุ้ง/รวมมิตร',
             'ต้มยำโป๊ะแตก',
             'แกงกระหรี่ไก่',
             'แกงคั่วสับปะรด',
             'แกงเขียวหวานปลากราย/ไก่',
             'แกงเทโพหมู',
             'แกงไตปลา',
             'แกงป่าขาหมู',
             'แกงเผ็ดเป็ดย่าง',
             'แกงเหลืองปลาขนมจีนน้ำยาปลาช่อน',
             'ฉู่ฉี่ปลา',
             'แกงไก่หน่อไม้ดอง',
             'แกงเผ็ดปลาหมึกสอดไส้',
             'แกงเผ็ดกระดูกหมู',
             'พะแนงหมู/ไก่/กุ้ง',
             'มัสมั่นหมู/ไก่',
             'น้ำตกหมู',
             'ปลาหมึกนึ่งมะนาว',
             'พล่ากุ้ง',
             'ยำก้านคะน้ากุ้งสด',
             'ยำคอหมูย่าง',
             'ไก่ย่าง',
             'ยำถั่วพลูกุ้ง',
             'ยำทะเลรวมมิตร',
             'ยำปลาดุกฟู',
             'ยำปลาทู',
             'ยำตะไคร้',
             'ยำมะเขือยาวเผา',
             'ยำวุ้นเส้นกุ้ง/ไก่/ปลาหมึก',
             'ยำหมูยอ',
             'ยำกุนเชียง',
             'ยำเห็ดหูหนูขาว',
             'ลาบหมู/ไก่/ปลาช่อน',
             'หมู/ไก่มะนาว']

app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello Guys!"


@app.route("/webhook", methods=['GET','POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    proc = word_tokenize(text, engine='newmm')
    matching = [s for s in proc if ('กิน' in s) or (
        'อาหาร' in s) or ('อะไร' in s)]
    if len(matching) != 0:
        i = randint(0, len(food_list)-1)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=food_list[i]))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text='ต้องการสุ่มอาหารหรือเปล่า หากต้องการสุ่ม พิมพ์ กินอะไรดี'))

if __name__ == "__main__":
    app.run()
