
#importe as biblioteca
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft, fftshift
from scipy.signal import resample
from scipy.io import wavfile

s = signalMeu()

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    #y  = np.append(signal, np.zeros(len(signal)*fs))
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
    yf = fft(signal)
    return(xf, fftshift(yf))

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

# O audio escolhido tem sampleRate de 4800, o código abaixo muda isso para 44100

class AudioProcessor:
    @staticmethod
    def modify_sample_rate(input_filename, output_filename, new_sample_rate=44100):
        # Read the audio file
        sample_rate, audio_data = wavfile.read(input_filename)

        # Calculate the resampling factor
        resampling_factor = new_sample_rate / sample_rate

        # Resample the audio data to the new sample rate
        resampled_audio = resample(audio_data, int(len(audio_data) * resampling_factor))

        # Save the modified audio to a new WAV file
        wavfile.write(output_filename, new_sample_rate, resampled_audio.astype(np.int16))

# Example usage:
input_filename = "audios/belligol.wav"
output_filename = "audios/initial44100.wav"
new_sample_rate = 44100

AudioProcessor.modify_sample_rate(input_filename, output_filename, new_sample_rate)


def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    samplerate, u = wavfile.read('audios/initial44100.wav')
    u = [s[0] for s in u]
    u = u[0:220500]

    fs = 44100
    T = 5
    y = []
    a = 0.005962
    b = 0.005528
    d = -1.782 
    e = 0.7971
    i = 0
    while i < len(u):
        if i < 2:
            yf = u[i]
        else:
            yf = (-d* y[i-1] - e*y[i-2] + a*u[i-1] + b*u[i-2])

        y.append(yf)
        print(i, len(u))
        i += 1

    st=[]
    t = np.linspace(0,T,int(T*fs))
    i = 0
    while i < len(y):
        c = np.cos(2*np.pi*14000*t[i])*14000
        st.append(c + y[i]*c)
        print(len(st), len(y))
        i+=1

    st = st/max(st)

    s.plotFFT(u, 44100)
    s.plotFFT(y, 44100)
    s.plotFFT(st, 44100)

    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    sd.play(st, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

    

if __name__ == "__main__":
    main()
