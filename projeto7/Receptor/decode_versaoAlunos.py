
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  
# from detect_peaks import *   
import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


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

    freqs = {
        "1":(697, 1209),
        "3":(697, 1336),
        "2":(697, 1477),
        "A":(697, 1633),
        "4":(770, 1209),
        "5":(770, 1336),
        "6":(770, 1477),
        "B":(770, 1633),
        "7":(852, 1209),
        "8":(852, 1336),
        "9":(852, 1477),
        "C":(852, 1633),
        "X":(941, 1209),
        "0":(941, 1336),
        "#":(941, 1477),
        "D":(941, 1633)
    }


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


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    y = audio[:,0]
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
  
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(y, freq)
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index_p = peakutils.indexes(yf, thres=0.2, min_dist=150)
    freqs_p = xf[index_p]
    print("index de picos: {}".format(index_p)) #yf é o resultado da transformada de fourier
    print(f"frequencias de picos: {freqs_p}")

    #printe os picos encontrados! 

    signal.plotFFT(y, freq)
    plt.xlim(0,2000)

    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 
    def find_keys(freqs, freqs_p):
        for key,value in freqs.items():
            freq1,freq2 = value
            if np.isclose(freqs_p[0], freq1, atol=2) and np.isclose(freqs_p[1], freq2, atol=2):
                return key
        return None
    key = find_keys(freqs,freqs_p)
    print(f"a tecla é {key}")

        
      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
