# csaudio.py

# import csaudio ; reload(csaudio) ; from csaudio import *

import wave
    
def printParams(params):
    print 'Parameters:'
    print '  nchannels:', params[0]
    print '  sampwidth:', params[1]
    print '  framerate:', params[2]
    print '  nframes  :', params[3]
    print '  comptype :', params[4]
    print '  compname :', params[5]
    
    
def tr(params,rf):
    """ tr transforms raw frames to floating-point samples """
    
    samps = [ord(x) for x in rf]    # convert to numeric bytes
    
    # give parameters nicer names
    nchannels = params[0]
    sampwidth = params[1]
    nsamples  = params[3]
    
    if sampwidth == 1:

        for i in range(nsamples):
            if samps[i] < 128:
                samps[i] *= 256.0       # Convert to 16-bit range, floating
            else:
                samps[i] = (samps[i] - 256) * 256.0

    elif sampwidth == 2:

        newsamps = nsamples * nchannels * [0]

        for i in range(nsamples * nchannels):
            # The wav package gives us the data in native
            # "endian-ness".  The clever indexing with wave.big_endian
            # makes sure we unpack in the proper byte order.
            sampval = samps[2*i + 1 - wave.big_endian] * 256 \
              + samps[2*i + wave.big_endian]
            if sampval >= 32768:
                sampval -= 65536
            newsamps[i] = float(sampval)

        samps = newsamps

    else:
        print 'A sample width of', params[1], 'is not supported.'
        print 'Returning silence.'
        samps = nsamples * [0.0]
        
    if nchannels == 2:
        # Mix to mono
        newsamps = nsamples * [0]
        for i in range(nsamples):
            newsamps[i] = (samps[2 * i] + samps[2 * i + 1]) / 2.0
        samps = newsamps

    return samps
    
    
    
def tri(params,samps):
    """ tri is tr inverse, i.e. from samples to rawframes """
    
    if params[1] == 1:                 # one byte per sample
        samps = [int(x+127.5) for x in samps]
        #print 'max, min are', max(samps), min(samps)
        rf = [chr(x) for x in samps]
        
    elif params[1] == 2:               # two bytes per sample
        bytesamps = (2*params[3])*[0]  # start at all zeros
        for i in range(params[3]):
            # maybe another rounding strategy in the future?
            intval = int(samps[i])
            if intval >  32767: intval = 32767
            if intval < -32767: intval = -32767  # maybe could be -32768
            
            if intval < 0: intval += 65536 # Handle negative values

            # The wav package wants its data in native "endian-ness".
            # The clever indexing with wave.big_endian makes sure we
            # pack in the proper byte order.
            bytesamps[2*i + 1 - wave.big_endian] = intval / 256
            bytesamps[2*i + wave.big_endian] = intval % 256
                
        samps = bytesamps
        #print 'max, min are', max(samps), min(samps)
        rf = [chr(x) for x in samps]
        
    return ''.join(rf)
    

def get_data(filename):
    """ the file needs to be in .wav format
        there are lots of conversion programs online, however,
        to create .wav from .mp3 and other formats
    """
    # this will complain if the file isn't there!
    fin = wave.open(filename, 'rb')
    params = fin.getparams()
    #printParams(params)
    rawFrames = fin.readframes(params[3])
    # need to extract just one channel of sound data at the right width...
    fin.close()
    return params, rawFrames


def readwav(filename):
    """ readwav returns the audio data from the file
        named filename, which must be a .wav file.
        
        Call this function as follows:
        
        samps, sr = readwav(filename)

        samps will be a list of the raw sound samples (floats)
        sr will be the sampling rate for that list (integer)
    """
    sound_data = [0,0]
    read_wav(filename,sound_data)
    samps = sound_data[0]
    sr = sound_data[1]
    if type(samps) != type([]): samps = [42] # default value
    return samps, sr

    
