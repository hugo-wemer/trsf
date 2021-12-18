def count():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    def tres():
        print('*******')
        print('     *')
        print('   **')
        print('     *')
        print('      *')
        print('      *')
        print('******')
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    def dois():
        print('  ****')
        print(' *   *')
        print('    *')
        print('   *')
        print('  *')
        print(' *')
        print(' ******')
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    def um():
        print('   *')
        print('  **')
        print(' * *')
        print('   *')
        print('   *')
        print('   *')
        print('*******')
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    tres()
    dois()
    um()

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
freq = 48000
duration = 5
    
def sayname():
    count()
    print('DIGA O SEU NOME')
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=1)
    sd.wait()
    write("name.wav", freq, recording)

    # Convert the NumPy array to audio file
     #wv.write("recording1.wav", recording, freq, sampwidth=2)

def sayfever():
    count()
    print('DIGA SE VOCÊ TEVE FEBRE? (SIM/NÃO)')
    recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=1)
    sd.wait()
    write("fever.wav", freq, recording)

    # Convert the NumPy array to audio file
    #wv.write("recording1.wav", recording, freq, sampwidth=2)

def sayheadache():
    count()
    print('DIGA SE VOCÊ TEVE DORES DE CABEÇA? (SIM/NÃO)')
    recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=1)
    sd.wait()
    write("headache.wav", freq, recording)

    # Convert the NumPy array to audio file
    #wv.write("recording1.wav", recording, freq, sampwidth=2)

def sayrednose():
    count()
    print('DIGA SE VOCÊ TEVE CORIZA? (SIM/NÃO)')
    recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=1)
    sd.wait()
    write("rednose.wav", freq, recording)

    # Convert the NumPy array to audio file
    #wv.write("recording1.wav", recording, freq, sampwidth=2)



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
        while(bpmTrigger & oxyTrigger):
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

#while(1):
#    if GPIO.input(bot) == 1:     
#        sleep(1)
#        if GPIO.input(bot) == 0:
#            print('Após a contagem, diga o seu nome')
#            sleep(2)
#            sayname()
#            print('Após a contagem, responda a pergunta: VOCÊ TEVE FEBRE?')
#            sleep(2)
#            sayfever()
#            print('Após a contagem, responda a pergunta: VOCÊ TEVE DOR DE CABEÇA?')
#            sleep(2)
#            sayheadache()
#            print('Após a contagem, responda a pergunta: VOCÊ TEVE CORIZA?')
#            sleep(2)
#            sayrednose()
#            print("Posicione os dedos indicadores nos dois sensores do totem.")
#            sleep(2)
#            measurements()
#            print('Temperatura = ',temperature, "°C")
#            print('Batimentos = ',bpm, "bpm")
#            print('Oxigenação = ',oxy, "%")
#while(1):
#    if GPIO.input(bot) == 1:     
#        print('Após a contagem, diga o seu nome')
#        sleep(2)
#        sayname()
#        print('Após a contagem, responda a pergunta: VOCÊ TEVE FEBRE?')
#        sleep(2)
#        sayfever()
#        print('Após a contagem, responda a pergunta: VOCÊ TEVE DOR DE CABEÇA?')
#        sleep(2)
#        sayheadache()
#        print('Após a contagem, responda a pergunta: VOCÊ TEVE CORIZA?')
#        sleep(2)
#        sayrednose()
#        print("Posicione os dedos indicadores nos dois sensores do totem.")
#        sleep(2)
#        measurements()
#        print('Temperatura = ',temperature, "°C")
#        print('Batimentos = ',bpm, "bpm")
#        print('Oxigenação = ',oxy, "%")
if GPIO.input(bot) == 1:     
    print('Após a contagem, diga o seu nome')
    sleep(2)
    sayname()
    print('Após a contagem, responda a pergunta: VOCÊ TEVE FEBRE?')
    sleep(2)
    sayfever()
    print('Após a contagem, responda a pergunta: VOCÊ TEVE DOR DE CABEÇA?')
    sleep(2)
    sayheadache()
    print('Após a contagem, responda a pergunta: VOCÊ TEVE CORIZA?')
    sleep(2)
    sayrednose()
    print("Posicione os dedos indicadores nos dois sensores do totem.")
    sleep(2)
    measurements()
    print('Temperatura = ',temperature, "°C")
    print('Batimentos = ',bpm, "bpm")
    print('Oxigenação = ',oxy, "%")
      
