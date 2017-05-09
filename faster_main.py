import soundfile as sf
import numpy as np
from scipy.ndimage import imread
import matplotlib.pyplot as plt
import time



def image_to_audio(image,sample_rate=44100,audio_duration=3):
    height,width = image.shape

    total_samples = audio_duration * sample_rate 
    samplesPerPixel = total_samples // width # how many samples should each pixel occupy
    freq_increments = (sample_rate//2) // height # difference in frequency between each pixel
    
    volume = (100/255 * image) ** 2
    volume = volume.repeat(samplesPerPixel,axis=1)
    
    height  = np.arange((1+height)*freq_increments,freq_increments,-freq_increments).reshape(-1,1)
    nsample = np.arange(0,volume.shape[1]).reshape(-1,1)

    frequencies = volume * np.cos(height.dot(nsample.T) * 6.28 / sample_rate)
    max_freq = np.abs(frequencies).sum(axis=0).max()
    frequencies = frequencies.sum(axis=0) * (2**15-1) / max_freq

    return frequencies.astype('int16').reshape(-1,1)


sample_rate,audio_duration = 44100,3

start = time.time()

image = imread('/home/hasebou/Pictures/bus.jpg',mode="RGB")
channels = []

for i in range(3):
    result = image_to_audio(image[:,:,i])
    channels.append(result)

image = imread('/home/hasebou/Pictures/bus.jpg',mode="L")
result = image_to_audio(image,sample_rate=sample_rate,audio_duration=audio_duration)
channels.append(result)

channels = np.concatenate(channels,axis=1)
print(channels.shape)
sf.write('4channel_audio.wav',channels,sample_rate)

print(time.time() - start)