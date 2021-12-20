from loading import load

def count():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    load()

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
freq = 48000
duration = 5
import os
def sayname():
    count()
    print('DIGA O SEU NOME')
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=1)
    sd.wait()
    write("name0.wav", freq, recording)

    # Convert the NumPy array to audio file
    wv.write("name1.wav", recording, freq, sampwidth=2)
    os.replace("name0.wav", "rec/name0.wav")
    os.replace("name1.wav", "rec/name1.wav")

def sayfever():
    count()
    print('DIGA SE VOCÊ TEVE FEBRE? (SIM/NÃO)')
    recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=1)
    sd.wait()
    write("fever0.wav", freq, recording)

    # Convert the NumPy array to audio file
    wv.write("fever1.wav", recording, freq, sampwidth=2)
    os.replace("fever0.wav", "rec/fever0.wav")
    os.replace("fever1.wav", "rec/fever1.wav")

def sayheadache():
    count()
    print('DIGA SE VOCÊ TEVE DORES DE CABEÇA? (SIM/NÃO)')
    recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=1)
    sd.wait()
    write("headache0.wav", freq, recording)

    # Convert the NumPy array to audio file
    wv.write("headache1.wav", recording, freq, sampwidth=2)
    os.replace("headache0.wav", "rec/headache0.wav")
    os.replace("headache1.wav", "rec/headache1.wav")

def sayrednose():
    count()
    print('DIGA SE VOCÊ TEVE CORIZA? (SIM/NÃO)')
    recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=1)
    sd.wait()
    write("rednose0.wav", freq, recording)

    # Convert the NumPy array to audio file
    wv.write("rednose1.wav", recording, freq, sampwidth=1)
    os.replace("rednose0.wav", "rec/rednose0.wav")
    os.replace("rednose1.wav", "rec/rednose1.wav")



def measurements():
    import board
    import busio as io
    import adafruit_mlx90614
    import time
    import max30100
    from time import sleep
    
    mx30 = max30100.MAX30100()
    mx30.enable_spo2()
    mea = True
    tempTrigger = True
    bpmTrigger = True
    oxyTrigger = True
    while(mea):
        i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
        mlx = adafruit_mlx90614.MLX90614(i2c)
        while(tempTrigger):
            #ambientTemp = "{:.2f}".format(mlx.ambient_temperature)
            targetTemp = "{:.2f}".format(mlx.object_temperature)
            #print("Ambient Temperature:", ambientTemp, "°C")
            #print("Target Temperature:", targetTemp,"°C")
            if (float(targetTemp) > int(30)):
                global temperature
                temperature = 35.5 + (float(targetTemp)/100)*2
                tempTrigger = False
            else:
                tempTrigger = True
        while(bpmTrigger):
            mx30.read_sensor()
            mx30.ir, mx30.red
            hb = int(mx30.ir / 100)
            spo2 = int(mx30.red / 100)
            
            if mx30.ir != mx30.buffer_ir :
                #print("heart Rate:",hb);
                if (int(hb) > int(75)):
                    global bpm
                    bpm = int(hb)
                    bpmTrigger = False
                else:
                    bpmTrigger = True
            if mx30.red != mx30.buffer_red:
                #print("Blood Oxygen:",spo2);
                #print("-----------------------")
                if (int(spo2) > int(80)):
                    global oxy
                    oxy = 95 + ((int(spo2)/100) * 2)
                    oxyTrigger = False
                    mea = False
                else:
                    oxyTrigger = True
        
import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode (GPIO.BCM)
bot = 22
GPIO.setup (bot,GPIO.IN)
print("Seja bem-vindo à triagem")
print("Pressione o botão para iniciar")

while(1):
    if GPIO.input(bot) == 0:     
        print('Após o loading, diga o seu nome')
        sleep(5)
        sayname()
        print('Após o loading, responda a pergunta: VOCÊ TEVE FEBRE?')
        sleep(5)
        sayfever()
        print('Após o loading, responda a pergunta: VOCÊ TEVE DOR DE CABEÇA?')
        sleep(5)
        sayheadache()
        print('Após o loading, responda a pergunta: VOCÊ TEVE CORIZA?')
        sleep(5)
        sayrednose()
        print("Posicione os dedos indicadores nos dois sensores do totem.")
        sleep(5)
        measurements()
        print('Temperatura = ', temperature)
        print('Batimentos = ', bpm)
        print('Oxigenação = ', oxy)
        
        from pydub import AudioSegment
        sound = AudioSegment.from_wav("/home/ubuntu/trsf/v2/rec/name0.wav")
        sound = sound.set_channels(2)
        sound.export("/home/ubuntu/trsf/v2/rec/name0.wav", format="wav")

        sound = AudioSegment.from_wav("/home/ubuntu/trsf/v2/rec/fever0.wav")
        sound = sound.set_channels(2)
        sound.export("/home/ubuntu/trsf/v2/rec/fever0.wav", format="wav")

        sound = AudioSegment.from_wav("/home/ubuntu/trsf/v2/rec/headache0.wav")
        sound = sound.set_channels(2)
        sound.export("/home/ubuntu/trsf/v2/rec/headache0.wav", format="wav")

        sound = AudioSegment.from_wav("/home/ubuntu/trsf/v2/rec/rednose0.wav")
        sound = sound.set_channels(2)
        sound.export("/home/ubuntu/trsf/v2/rec/rednose0.wav", format="wav")

        import requests

        auth = True
        post = True

        if(auth):
            url = "https://adonis-backend-tcc.herokuapp.com/auth"
            data = {
                "username": "master",
                "password": "master"
            }
            x = requests.post(url, data=data)
            response = x.json()
            Token = response['token']
            # print(Token)


        if(post):
            url = "https://adonis-backend-tcc.herokuapp.com/posts/"
            data = {
                "name": "Felipe Silva",
                "temperature": temperature,
                "diagnostic": 1,
                "blood_oxygen": oxy,
                "heart_rate": bpm,
                "fever": 0,
                "headache": 1,
                "runny_nose": 0
                }
            
            headers = {"Authorization": "Bearer " + Token}
            x = requests.post(url, data=data, headers=headers)
            print(x)

        sleep(5)

