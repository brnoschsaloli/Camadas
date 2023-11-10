
#Importe todas as bibliotecas
import peakutils    #alternativas  
# from detect_peaks import *   
import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from suaBibSignal import *
from scipy import signal
from scipy.fftpack import fft, fftshift
from scipy.signal import resample
from scipy.io import wavfile


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    s = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    freq = 44100
    T = 5
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    samplerate, st = wavfile.read('audios/audio_modulado.wav') 

    s.plotFFT(st, freq)

    t = np.linspace(0,T,int(T*freq))
    i = 0
    dm = []
    while i < len(st):
        c = np.cos(2*np.pi*14000*t[i])*14000
        n = st[i] * c
        dm.append(n)
        print(i, len(st))
        i += 1

    s.plotFFT(dm, 44100)

    i = 0
    a = 0.005962
    b = 0.005528
    d = -1.782 
    e = 0.7971
    dmf = []
    while i < len(dm):
        if i < 2:
            yf = dm[i]
        else:
            yf = (-d* dmf[i-1] - e*dmf[i-2] + a*dm[i-1] + b*dm[i-2])

        dmf.append(yf)
        print(i, len(dm))
        i += 1
        
    dmf = dmf/max(dmf)

    s.plotFFT(dmf, 44100)

    wavfile.write('audios/audio_demodulado.wav', 44100, np.array(dmf))
    ## Exiba gráficos do fourier do som gravados 
    
    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    sd.play(dmf, freq)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()



if __name__ == "__main__":
    main()
