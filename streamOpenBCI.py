    # -*- coding: utf-8 -*-
"""
Script for the online streaming, pre-processing, and analysis of EEG from OpenBCI 

"""
import libmushu
from wyrm import processing as proc 
from wyrm import io 
from wyrm.types import RingBuffer 
import time
import numpy
import scipy
from Quartz.CoreGraphics import CGEventCreateKeyboardEvent
from Quartz.CoreGraphics import CGEventPost
import os

# Python releases things automatically, using CFRelease will result in a scary error
#from Quartz.CoreGraphics import CFRelease

from Quartz.CoreGraphics import kCGHIDEventTap

# From http://stackoverflow.com/questions/281133/controlling-the-mouse-from-python-in-os-x
# and from https://developer.apple.com/library/mac/documentation/Carbon/Reference/QuartzEventServicesRef/index.html#//apple_ref/c/func/CGEventCreateKeyboardEvent


''' 
1) First, open cmd window and then cd into /Users/salman.qasim/anaconda/pkgs/OpenBCI_Python-master
2) python user.py -p=/dev/tty.usbserial-DJ00IWYI --add streamer_lsl
3) /start
4) execute code below 

'''

def KeyTap(k):
    KeyDown(k)
    KeyUp(k)


def KeyDown(k):
    keyCode, shiftKey = toKeyCode(k)

    time.sleep(0.0001)

    if shiftKey:
        CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 0x38, True))
        time.sleep(0.0001)

    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keyCode, True))
    time.sleep(0.0001)

    if shiftKey:
        CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 0x38, False))
        time.sleep(0.0001)

def KeyUp(k):
    keyCode, shiftKey = toKeyCode(k)

    time.sleep(0.0001)

    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keyCode, False))
    time.sleep(0.0001)

def KeyPress(k):
    keyCode, shiftKey = toKeyCode(k)

    time.sleep(0.0001)

    if shiftKey:
        CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 0x38, True))
        time.sleep(0.0001)

    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keyCode, True))
    time.sleep(0.0001)

    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keyCode, False))
    time.sleep(0.0001)

    if shiftKey:
        CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 0x38, False))
        time.sleep(0.0001)



# From http://stackoverflow.com/questions/3202629/where-can-i-find-a-list-of-mac-virtual-key-codes

def toKeyCode(c):
    shiftKey = False
    # Letter
    if c.isalpha():
        if not c.islower():
            shiftKey = True
            c = c.lower()

    if c in shiftChars:
        shiftKey = True
        c = shiftChars[c]
    if c in keyCodeMap:
        keyCode = keyCodeMap[c]
    else:
        keyCode = ord(c)
    return keyCode, shiftKey

shiftChars = {
    '~': '`',
    '!': '1',
    '@': '2',
    '#': '3',
    '$': '4',
    '%': '5',
    '^': '6',
    '&': '7',
    '*': '8',
    '(': '9',
    ')': '0',
    '_': '-',
    '+': '=',
    '{': '[',
    '}': ']',
    '|': '\\',
    ':': ';',
    '"': '\'',
    '<': ',',
    '>': '.',
    '?': '/'
}


