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
        
        def getDatagrama():
            type = int.from_bytes(com1.getData(1), "little")
            serv = int.from_bytes(com1.getData(1), "little")
            free = int.from_bytes(com1.getData(1), "little")
            n_packs = int.from_bytes(com1.getData(1), "little")
            n_pack = int.from_bytes(com1.getData(1), "little")
            if type == 1:
                id = int.from_bytes(com1.getData(1), "little")
            else:
                t_payload = int.from_bytes(com1.getData(1), "little")
            reset_pack = int.from_bytes(com1.getData(1), "little")
            last_pack = int.from_bytes(com1.getData(1), "little")
            crc1 = int.from_bytes(com1.getData(1), "little")
            crc2 = int.from_bytes(com1.getData(1), "little")
            payload = com1.getData(t_payload)
            eop = com1.getData(4)
            if type == 1:
                return type,serv,free,n_packs,n_pack,id,reset_pack,last_pack,crc1,crc2,payload,eop
            else:
                return type,serv,free,n_packs,n_pack,t_payload,reset_pack,last_pack,crc1,crc2,payload,eop


        answer = b''
        cont = 0
        ocioso = True
        while ocioso == True:
            if com1.rx.getBufferLen() != 0:  
                type,serv,free,n_packs,n_pack,id,reset_pack,last_pack,crc1,crc2,payload,eop = getDatagrama()
                if type == 1:
                    if serv == 13:
                        ocioso = False
                    else:
                        time.sleep(1)
                else: 
                    time.sleep(1)
            else:
                time.sleep(1)
        #m2
        header = makeheader(2,0,0,0,0,0,0,cont,0,0)
        eop_ = b'\xAA\xBB\xCC\xDD'
        txBuffer = header + eop
        com1.sendData(np.asarray(txBuffer))
        cont += 1
        ocioso = True
        while ocioso:
            if cont <= n_packs:
                t1 = time.time()
                t2 = time.time()
                if com1.rx.getBufferLen() != 0:  
                    type,serv,free,n_packs,n_pack,id,reset_pack,last_pack,crc1,crc2,payload,eop = getDatagrama()
                    answer = answer + payload
                    if cont == n_pack: #m4
                        if eop == eop_:
                            header = (4,0,0,0,0,0,0,cont,0,0)
                            txBuffer = header + eop_
                            com1.sendData(np.asarray(txBuffer)) 
                            cont+=1
                        else: #m6
                            header = makeheader(6,0,0,0,0,0,cont,cont,0,0)
                            txBuffer = header + eop_
                            com1.sendData(np.asarray(txBuffer)) 
                    else: #m6
                        header = makeheader(6,0,0,0,0,0,cont,cont,0,0)
                        txBuffer = header + eop_
                        com1.sendData(np.asarray(txBuffer))                        
                else:
                    time.sleep(1)
                    if t2 + 20 > time.time():
                        ocioso = False
                        header = (5,0,0,0,0,0,0,cont,0,0)
                        txBuffer = header + eop_
                        com1.sendData(np.asarray(txBuffer)) 
                        com1.disable()
                    else:
                        if t1 + 2 > time.time(): #m4
                            header = (4,0,0,0,0,0,0,cont-1,0,0)
                            txBuffer = header + eop_
                            com1.sendData(np.asarray(txBuffer)) 
                            t1 = time.time()

            else:
                com1.disable()
                print("--------------------")
                print("      SUCESSO!      ")
                print("--------------------")

                     

     
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