def read_wav(filename,sound_data):
    """ read_wav returns the audio data from the file
        named filename (the first input) in the list
        named sound_data (the second input)

        If the file exists and is the correct .wav format,
        then after this call sound_data will be a list of two
        elements:

        sound_data[0] will be a list of the raw sound samples
        sound_data[1] will be the sampling rate for that list

        That is, sound_data will be the following:
    
            [ [d0, d1, d2, ...], samplingrate ]
            
        where each d0, d1, d2, ... is a floating-point value
        and sampling rate is an integer, representing the
        frequency with which audio samples were taken.

        No value is returned from this function!
    """
    if type(sound_data) != type([]):
        print """
            read_wav was called with a second input,
            sound_data, that was _not_ of type list.

            That input needs to be a list, e.g., []
            """
        return # nothing

    # sound_data is a list: we create/clear its first two elements
    if len(sound_data) < 1:
        sound_data.append(0)
    if len(sound_data) < 2:
        sound_data.append(0)
    # now it has at least two elements, and we reset them
    sound_data[0] = 42
    sound_data[1] = 42

    try:        
        params, rf = get_data(filename)
        samps = tr(params,rf)
    except:
        print "There was a problem with the file", filename
        print "You might check if it's here and of"
        print "the correct format (.wav) ... "
        return # nothing
    
    numchannels = params[0]
    datawidth = params[1]
    framerate = params[2]
    numsamples = params[3]
    
    print
    print 'You opened', filename, 'which has'
    print '   ', numsamples, 'audio samples, taken at'
    print '   ', framerate, 'hertz (samples per second).'
    print
    
    sound_data[0] = samps
    sound_data[1] = framerate

    return # nothing


def write_data(params=None, rawFrames=None, filename="out.wav"):
    """ back out to .wav format """

    fout = wave.open(filename,'wb')
    if params:
        fout.setparams(params)
        if rawFrames:
            fout.writeframes(rawFrames)
        else:
            print 'no frames'
    else:
        print 'no params'
    
    fout.close()
    

def writewav(samps, sr, filename):
    """ write_wav saves a .wav file whose

            first input parameter is the audio data as a list
            
            second parameter is the integer sampling rate
                the minimum allowed value is 1 hertz (1 sample per second),
                which is well under human hearing range
                
            third parameter is the output file name
                if no name is specified, this parameter defaults to 'out.wav'
    """
    write_wav([samps, sr], filename)
    
    
def write_wav(sound_data, filename="out.wav"):
    """ write_wav outputs a .wav file whose
            first parameter is the [audio data, srate] as a list
                
            second parameter is the output file name
                if no name is specified, this parameter defaults to 'out.wav'
    """
    if type(sound_data) != type([]) or \
       len(sound_data) < 2 or \
       type(sound_data[0]) != type([]) or \
       type(sound_data[1]) != type(42):
        print """
            write_wav was called with a first input,
            sound_data, that was _not_ an appropriate list.

            That input needs to be a list such that
            sound_data[0] are the raw sound samples and
            sound_data[1] is the sampling rate, e.g.,

                [ [d0, d1, d2, ...], samplingrate ]
            
            where each d0, d1, d2, ... is a floating-point value
            and sampling rate is an integer, representing the
            frequency with whi audio samples were taken.
            """
        return # nothing

    # name the two components of sound_data
    data = sound_data[0]
    samplingrate = sound_data[1]

    # compose the file...
    framerate = int(samplingrate)
    if framerate < 0:
        framerate = -framerate
    if framerate < 1:
        framerate = 1
        
    # always 1 channel and 2 output bytes per sample
    params = [1, 2, framerate, len(data), "NONE", "No compression"]
    
    # convert to raw frames
    rawframesstring = tri(params,data)
    write_data(params, rawframesstring, filename)
    
    print
    print 'You have written the file', filename, 'which has'
    print '   ', len(data), 'audio samples, taken at'
    print '   ', samplingrate, 'hertz.'
    print

    return # nothing
    
    
# a useful thing to have... can be done all in sw under windows...
import os

if os.name == 'nt':
    import winsound
elif os.uname()[0] == 'Linux':
    import ossaudiodev

def play(filename):
    """ play a .wav file for Windows, Linux, or Mac 
        for Mac, you need to have the "play"
        application in the current folder (.)
    """
    if type(filename) != type(''):
        raise TypeError, 'filename must be a string'
    if os.name == 'nt':
        winsound.PlaySound(filename, winsound.SND_FILENAME)
    elif os.uname()[0] == 'Linux':
	os.system('/usr/bin/play ' + filename + ' || /usr/bin/aplay ' + filename)
    # assume MAC, if not a Windows or Linux machine
    # if you're using another OS, you'll need to adjust this...
    else:
        # this was the pre MacOS 10.5 method...
        #os.system( ('./play ' + filename) )
        # now, it seems that /usr/bin/afplay is provided with MacOS X
        # and it seems to work in the same way play did
        # perhaps Apple simply used play?
        os.system( ('/usr/bin/afplay ' + filename) )
        

        
        
   

