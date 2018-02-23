# copyright Isaac Wellish


import audiobusio
import board
import array
import math
import time
from digitalio import DigitalInOut, Direction, Pull
import audioio
import neopixel




pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0,0,0))
pixels.show()


def tones(tone_number):

 
    # set up time signature
    whole_note = 1.5  # adjust this to change tempo of everything

 
    # set up note values
    Ab3 = 208
    A3 = 220
    As3 = 233
    Bb3 = 233
    B3 = 247
    C4 = 262
    Cs3 = 277
    Db4 = 277
    D4 = 294
    Ds3 = 311
    Eb4 = 311
    E4 = 330
    F4 = 349
    Fs3 = 370
    Gb4 = 370
    G4 = 392
    Gs4 = 415


#button code

buttonD = DigitalInOut(board.BUTTON_A)
buttonD.direction = Direction.INPUT
buttonD.pull = Pull.DOWN

buttonU = DigitalInOut(board.BUTTON_B)
buttonU.direction = Direction.INPUT
buttonU.pull = Pull.DOWN
 




#magnitude calculations

NUM_SAMPLES = 160

# Prep a buffer to record into
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, frequency=16000, bit_depth=16)
samples = array.array('H', [0] * NUM_SAMPLES)
mic.record(samples, len(samples))


# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))
 
# Scale input_value to be between output_min and output_max, in an exponential way.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / (input_max - input_min)
    return output_min + math.pow(normalized_input_value, SCALE_EXPONENT) * (output_max - output_min)
 
# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    return math.sqrt(sum(float((sample-minbuf)*(sample-minbuf)) for sample in values)/len(values))
 
def mean(values):
    return (sum(values) / len(values))

input_floor = normalized_rms(samples) + 10

input_ceiling = input_floor + 500

NUM_PIXELS = 10

CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE*-0.1)
 
PEAK_COLOR = (100, 0, 255)

FREQUENCY = 440    # 440 Hz middle 'A'
SAMPLERATE = 8000  # 8000 samples/second, recommended!

length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
# for i in range(length):
#     sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)
 
# enable the speaker
spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = Direction.OUTPUT
spkrenable.value = True

sample = audioio.AudioOut(board.SPEAKER, sine_wave)

sample.frequency = SAMPLERATE





counter = 0



while True:





   



    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print("mag = ",magnitude)
    print("freq = ",mic.frequency)


    if buttonU.value == True:  # button is pushed then 
        pixels.fill((0,0,0))
        counter += 1
        time.sleep(0.2)
    elif buttonD.value == True:
        pixels.fill((0,0,0))
        counter -= 1
        time.sleep(0.2)


    print("Counter = ",counter)

    
    if counter == 0: #Ab
        pixels[9] = (0,0,255)
        FREQUENCY = 208
    elif counter == 1: #A
        pixels[9] = (0,255,0)
        FREQUENCY = 223
    elif counter == 2: #A#
        pixels[9] = (255,0,0)
        FREQUENCY = 233
    elif counter == 3: #Bb
        pixels[0] = (0,0,255)
        FREQUENCY = 233
    elif counter == 4: #B
        pixels[0] = (0,255,0)
        FREQUENCY = 247
    elif counter == 5: #C
        pixels[1] = (0,255,0)
        FREQUENCY = 262
    elif counter == 6: #C#
        pixels[1] = (255,0,0)
        FREQUENCY = 277
    elif counter == 7: #Db
        pixels[2] = (0,0,255)
        FREQUENCY = 277
    elif counter == 8: #D
        pixels[2] = (0,255,0)
        FREQUENCY = 294
    elif counter == 9:# D#
        pixels[2] = (255,0,0)
        FREQUENCY = 311
    elif counter == 10: #Eb
        pixels[3] = (0,0,255)
        FREQUENCY = 311
    elif counter == 11: #E
        pixels[3] = (0,255,0)
        FREQUENCY = 330
    elif counter == 12: #F
        pixels[4] = (0,255,0)
        FREQUENCY = 349
    elif counter == 13: #F#
        pixels[4] = (255,0,0)
        FREQUENCY = 370
    elif counter == 14: #Gb
        pixels[5] = (0,0,255)
        FREQUENCY = 370
    elif counter == 15: #G
        pixels[5] = (0,255,0)
        FREQUENCY = 392
    elif counter == 16: #G#
        pixels[5] = (255,0,0)
        FREQUENCY = 415
    elif counter > 16: #if counter goes above 16 set back to 0
        counter = 0
    elif counter < 0: #if counter goes below 0 set back to 16
        counter = 16;


    if magnitude > 5000:
        print(FREQUENCY)
        length = SAMPLERATE // FREQUENCY
        sine_wave = array.array("H", [0] * length)
        for i in range(length):
            sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)
        sample = audioio.AudioOut(board.SPEAKER, sine_wave)
        sample.frequency = SAMPLERATE
        sample.play(loop=True)  # keep playing the sample over and over
        time.sleep(1)           # until...
        sample.stop()           # we tell the board to stop 
    
    pixels.show()


 
   