keyCodeMap = {
    'a'                 : 0x00,
    's'                 : 0x01,
    'd'                 : 0x02,
    'f'                 : 0x03,
    'h'                 : 0x04,
    'g'                 : 0x05,
    'z'                 : 0x06,
    'x'                 : 0x07,
    'c'                 : 0x08,
    'v'                 : 0x09,
    'b'                 : 0x0B,
    'q'                 : 0x0C,
    'w'                 : 0x0D,
    'e'                 : 0x0E,
    'r'                 : 0x0F,
    'y'                 : 0x10,
    't'                 : 0x11,
    '1'                 : 0x12,
    '2'                 : 0x13,
    '3'                 : 0x14,
    '4'                 : 0x15,
    '6'                 : 0x16,
    '5'                 : 0x17,
    '='                 : 0x18,
    '9'                 : 0x19,
    '7'                 : 0x1A,
    '-'                 : 0x1B,
    '8'                 : 0x1C,
    '0'                 : 0x1D,
    ']'                 : 0x1E,
    'o'                 : 0x1F,
    'u'                 : 0x20,
    '['                 : 0x21,
    'i'                 : 0x22,
    'p'                 : 0x23,
    'l'                 : 0x25,
    'j'                 : 0x26,
    '\''                : 0x27,
    'k'                 : 0x28,
    ';'                 : 0x29,
    '\\'                : 0x2A,
    ','                 : 0x2B,
    '/'                 : 0x2C,
    'n'                 : 0x2D,
    'm'                 : 0x2E,
    '.'                 : 0x2F,
    '`'                 : 0x32,
    'k.'                : 0x41,
    'k*'                : 0x43,
    'k+'                : 0x45,
    'kclear'            : 0x47,
    'k/'                : 0x4B,
    'k\n'               : 0x4C,
    'k-'                : 0x4E,
    'k='                : 0x51,
    'k0'                : 0x52,
    'k1'                : 0x53,
    'k2'                : 0x54,
    'k3'                : 0x55,
    'k4'                : 0x56,
    'k5'                : 0x57,
    'k6'                : 0x58,
    'k7'                : 0x59,
    'k8'                : 0x5B,
    'k9'                : 0x5C,

    # keycodes for keys that are independent of keyboard layout
    '\n'                : 0x24,
    '\t'                : 0x30,
    ' '                 : 0x31,
    'del'               : 0x33,
    'delete'            : 0x33,
    'esc'               : 0x35,
    'escape'            : 0x35,
    'cmd'               : 0x37,
    'command'           : 0x37,
    'shift'             : 0x38,
    'caps lock'         : 0x39,
    'option'            : 0x3A,
    'ctrl'              : 0x3B,
    'control'           : 0x3B,
    'right shift'       : 0x3C,
    'rshift'            : 0x3C,
    'right option'      : 0x3D,
    'roption'           : 0x3D,
    'right control'     : 0x3E,
    'rcontrol'          : 0x3E,
    'fun'               : 0x3F,
    'function'          : 0x3F,
    'f17'               : 0x40,
    'volume up'         : 0x48,
    'volume down'       : 0x49,
    'mute'              : 0x4A,
    'f18'               : 0x4F,
    'f19'               : 0x50,
    'f20'               : 0x5A,
    'f5'                : 0x60,
    'f6'                : 0x61,
    'f7'                : 0x62,
    'f3'                : 0x63,
    'f8'                : 0x64,
    'f9'                : 0x65,
    'f11'               : 0x67,
    'f13'               : 0x69,
    'f16'               : 0x6A,
    'f14'               : 0x6B,
    'f10'               : 0x6D,
    'f12'               : 0x6F,
    'f15'               : 0x71,
    'help'              : 0x72,
    'home'              : 0x73,
    'pgup'              : 0x74,
    'page up'           : 0x74,
    'forward delete'    : 0x75,
    'f4'                : 0x76,
    'end'               : 0x77,
    'f2'                : 0x78,
    'page down'         : 0x79,
    'pgdn'              : 0x79,
    'f1'                : 0x7A,
    'left'              : 0x7B,
    'right'             : 0x7C,
    'down'              : 0x7D,
    'up'                : 0x7E
}

def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]



#---- Find the amplifier 

# will be using labstreaminglayer for this 

available_amps = libmushu.get_available_amps()

ampname = available_amps[3]
amp = libmushu.get_amp(ampname)

# configure the amplifier (may have to do some kind of blockconfig given the downsampling I intend to do)
amp.configure()
amp_fs, aux_fs = amp.get_sampling_frequency() # standard for openBci should be ~ 256 Hz 

amp_channels = ['Ch0', 'Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch6', 'Ch7'] #amp.get_channels() # should be 17 of them 
aux_channels = ['Ch13', 'Ch14', 'Ch15']
Fp1 = 0
Fp2 = 1
emg_chan = 3
accel_chan = 0
n_channels = len(amp_channels)
n_aux = len(aux_channels)
#---- Detail the channel information - which channel is which? 

# -----------------TODO ---------------

#---- Initialize filter characteristics 

