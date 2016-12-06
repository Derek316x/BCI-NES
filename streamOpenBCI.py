    # -*- coding: utf-8 -*-
"""
Script for the online streaming, pre-processing, and analysis of EEG from OpenBCI 

"""
import libmushu
from wyrm import processing as proc 
from wyrm import io 
from wyrm.types import BlockBuffer 
import time
import numpy
import scipy
from scipy import signal 
from Quartz.CoreGraphics import CGEventCreateKeyboardEvent
from Quartz.CoreGraphics import CGEventPost
import os
import time
import matplotlib
from matplotlib import pyplot as plt

# Python releases things automatically, using CFRelease will result in a scary error
#from Quartz.CoreGraphics import CFRelease

from Quartz.CoreGraphics import kCGHIDEventTap

# From http://stackoverflow.com/questions/281133/controlling-the-mouse-from-python-in-os-x
# and from https://developer.apple.com/library/mac/documentation/Carbon/Reference/QuartzEventServicesRef/index.html#//apple_ref/c/func/CGEventCreateKeyboardEvent


''' 
1) First, open cmd window and then cd into /Users/salman.qasim/anaconda/pkgs/OpenBCI_Python-master
2) python user.py -p=/dev/tty.usbserial-DQ0084AI --add streamer_lsl
3) /start
4) execute code below 
5) remember to change port in ampdecorator.py

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

# -----------------TODO ---------------
# alter this depending on our cap, or better yet generalize it. 

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
b_band, a_band = signal.butter(4, [4/fn, 50/fn], 'bandpass')
#b_band, a_band = proc.signal.butter(5,[5/fn, 40/fn],btype='band')
#b_high, a_high = proc.signal.butter(5,[1/fn],btype = 'high')
zi_band = proc.lfilter_zi(b_band,a_band,n_channels)
zi_aux = proc.lfilter_zi(b_band, a_band, n_aux) # only for the EMG filtering
#zi_high = proc.lfilter_zi(b_high,a_high,n_channels)

#---- Start the amplifier data stream 
streamed_raw = numpy.empty([1,8]) # initialize datastream array 
streamed_spect = numpy.empty([1,8])
#streamed_aux = numpy.empty([1,3]) 
time_of_data = numpy.empty([1,1])
amp.start()
start = time.time()   
sample_num = 0 
# setup block buffer 
# -----------------TODO ---------------
# Set this up to work properly: have to use this to filter the data in real time 
#bb = BlockBuffer(100) # set this up so we always have the last 1000 ms of data 

tick = 0
baseline = 0

## Setup the plot the of the spectrogram? 
# fig, ax = plt.subplots()
# ax.axis([0, 100, 0, 1])
#
# y = numpy.random.rand(100)
# lines = ax.plot(y)
#
# fig.canvas.manager.show() 
left_accuracy =[1]
right_accuracy = [1]
    
left_emg_chan = 3 # 4 -1
right_emg_chan = 4 # 5-1 
    
left_beta_window = []

right_beta_window = []

# Collect data for ITR 
left_decision = [1] 
right_decision = [1]    
left_action = [1] 
right_action = [1]

i=0
while True:
    sample_num += 1  # number of data acquisitions 
    delta = time.time() - start  
    data, auxdata = amp.get_data() # get the data 
    trigger = (time.time()-start,'trigger') # gets relative time stamp, can serve as a psuedo marker
    cnt = io.convert_mushu_data(data,trigger, amp_fs, amp_channels) # convert to wyrm format
    #cnt, zi_band = proc.lfilter(cnt, b_band, a_band, zi = zi_band) # bandpass the data  
    #aux_cnt, zi_aux = proc.lfilter(aux_cnt, b_band, a_band, zi = zi_aux)
    #cnt, zi_low = proc.lfilter(cnt, b_high, a_high, zi = zi_high) # highpass 

        # don't worry about subsampling necessarily 
    #cnt = proc.subsample(cnt,100) # subsamples the data from 240 Hz to 50 Hz
    streamed_raw = numpy.concatenate((streamed_raw, cnt.data), axis=0) # buffer the streaming data 

    #cnt_log_spectrum = proc.logarithm(cnt_spectrum) # this is the logged spectrum 
#    bb.append(cnt)
 #   cnt = bb.get()
        #aux_cnt =io.convert_mushu_data(auxdata,trigger,aux_fs,aux_channels)
    #cnt.data = proc.rectify_channels(cnt.data)

    #cnt_spectrum = proc.spectrum(cnt)
    #frequencies = cnt_spectrum.axes


    #streamed_spect = numpy.concatenate((streamed_spect,cnt_spectrum.data),axis=0)
    #streamed_aux = numpy.concatenate((streamed_aux, aux_cnt.data), axis =0)
    
# First ,let's estabish some person specific baselines in a 30 second period     


    # One of the problems we have here is big deflections of the signal in the first ~10 sec

    
    
    if delta > 30 and delta <32.5: # 30 seconds have passed
        # establish a baseline amplitude for each channel 
        streamed_raw = streamed_raw[2500:,:]
        #aux_threshold = 10*numpy.median(streamed_aux, axis = 0)
        # calculate the beta power as well 
        left_beta_baseline =[]
        right_beta_baseline =[]
        
        # bandpass the data 
        streamed_filt = signal.filtfilt(b_band, a_band, streamed_raw, axis = 0)
        amplitude_baseline = numpy.median(streamed_filt, axis=0) # uses the median to decrease the effect of outliers 
        amplitude_threshold = 5*amplitude_baseline   # may be good for checking ITR  

        
        freqs, left_Pxx = scipy.signal.welch(streamed_filt[:,1],fs = amp_fs) # i = 1 = channel 2 on the openBCI 
        freqs, right_Pxx = scipy.signal.welch(streamed_filt[:,6],fs = amp_fs) # i = 6 = channel 7 on the openBCI             
        lowerbound = indices(freqs, lambda x: x>13)
        lowerbound = lowerbound[0]
        upperbound = indices(freqs, lambda x: x>30)
        upperbound = upperbound[0]
        
        left_beta_baseline.append(numpy.mean(left_Pxx[lowerbound:upperbound])) # make sure the dimensions on this are ok 
        right_beta_baseline.append(numpy.mean(left_Pxx[lowerbound:upperbound])) # make sure the dimensions on this are ok 

        left_beta_baseline = numpy.array([left_beta_baseline])
        left_beta_baseline =  left_beta_baseline
        right_beta_baseline = numpy.array([right_beta_baseline])
        right_beta_baseline =  right_beta_baseline 
        
        # compare this to the atreamed_spect data 
        emg_threshold_left = 4 * amplitude_baseline[left_emg_chan] 
        emg_threshold_right = 4 * amplitude_baseline[right_emg_chan]
        
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
    winAdvance = 40.0
    winLen = 400.0
    if baseline==1: # indicating that baseline has occured
        time.sleep(winLen/1000)
    post_baseline = time.time()- end_baseline
    T = winLen/1000
    while post_baseline > T: # run the first window 
        # initiate analysis 
        os.system('say "move now"')
        analysis_end = streamed_raw.shape[0]
        analysis_begin = int(streamed_raw.shape[0] - (amp_fs*winLen/100)) # grab the last 1000 samples for analysis 
        data_windowed = streamed_filt[analysis_begin:analysis_end,:]
#        aux_windowed = streamed_aux[analysis_begin:analysis_end,:]
        amplitude_window= numpy.median(data_windowed, axis=0) # uses the median to decrease the effect of outliers 
#        aux_amplitude_window = numpy.median(aux_windowed, axis = 0)
#        
#        # analysis: mean amplitude over the window, alpha power over the window =
##        freq_emg, Pemg = scipy.signal.welch(data_windowed[:,emg_chan],aux_fs)
##        lowerbound1 = indices(freqs, lambda x: x>3)
##        lowerbound1 = lowerbound1[0]
##        upperbound1 = indices(freqs, lambda x: x>8)
##        upperbound1 = upperbound1[0]
##        lowerbound2 = indices(freqs, lambda x: x>13)
##        lowerbound2 = lowerbound2[0]
##        upperbound2 = indices(freqs, lambda x: x>29)
##        upperbound2 = upperbound2[0]
##        
##        theta_emg_window = numpy.mean(Pxx[lowerbound1:upperbound1])
##        beta_emg_window = numpy.mean(Pxx[lowerbound2:upperbound2])
#        
#        # Check which behavioral condition is true
#        
#        #EYEBLINK CONDN 
#        if numpy.abs(amplitude_window[Fp1]) > numpy.abs(amplitude_threshold[Fp1]) or numpy.abs(amplitude_window[Fp2]) > numpy.abs(amplitude_threshold[Fp2]):
#            KeyDown('j')
#            time.sleep(.016)
#            KeyUp('j')
#            
#            # control: if held down for too long, just keyup
#        else:
#            KeyUp('j')
#            time.sleep(.5)


        # EMG CONDN to help compute ITR (true decision)

        if numpy.abs(amplitude_window[left_emg_chan])> numpy.abs(emg_threshold_left):
            left_decision.append(1)

        if numpy.abs(amplitude_window[right_emg_chan])> numpy.abs(emg_threshold_right):
            right_decision.append(1)            
            
        
#        if tick!= 1 and (numpy.abs(aux_amplitude_window[accel_chan]) >  numpy.abs(aux_threshold[accel_chan])): # make sure to set this threshold fairly high
#            KeyDown('w')
#            time.sleep(.04)
#            tick = 1
#        elif tick== 1 and numpy.abs((aux_amplitude_window[accel_chan]) >  numpy.abs(aux_threshold[accel_chan])):
#            KeyUp('w')
#            time.sleep(.04)
#            tick = 0
       
        
        freqs, left_Pxx = scipy.signal.welch(data_windowed[:,1],fs = amp_fs)
        freqs, right_Pxx = scipy.signal.welch(data_windowed[:,6],fs = amp_fs)            
        lowerbound3 = indices(freqs, lambda x: x>13)
        lowerbound3 = lowerbound3[0]
        upperbound3 = indices(freqs, lambda x: x>30)
        upperbound3 = upperbound3[0]
        left_beta_window.append(numpy.mean(left_Pxx[lowerbound3:upperbound3]))
        right_beta_window.append(numpy.mean(right_Pxx[lowerbound3:upperbound3]))


        if numpy.abs(numpy.mean(left_Pxx[lowerbound3:upperbound3])) <  left_beta_baseline: # i can specify a channel here if that helps 
            left_action.append(1)            
            KeyDown('a')
            time.sleep(.016)
            KeyUp('a')
        else:
            KeyUp('a') 
            time.sleep(.04)
            
        if numpy.abs(numpy.mean(right_Pxx[lowerbound3:upperbound3])) <  right_beta_baseline: # i can specify a channel here if that helps 
            right_action.append(1)            
            KeyDown('d')
            time.sleep(.016)

        else:
            KeyUp('d')
            time.sleep(.04)
        
        left_accuracy.append(sum(left_decision)/sum(left_action))
        right_accuracy.append(sum(right_decision)/sum(right_action))
        
    else:
        sample_num += 1 
        delta = time.time() - start  
        data, auxdata = amp.get_data() #, triger
        trigger = (time.time()-start,'fuck') # gets raletive time stamp
        cnt = io.convert_mushu_data(data,trigger, amp_fs, amp_channels) # convert to wyrm format
        cnt, zi_band = proc.lfilter(cnt, b_band, a_band, zi = zi_band) # bandpass the data  
            #aux_cnt, zi_aux = proc.lfilter(aux_cnt, b_band, a_band, zi = zi_aux)
            #cnt, zi_low = proc.lfilter(cnt, b_high, a_high, zi = zi_high) # highpass 

        # don't worry about subsampling necessarily 
        cnt = proc.subsample(cnt,100) # subsamples the data from 240 Hz to 50 Hz
        streamed_raw = numpy.concatenate((streamed_raw, cnt.data), axis=0)
            #streamed_aux = numpy.concatenate((streamed_aux, aux_cnt.data), axis =0)
        time.sleep(winAdvance/1000) # put this mofo to sleep for 50 ms

    if delta>60*6:
        break

end = time.time()
amp.stop()





