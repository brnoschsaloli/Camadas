#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 
from enlaceTx import *
from enlaceRx import *
from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM6"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main \n")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        print("Abriu a comunicação \n")

        print("A recepção vai começar \n")

        print("esperando um byte de sacrifício \n")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(1)

        print("byte sacrificado com sucesso!\n")

        inicia = True
        pacote_atual_int = 0
        pacote_anterior_int = 0
        ultimo_pacote = 0
        imagem = b''
        while inicia:

            print("A recepção vai começar \n")

            pacote_atual_b, nRx = com1.getData(2)
            pacote_atual_int = int.from_bytes(pacote_atual_b, "little")

            if pacote_atual_int == pacote_anterior_int + 1:
                pacote_correto = True

            ultimo_pacote_b, _ = com1.getData(2)
            ultimo_pacote = int.from_bytes(ultimo_pacote_b, "little")

            tamanho_payload, _ = com1.getData(1)
            tamanho_payload_int = int.from_bytes(tamanho_payload, "little")

            if pacote_atual_int == ultimo_pacote:
                payload, _ = com1.getData(tamanho_payload_int)
            else:
                payload, _ = com1.getData(50)

            eop, _ = com1.getData(3)

            print("a recepção terminou \n")

            if eop == b'\xff\xff\xff':
                eop_correto = True

            if eop_correto and pacote_correto:

                imagem = imagem + (payload)
                pacote_anterior_int = pacote_atual_int

                if pacote_atual_int == ultimo_pacote:
                    inicia = False
                    txBuffer = b'transmissao sucedida'
                    print("o envio vai começar \n")
                    com1.sendData(np.asarray(txBuffer))
                    print("o envio terminou \n")

                else:
                    txBuffer = b'ok'
                    print("o envio vai começar \n")
                    com1.sendData(np.asarray(txBuffer))
                    print("o envio terminou \n")
                    
            else:
                txBuffer = b'erro!'
                print("o envio vai começar \n")
                com1.sendData(np.asarray(txBuffer))
                print("o envio terminou \n")
                inicia = False     
     
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
