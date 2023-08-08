import pyrebase
from pusher_push_notifications import PushNotifications

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


def stream_handler(message):
    print(message)
    if(message['data'] == True):
      response = beams_client.publish_to_interests(
        interests=['hello'],
        publish_body={
          'apns': {
            'aps': {
              'alert': 'Hello!'
            }
          },
          'fcm': {
            'notification': {
              'title': 'Api Terdeteksi',
              'body': 'KEBAKARAN'
            }
          }
        }
      )

      print(response['publishId'])


data_path = "/Sensors/Sensor Api/Value"
my_stream = db.child(data_path).stream(stream_handler, None)
