import pyrebase
from pusher_push_notifications import PushNotifications
import time

firebaseConfig = {
    'apiKey': "AIzaSyDGXyuMff5dbI7te0X4IuyfcQfCsomjZp8",
    'authDomain': "deteksi-dini-kebakaran-49169.firebaseapp.com",
    'databaseURL': "https://deteksi-dini-kebakaran-49169-default-rtdb.firebaseio.com",
    'projectId': "deteksi-dini-kebakaran-49169",
    'storageBucket': "deteksi-dini-kebakaran-49169.appspot.com",
    'messagingSenderId': "425052406611",
    'appId': "1:425052406611:web:2ee87e25e4f03e0f45d7a6",
    'measurementId': "G-3B5YSH9D2P"
}


firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
beams_client = PushNotifications(
    instance_id='782baeab-3199-497a-8655-25c8ead1a917',
    secret_key='DF10D89EC16196B300EE835021971D9F88E3725667087AD2935062B2A88592FF',
)


def send_notification(title, body):
    response = beams_client.publish_to_interests(
        interests=['hello'],
        publish_body={
            'apns': {
                'aps': {
                    'alert': title
                }
            },
            'fcm': {
                'notification': {
                    'title': title,
                    'body': body
                }
            }
        }
    )
    print(response['publishId'])


def stream_handler_api(message):
    print(message)
    value = message['data']
    if value == True:
        api_kondisi = db.child("/Sensors/Sensor Api/Kondisi").get().val()
        while value:
            send_notification('Api Terdeteksi', 'Bahaya: KEBAKARAN!')
            time.sleep(1)  # Tunggu 1 detik
            value = db.child("/Sensors/Sensor Api/Value").get().val()


def stream_handler_gas(message):
    print(message)
    value = message['data']
    if value >= 300:
        gas_kondisi = db.child("/Sensors/Sensor Gas/Value").get().val()
        send_notification('Gas Berlebih Terdeteksi', f'Waspada : {gas_kondisi} PPM')


def stream_handler_suhu(message):
    print(message)
    value = message['data']
    if value >= 40:
        suhu_kondisi = db.child("/Sensors/Sensor Suhu/Value").get().val()
        send_notification('Suhu Tinggi Terdeteksi', f'Waspada : {suhu_kondisi}℃')


# Streaming Sensor Api
data_path_api = "/Sensors/Sensor Api/Value"
my_stream_api = db.child(data_path_api).stream(stream_handler_api, None)

# Streaming Sensor Gas
data_path_gas = "/Sensors/Sensor Gas/Value"
my_stream_gas = db.child(data_path_gas).stream(stream_handler_gas, None)

# Streaming Sensor Suhu
data_path_suhu = "/Sensors/Sensor Suhu/Value"
my_stream_suhu = db.child(data_path_suhu).stream(stream_handler_suhu, None)