fn = amp_fs / 2 # Nyquist 
# Get filter coefficients 
b_band, a_band = proc.signal.butter(5,[2/fn, 40/fn],btype='band')
#b_high, a_high = proc.signal.butter(5,[1/fn],btype = 'high')
zi_band = proc.lfilter_zi(b_band,a_band,n_channels)
zi_aux = proc.lfilter_zi(b_band, a_band, n_aux) # only for the EMG filtering
#zi_high = proc.lfilter_zi(b_high,a_high,n_channels)

#---- Start the amplifier data stream 
streamed_data = numpy.empty([1,8]) # initialize datastream array 
streamed_aux = numpy.empty([1,3]) 
time_of_data = numpy.empty([1,1])
amp.start()
start = time.time()   
sample_num = 0 
# setup ring buffer 
rb = RingBuffer(1000) # set this up so we always have the last 1000 ms of data 
tick = 0
baseline = 0
while True:
    sample_num += 1 
    delta = time.time() - start  
    data, auxdata = amp.get_data() #, triger
    trigger = (time.time()-start,'fuck') # gets raletive time stamp
    cnt = io.convert_mushu_data(data,trigger, amp_fs, amp_channels) # convert to wyrm format 
    aux_cnt =io.convert_mushu_data(auxdata,trigger,aux_fs,aux_channels)
    #cnt.data = proc.rectify_channels(cnt.data)
    cnt, zi_band = proc.lfilter(cnt, b_band, a_band, zi = zi_band) # lowpass the data  
    aux_cnt, zi_aux = proc.lfilter(aux_cnt, b_band, a_band, zi = zi_aux)
    #cnt, zi_low = proc.lfilter(cnt, b_high, a_high, zi = zi_high) # highpass 
#        # don't worry about subsampling necessarily 
    newsamples = cnt.data.shape[1] 
    streamed_data = numpy.concatenate((streamed_data, cnt.data), axis=0)
    streamed_aux = numpy.concatenate((streamed_aux, aux_cnt.data), axis =0)
    if delta > 30 and delta <32.5: # 60 seconds have passed
        # establish a baseline amplitude for each channel 
        amplitude_baseline = numpy.median(streamed_data, axis=0) # uses the median to decrease the effect of outliers 
        amplitude_threshold = 4*amplitude_baseline     
        aux_threshold = numpy.median(streamed_aux, axis = 0)
        # calculate the alpha power as well 
        alpha_baseline =[]
        for i in range(n_channels):
            freqs, Pxx = scipy.signal.welch(streamed_data[:,i],fs = amp_fs)
            lowerbound = indices(freqs, lambda x: x>7)
            lowerbound = lowerbound[0]
            upperbound = indices(freqs, lambda x: x>12)
            upperbound = upperbound[0]
            alpha_baseline.append(numpy.mean(Pxx[lowerbound:upperbound])) # make sure the dimensions on this are ok 
        alpha_baseline = numpy.array([alpha_baseline])
        alpha_baseline =  alpha_baseline * 3

        emg_threshold_left = 2.5 * amplitude_baseline[emg_chan] 
        emg_threshold_right = 5 * amplitude_baseline[emg_chan]
        # get the baseline for theta power and beta power in emg 
