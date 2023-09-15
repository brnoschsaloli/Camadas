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
import os
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

        handshake, _ = com1.getData(1)
        print(handshake)
        if handshake == b'\x01':
            txBuffer = b'\x80'
            print(txBuffer)
            com1.sendData(np.asarray(txBuffer))
        else:
            inicia = False
            print("Handshake errado, meu amigo")


        while inicia:

            print("A recepção vai começar \n")

            pacote_atual_b, nRx = com1.getData(2)
            pacote_atual_int = int.from_bytes(pacote_atual_b, "little")

            if pacote_atual_int == pacote_anterior_int + 1:
                pacote_correto = True
            else:
                pacote_correto = False

            ultimo_pacote_b, _ = com1.getData(2)
            ultimo_pacote = int.from_bytes(ultimo_pacote_b, "little")

            tamanho_payload, _ = com1.getData(1)
            tamanho_payload_int = int.from_bytes(tamanho_payload, "little")

            _,_ = com1.getData(7)

            if pacote_atual_int == ultimo_pacote:
                tamanho_payload_int_real = com1.rx.getBufferLen() - 3
                if tamanho_payload_int_real == tamanho_payload_int:
                    payload, _ = com1.getData(tamanho_payload_int)
                else:
                    txBuffer = b'\x11'
                    print(txBuffer)
                    com1.sendData(np.asarray(txBuffer))
                    inicia = False
                    print('\nErro: tamanho do payload do pacote diferente do esperado')
                    com1.disable()
                    ultimo_pacote = True
                    
                
            else:
                payload, _ = com1.getData(50)

            eop, _ = com1.getData(3)

            print("a recepção terminou \n")

            # txBuffer = b'\xff'
            # com1.sendData(np.asarray(txBuffer))
            eop_correto = False
            if eop == b'\xff\xff\xff':
                eop_correto = True
            if eop_correto and pacote_correto and ultimo_pacote:

                imagem = imagem + (payload)
                pacote_anterior_int = pacote_atual_int

                if pacote_atual_int == ultimo_pacote:
                    inicia = False
                    txBuffer = b'transmissao sucedida'
                    print("o envio vai começar \n")
                    com1.sendData(np.asarray(txBuffer))
                    print("o envio terminou \n")
                    imagemCopia = r"C:\Users\brnos\Documents\INSPER\Camadas\projeto3\img\imagemCopia.jpg"
                    f = open(imagemCopia, 'wb')
                    f.write(imagem)
                    f.close()
                    print('\nConcluído com Sucesso')


                else:
                    txBuffer = b'\x80'
                    print(txBuffer)
                    print("o envio vai começar \n")
                    com1.sendData(np.asarray(txBuffer))
                    print("o envio terminou \n")
                    
            else:
                if ultimo_pacote == False:
                    print('\nEnvio fora de ordem! \n')
                    txBuffer = b'\x11'
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
