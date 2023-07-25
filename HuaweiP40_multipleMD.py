# @Time: 2023/7/23 14:00
# @Auther: MHC
# @File: HuaweiP40_multipleMD.py
# @Description:

import paho.mqtt.client as mqtt_client
import base64
from io import BytesIO
from PIL import Image
import subprocess
import os
import re

# MQTT连接配置
broker = "10.16.16.145"
port = 9883
topic = "camera/image/multiplyMD"
client_id = "python-mqttclientMD"


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
    # 定义保存消息的变量和列表
    message_count = 0
    text = ""

    # 回调函数用于处理接收到的消息
    def on_message(client, userdata, msg):
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        global path
        nonlocal message_count
        nonlocal text
        message_count += 1

        if message_count == 1:
            # 在F:\\workplace\\Internship\\ocrToExcel\\image\\MaterialDelivery目录下创建一个新的文件夹
            # 用于存放接收到的图片
            path = "F:\\workplace\\Internship\\ocrToExcel\\image\\MaterialDelivery\\tempt\\"
            os.mkdir(path)

        if msg.payload.decode() != "multipleMD-confirm":
            # 将编码后的图片解码
            # 解码Base64字符串为图像数据
            base64_string = msg.payload.decode()
            image_bytes = base64.b64decode(base64_string)

            # 将图像数据加载为PIL图像对象
            image = Image.open(BytesIO(image_bytes))

            # 保存图像到文件
            process_path = path + str(message_count) + ".jpg"
            image.save(process_path)
            command = [
                'E:/develop/Anaconda/Anaconda3/envs/Opencv/python',
                'D:/MHC/pycharm/Opencv/internship/image_process.py',
                process_path
            ]
            subprocess.call(command, shell=True)

            # 判断如果保存成功则调用ocr模块
            if image and message_count == 1:
                print("Image file saved")

                # 命令行参数列表
                args = ['E:/develop/Anaconda/Anaconda3/envs/Opencv/python',
                        'D:/MHC/pycharm/Opencv/HuaweiP40_multiple.py']
                # 调用另一个Python脚本，并获取其返回值
                result = subprocess.run(args, capture_output=True, text=True)
                # print(result)
                # print(result.stdout.strip())
                # 不知道为什么这里会输出乱码，但是没有关系，只需要取出数字部分即可
                text = result.stdout.strip()  # 获取标准输出结果
                # 取出数字部分
                text = re.sub(r'\D', '', text)
                print("ocr module run successfully")
        else:
            print("上传完成")
            original_folder_path = "F:\\workplace\\Internship\\ocrToExcel\\image\\MaterialDelivery\\tempt"
            # 新的文件夹名称
            new_folder_name = "materialDelivery-" + text
            # 判断是否已经存在同名文件夹
            if os.path.exists("F:\\workplace\\Internship\\ocrToExcel\\image\\MaterialDelivery\\" + new_folder_name):
                # 如果存在则弹出提示信息
                print("文件夹已存在")
            else:
                # 修改文件夹名称
                new_folder_path = os.path.dirname(original_folder_path) + os.sep + new_folder_name
                os.rename(original_folder_path, new_folder_path)
                message_count = 0
                text = ""

    client.subscribe(topic)
    client.on_message = on_message


def run_material_delivery():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run_material_delivery()

