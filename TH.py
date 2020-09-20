import Adafruit_DHT
from datetime import datetime
from firebase import firebase
from time import sleep

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio=4

# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

# firebase
firebase = firebase.FirebaseApplication('https://raspberrypi-test-2b184.firebaseio.com/')

# time
now = datetime.now()

# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.
def update_firebase() :
  
  humidity, temperature = Adafruit_DHT.read_retry(sensor,gpio)
  if humidity is not None and temperature is not None:
    sleep(10)
    str_temp = '{0:0.2f} *C '.format(temperature)
    str_hum = ' {0:0.2f} %'.format(humidity)
    nowDateTime = now.strftime('%Y-%m-%d %H:%M:%S')
    # print ("%s/%s/%s %s:%s" %(now.year, now.month, now.day, now.hour, now.minute))
    print(nowDateTime,'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
  else:
    print('Failed to get reading. Try again!')
    sleep(10)
    
  data = {"time": nowDateTime ,"temperature": temperature, "humidity" : humidity}
  firebase.post('/sensor/dht', data)

while True:
  update_firebase()

  #sleepTime = int(sleepTime)
  sleep(10)