#        freq_emg, Pemg = scipy.signal.welch(streamed_data[:,emg_chan],aux_fs)
#        lowerbound1 = indices(freqs, lambda x: x>3)
#        lowerbound1 = lowerbound1[0]
#        upperbound1 = indices(freqs, lambda x: x>8)
#        upperbound1 = upperbound1[0]
#        lowerbound2 = indices(freqs, lambda x: x>13)
#        lowerbound2 = lowerbound2[0]
#        upperbound2 = indices(freqs, lambda x: x>29)
#        upperbound2 = upperbound2[0]
#        theta_emg_threshold = numpy.mean(Pxx[lowerbound1:upperbound1])
#        beta_emg_threshold = numpy.mean(Pxx[lowerbound2:upperbound2])
#
#        theta_emg_threshold = theta_emg_threshold * 2 
#        beta_emg_threshold = beta_emg_threshold * 2
        
        baseline = 1
        os.system('say "baseline period is over, get ready!"')
        end_baseline = time.time() 
         # to make sure it only does this shit once 
    else:
        continue
    end_baseline = time.time() 
    winAdvance = 20.0
    winLen = 400.0
    if baseline==1: # indicating that baseline has occured
        time.sleep(winLen/1000)
    post_baseline = time.time()- end_baseline
    T = winLen/1000
    if post_baseline > T: # run the first window 
        # initiate analysis 
        analysis_end = streamed_data.shape[0]
        analysis_begin = int(streamed_data.shape[0] - (amp_fs*winLen/1000))
        data_windowed = streamed_data[analysis_begin:analysis_end,:]
        aux_windowed = streamed_aux[analysis_begin:analysis_end,:]
        amplitude_window= numpy.median(data_windowed, axis=0) # uses the median to decrease the effect of outliers 
        aux_amplitude_window = numpy.median(aux_windowed, axis = 0)
        
        # analysis: mean amplitude over the window, alpha power over the window =
#        freq_emg, Pemg = scipy.signal.welch(data_windowed[:,emg_chan],aux_fs)
#        lowerbound1 = indices(freqs, lambda x: x>3)
#        lowerbound1 = lowerbound1[0]
#        upperbound1 = indices(freqs, lambda x: x>8)
#        upperbound1 = upperbound1[0]
#        lowerbound2 = indices(freqs, lambda x: x>13)
#        lowerbound2 = lowerbound2[0]
#        upperbound2 = indices(freqs, lambda x: x>29)
#        upperbound2 = upperbound2[0]
#        
#        theta_emg_window = numpy.mean(Pxx[lowerbound1:upperbound1])
#        beta_emg_window = numpy.mean(Pxx[lowerbound2:upperbound2])
        
        # Check which behavioral condition is true
        
        #EYEBLINK CONDN 
        if numpy.abs(amplitude_window[Fp1]) > numpy.abs(amplitude_threshold[Fp1]) or numpy.abs(amplitude_window[Fp2]) > numpy.abs(amplitude_threshold[Fp2]):
            time.sleep(.001)
            KeyDown('j')
            
            # control: if held down for too long, just keyup
        else:
            time.sleep(.001)
            KeyUp('j')

        # EMG CONDN
        
        if numpy.abs(amplitude_window[emg_chan])> numpy.abs(emg_threshold_left):
            time.sleep(.001)
            KeyDown('a')
        else:
            time.sleep(.001)
            KeyUp('a') 

        if numpy.abs(amplitude_window[emg_chan])> numpy.abs(emg_threshold_right):
            time.sleep(.001)
            KeyDown('d')
        else:
            time.sleep(.001)
            KeyUp('d')
        
        if tick!= 1 and (numpy.abs(aux_amplitude_window[accel_chan]) >  numpy.abs(aux_threshold[accel_chan])): # make sure to set this threshold fairly high
            time.sleep(.001)
            KeyDown('w')
            tick = 1
        elif tick== 1 and numpy.abs((aux_amplitude_window[accel_chan]) >  numpy.abs(aux_threshold[accel_chan])):
            time.sleep(.001)
            KeyUp('w')
            tick = 0
       
        alpha_window = []
        
        for i in range(n_channels):
            freqs, Pxx = scipy.signal.welch(data_windowed[:,i],fs = amp_fs)
            lowerbound3 = indices(freqs, lambda x: x>7)
            lowerbound3 = lowerbound3[0]
            upperbound3 = indices(freqs, lambda x: x>12)
            upperbound3 = upperbound3[0]
            alpha_window.append(numpy.mean(Pxx[lowerbound3:upperbound3]))

        compare = (numpy.array([alpha_window]) >  alpha_baseline)
        if compare.any(): # i can specify a channel here if that helps 
            # SEND KEY COMMAND TO QUIT
            time.sleep(.1)
            KeyDown('g')
        else:
            time.sleep(winAdvance/1000) # put this mofo to sleep for 50 ms

    if delta>60*20:
        break

end = time.time()
amp.stop()





