# laughDetector
Fall 2020 CS530 Project for SDSU

1 minute demo: https://youtu.be/D3CDYXAGYII
Presentation: https://youtu.be/V-3oDYuGfxI

Files: 
1. JokeBank.txt - This file contains the jokes, which are saved into an array for later use. Each joke is separated by a new line. These jokes are outputted for the user to hear via the text to speech feature.

2. main.py - inside LaughDetector contains these functions:

main()
This function calls all the functions within the source code, and keeps running until the button is pressed twice to exit the program. If the button is pressed once, it will keep reading out a joke to the user and outputting the difference in heart rate.

beatDifference(before, after)
This function calculates the heart rate difference in percentage form. It takes the output data from the heartbeat sensor before and after the joke is told in order to measure the reaction difference.  
- Parameter: 
before: integer that represents change of heart rate before joke.
after: integer that represents change of heart rate after joke.
- Returns: 
Integer which represents the difference of heart rate in percentage form 

rngGrabber()
This function grabs the values from the humidity/temperature sensor and adds the humidity and temperature values together. 
- Parameter: 
None
- Returns: 
Integer which is a random value

jokeSelector(rngNum, JokeBank)
The jokeSelector function will take in the outputs from our humidifier sensor, and select a joke based on our JokeBank. Randomly picks a joke from our jokebank text file separated by new line
- Parameter: 
rngNum: integer.
JokeBank: array of strings.
- Returns: joke for user as a String (will be outputted as text to voice through speakers)

readJokeBank()
This function reads JokeBank.txt file and puts all the jokes into an array which are separated by a new line.
- Parameter:
None
- Returns:
Array of strings called JokeBank

heartAnalyzer()
This function records the heart rate and adds the change of signal to monitor change of heart rate.
- Parameter:
None
- Returns:
An integer that represents the total change in heart rate

speakbot(speak)
This function accepts strings and reads a joke out loud using eSpeak text-to-speech
- Parameter:
speak: string to be read out loud
- Returns:
None

speakbotReaction(percent):
This function reacts to the percentage of change of heart rate and reads out loud the difference using eSpeak
- Parameter:
percent: string that represents the change of heart rate in a percentage form
- Returns:
None

buttonInput()
This function listens for a button press event. Either 1 press for a joke to start, or 2 presses to exit to the program.
- Parameter:
None
- Returns:
Boolean. True when the button is pressed once. False when the button is pressed twice.

Instructions for user: 
1) Add all source code files into the same directory. Download all necessary dependencies and libraries. Make sure all circuits are correct.
2) Put all files in the same directory: 
- LaughDetector.py
- JokeBank.txt
3) Initiate laugh detector with the following command within the directory with all files:
python3 LaughDetector.py
4) Press the button once to enter the joke sequence. Press the button twice to exit the program.
- If the button was pressed once, the bot will ask the user to place a finger on the heartbeat sensor, tell a joke, and will calculate heart rate difference. Once the heart rate change is read out loud, it will start over and await for one button press or two button presses again.
- If the button was pressed twice, the bot will exit the program.
