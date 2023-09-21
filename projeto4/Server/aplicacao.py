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

        def makeheader(h0,h1,h2,h3,h4,h5,h6,h7,h8,h9):
            return  bytearray([h0,h1,h2,h3,h4,h5,h6,h7,h8,h9])
        
        def getheader():
            int.from_bytes(pacote_atual_b, "little")
            tm = int.from_bytes(com1.getData(1), "little")
            serv = int.from_bytescom1.getData(1)
            liv = int.from_bytescom1.getData(1)
            n_packs = int.from_bytescom1.getData(1)
            n_pack = int.from_bytescom1.getData(1)
            if tm == 1:
                id = int.from_bytescom1.getData(1)
            else:
                t_payload = int.from_bytescom1.getData(1)
            reset_pack = int.from_bytescom1.getData(1)
            last_pack = int.from_bytescom1.getData(1)
            crc1 = int.from_bytescom1.getData(1)
            crc2 = int.from_bytescom1.getData(1)
            message = com1.getData(t_payload)
            eop = com1.getData(4)
            if tm == 1:
                return tm,serv,liv,n_packs,n_pack,id,reset_pack,last_pack,crc1,crc2,message,eop
            else:
                return tm,serv,liv,n_packs,n_pack,t_payload,reset_pack,last_pack,crc1,crc2,message,eop


        answer = b''
        cont = 0
        ocioso = True
        if ocioso == True:
            if com1.rx.getBufferLen() != 0:  
                
                if tm == 1:
                    if serv == 'x':
                        ocioso = False
                    else:
                        time.sleep(1)
                else: 
                    time.sleep(1)
            else:
                time.sleep(1)
        else:
            
            txBuffer = 'msg2'
            cont += 1
                     

     
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
