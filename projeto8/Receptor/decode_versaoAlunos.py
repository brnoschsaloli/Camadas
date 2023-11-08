
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  
# from detect_peaks import *   
import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    freq = 44100
    sd.default.samplerate = freq #taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  5 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    numAmostras = duration * freq

    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao
    t = 2
    print(f"a captação começará em {t} segundos")

    #use um time.sleep para a espera
    time.sleep(t)

    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("a gravação foi inicializada")

    #para gravar, utilize
    audio = sd.rec(int(numAmostras), samplerate = freq, channels=1)
    sd.wait()
    print("gravação finalizada")

    # filtro de frequências acima de 4kHz
    



    # reproduzindo audio com menor qualidade
    y = audio[:,0]
    sd.play(y, freq)
      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
