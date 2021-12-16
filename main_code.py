def measurements():
    import board
    import busio as io
    import adafruit_mlx90614
    import time
    import max30100
    from time import sleep
    
    mx30 = max30100.MAX30100()
    mx30.enable_spo2()
          
    while(1):
        i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
        mlx = adafruit_mlx90614.MLX90614(i2c)

        ambientTemp = "{:.2f}".format(mlx.ambient_temperature)
        targetTemp = "{:.2f}".format(mlx.object_temperature)

        sleep(1)

        print("Ambient Temperature:", ambientTemp, "°C")
        print("Target Temperature:", targetTemp,"°C")
      
        mx30.read_sensor()
        mx30.ir, mx30.red

        hb = int(mx30.ir / 100)
        spo2 = int(mx30.red / 100)
        
        if mx30.ir != mx30.buffer_ir :
            print("heart Rate:",hb);
        if mx30.red != mx30.buffer_red:
            print("Blood Oxygen:",spo2);
            print("-----------------------")

import RPi.GPIO as GPIO
#GPIO.setmode (GPIO.BOARD)
GPIO.setmode (GPIO.BCM)
#bot = 15
bot = 22
GPIO.setup (bot,GPIO.IN)

print("Seja bem-vindo à triagem")
print("Pressione o botão para iniciar")

while(1):
  
    if GPIO.input(bot) ==1:
        
      measurements()
