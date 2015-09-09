# -*- coding: utf-8 -*-
import random
import math
from csaudio import play, readwav, writewav


def scale(L, scale_factor):
    '''Given a list L, scales each element of the list by scale_factor'''

    return [scale_factor * n for n in L]

def wrap1( L ):
    """ Given a list L, shifts each element in L to the right by 1 
        (the element at the end of the list wraps around to the beginning)
    """

    # I changed the body of this function to call wrapN, 
    # so that I can reuse the code I wrote for that problem 
    return wrapN(L, 1)   


def wrapN(L, N):
    """ Given a list L, shifts each element in L to the right by N 
        (elements at the end of the list wrap around to the beginning)
    """

    length = len(N)
    return [ L[i-N] for i in range(length) ]


def add_2(L, M):
    '''Given two lists, L and M, adds their respective elements. If the two 
       lists have different lengths, the function truncates the result so that 
       it is as long as the shorter list.
    '''

    length = min(len(L), len(M))  # find the shorter length
    return [ L[i] + M[i] for i in range(length) ]
    
    # Here's an alternative solution that uses the built-in zip function,
    # which truncates for us and creates tuples of the corresponding elements.
    #return [l + m for (l, m) in zip(L, M)]    


def add_scale_2(L, M, L_scale, M_scale):
    '''Given two lists, L and M, and two scale factors, L_scale and M_scale, 
       scales each list by its respective scale factor, then adds the 
       results, pairwise. If the two  lists have different lengths, the function 
       truncates the result so that it is as long as the shorter list.
    '''
    
    return add_2(scale(L, L_scale), scale(M, M_scale))  # yay for code re-use!


# generalized versions of add_2 and add_scale_2

def add_N(lists):
    '''Given a list of lists, adds their respective elements. If the two 
       lists have different lengths, the function truncates the result so that 
       it is as long as the shortest list.
    '''
    
    return map(sum, apply(zip, lists)) # lots of higher-order functions here!


def add_scale_N(lists, scaleFactors):
    '''Given a list of lists and a list of scale factors, scales each list by 
       its respective scale factor, then sums the results, element-wise. If the 
       lists have different lengths, the function  truncates the result so that 
       it is as long as the shortest list.
    '''
    
    scaledLists = [scale(l, f) for (l, f) in zip(lists, scaleFactors)]
    return add_N(scaledLists)


# Helper function:  randomize
def randomize( x, chance_of_replacing ):
    """ randomize takes in an original value, x
        and a fraction named chance_of_replacing.

        With the "chance_of_replacing" chance, it
        should return a random float from -32767 to 32767.

        Otherwise, it should return x (not replacing it).
    """
    r = random.uniform(0,1)
    if r < chance_of_replacing:
        return random.uniform(-32768,32767)
    else:
        return x
    

def replace_some(L, chance_of_replacing):
    '''Given a list L, returns a new list L' where each element in L has a 
       chance_of_replacing chance of being replaced with a random, 
       floating-point value in the range -32767 to 32767.
    '''

    return [randomize(e, chance_of_replacing) for e in L]

#
# below are functions that relate to sound-processing ...
#


# a function to make sure everything is working
def test():
    """ a test function that plays swfaith.wav
        You'll need swfailt.wav in this folder.
    """
    play( 'swfaith.wav' )

    
# The example changeSpeed function
def changeSpeed(filename, newsr):
    """ changeSpeed allows the user to change an audio file's speed
        input: filename, the name of the original file
               newsr, the *new* sampling rate in samples per second
        output: no return value; creates and plays the file 'out.wav'
    """
    samps, sr = readwav(filename)

    print "The first 10 sound-pressure samples are\n", samps[:10]
    print "The original number of samples per second is", sr
    
    newsamps = samps                        # no change to the sound
    writewav( newsamps, newsr, "out.wav" )  # write data to out.wav
    print "\nPlaying new sound..."
    play( 'out.wav' )   # play the new file, 'out.wav'
    


def flipflop(filename):
    """ flipflop swaps the halves of an audio file
        input: filename, the name of the original file
        output: no return value, but
                this creates the sound file 'out.wav'
                and plays it
    """
    print "Playing the original sound..."
    play(filename)
    
    print "Reading in the sound data..."
    samps, sr = readwav(filename)
    
    print "Computing new sound..."
    # this gets the midpoint and calls it x
    x = len(samps)/2
    newsamps = samps[x:] + samps[:x] # flip flop
    newsr = sr                       # no change to the sr
    
    writewav( newsamps, newsr, "out.wav" )
    print "Playing new sound..."
    play( 'out.wav' )




# Sound function to write #1:  reverse







# Sound function to write #2:  volume







# Sound function to write #3:  static







# Sound function to write #4:  overlay







# Sound function to write #5:  echo








# Helper function for generating pure tones
def gen_pure_tone(freq, seconds):
    """ pure_tone returns the y-values of a cosine wave
        whose frequency is freq Hertz.
        It returns nsamples values, taken once every 1/44100 of a second;
        thus, the sampling rate is 44100 Hertz.
        0.5 second (22050 samples) is probably enough.
    """
    sr = 44100
    # how many data samples to create
    nsamples = int(seconds*sr) # rounds down
    # our frequency-scaling coefficient, f
    f = 2*math.pi/sr           # converts from samples to Hz
    # our amplitude-scaling coefficient, a
    a = 32767.0
    # the sound's air-pressure samples
    samps = [ a*math.sin(f*n*freq) for n in range(nsamples) ]
    # return both...
    return samps, sr


def pure_tone(freq, time_in_seconds):
    """ plays a pure tone of frequence freq for time_in_seconds seconds """
    print "Generating tone..."
    samps, sr = gen_pure_tone(freq, time_in_seconds)
    print "Writing out the sound data..."
    writewav( samps, sr, "out.wav" )
    print "Playing new sound..."
    play( 'out.wav' )




# Sound function to write #6:  chord








