# @Time: 2023/7/21 17:33
# @Auther: MHC
# @File: MQTTClient_subscribe_material_iData.py
# @Description: 纯数字识别

import paho.mqtt.client as mqtt_client
import base64
from io import BytesIO
from PIL import Image
import subprocess

# MQTT连接配置
broker = "10.16.17.50"
port = 9883
topic = "camera/image/number"
client_id = "python-mqttclientnu"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    # 回调函数用于处理接收到的消息
    def on_message(client, userdata, msg):
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        # 将编码后的图片解码
        # 解码Base64字符串为图像数据
        base64_string = msg.payload.decode()
        image_bytes = base64.b64decode(base64_string)

        # 将图像数据加载为PIL图像对象
        image = Image.open(BytesIO(image_bytes))

       # 保存图像到文件
        image.save("F:\\workplace\\Internship\\ocrToExcel\\image\\PureNumber\\received_image.jpg")

        # 判断如果保存成功则调用ocr模块
        if image:
            print("Image file saved")
            subprocess.call('E:/develop/Anaconda/Anaconda3/envs/Opencv/python '
                            'D:/MHC/pycharm/Opencv/internship/internship_openCV_pureNumber.py', shell=True)
            print("ocr module run successfully")

    client.subscribe(topic)
    client.on_message = on_message


def run_material_delivery():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run_material_delivery()
