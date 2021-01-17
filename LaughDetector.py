import gpiozero
import os
import RPi.GPIO as GPIO
import time
import random
import board
import adafruit_dht


def main():
    beginJoke = False
    jokeBank = []
    jokeBank = readJokeBank()
    while(True):
        GPIO.cleanup()
        speakbot(
            "Welcome to the laugh detector. Press the button once for a joke. or twice to exit")
        beginJoke = buttonInput()
        if(beginJoke):

            beforeJokeBPM = 0
            afterJokeBPM = 0

            speakbot("Place your finger on the heartbeat sensor!")
            time.sleep(1.5)
            print("==================")
            beforeJokeBPM = heartAnalyzer()
            print("Before joke: ", beforeJokeBPM)
            speakbot(jokeSelector(rngGrabber(), jokeBank))
            afterJokeBPM = heartAnalyzer()
            print("After joke: ", afterJokeBPM)
            reactionValue = beatDifference(beforeJokeBPM, afterJokeBPM)
            reactionStr = str(reactionValue)  # converting float to string
            speakbotReaction(reactionStr)

# calculates the heartbeat rate difference in percentage form
def beatDifference(before, after):
    diff = after - before
    percent = (diff/before) * 100
    print(percent, "%")
    return percent


def rngGrabber():  # calculates RNG value with the output of the humidity/temperature sensor
    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT11(board.D18)
    # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
    # This may be necessary on a Linux single board computer like the Raspberry Pi,
    # but it will not work in CircuitPython.
    # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
    validInput = True
    while (validInput):
        try:
            # Print the values to the serial port
            num1 = random.randrange(1000)
            num2 = random.randrange(100)
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            validInput = False
            # print(
            #     "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
            #         temperature_f, temperature_c, humidity
            #     )
            # )
            dhtDevice.exit()
            return (((temperature_f + humidity) * num1) + num2) 
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        time.sleep(2.0)

# selects a joke from our jokebank text file separated by new line
def jokeSelector(rngNum, JokeBank):
    # dynamically changes according to the size of the jokebank
    rngNum %= len(JokeBank)
    return JokeBank[int(rngNum)]


def readJokeBank():  # reads joke bank
    JokeBank = []
    jokeFile = open('JokeBank.txt')
    JokeBank = jokeFile.read().splitlines()
    jokeFile.close()
    return JokeBank


def heartAnalyzer():  # records heartrate and adds the change of signal to monitor change of heartrate
    hr = gpiozero.MCP3008(channel=1)
    print("start")
    counter = 0
    prevBeat = .748  # idling value is around .748
    diffBeat = 0
    currentSpike = 0
    while True:
        counter = counter+1
        diffBeat = prevBeat - hr.value
        prevBeat = hr.value  # prevBeat gets rewritten by current value here
        if (counter <= 5000):
            currentSpike = currentSpike + abs(diffBeat)
        else:
            counter = 0
            print("end")
            return currentSpike


def speakbot(speak):  # accepts strings and reads it aloud
    os.popen('espeak -s155 "' + speak +
             '" --stdout | aplay 2> /dev/null').read()


def speakbotReaction(percent):  # reacts to the percentage of change of heartrate
    formatted = '{:.2f}'.format(float(percent))
    # print(formatted)
    os.popen('espeak -s155 "' + "Your heartrate changed by " +
             str(formatted) + "%" + '" --stdout | aplay 2> /dev/null').read()


def buttonInput():  # listens for button press event. either 1 press for jokes to start, or 2 presses to exit to the program
    GPIO.setmode(GPIO.BCM)
    # The input pin of the Sensor will be declared. Additional to that the pull-up resistor will be activated.
    GPIO_PIN = 24
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # At the moment of detecting a Signal ( falling signal edge ) the output function will be activated.
    GPIO.add_event_detect(GPIO_PIN, GPIO.RISING)
    if GPIO.event_detected(GPIO_PIN):
        print('Buttone pressed')
    max_time = 1
    # main program loop
    try:
        while True:
            time.sleep(0.001)
            if GPIO.event_detected(GPIO_PIN):
                when_pressed = time.time()
                while time.time() - when_pressed < max_time:
                    time.sleep(0.001)
                    if GPIO.event_detected(GPIO_PIN):
                        time.sleep(0.5)
                        speakbot(
                            "Self destruct sequence activated. 5. 4. 3. 2. 1. Goodbye. ")
                        print('Thank you for hearing our Joke :)')
                        exit()
                print('button pressed once')
                return True

    # Scavenging work after the end of the program
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
