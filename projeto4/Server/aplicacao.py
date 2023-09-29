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
import datetime
import crcmod
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM6"                  # Windows(variacao de)

# crc16 = crcmod.mkCrcfun()

# def crc(data):
#     crc16.update(data)
#     return (crc16.crcValue).to_bytes(2,"little")

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

        meu_serv = 13
        answer = b''
        cont = 0
        ocioso = True

        def crc_from_payload(payload: bytes):
            crc16 = crcmod.mkCrcFun(0x11021, initCrc=0x0000, xorOut=0x0000)
            crc_value = crc16(payload)
            return crc_value.to_bytes(2, "little")

        def write(status,type,bytestotal=14,package=0,total_packages=0,crc_payload=0):
            time = datetime.datetime.now()
            file = r"C:\Users\brnos\Documents\INSPER\Camadas\projeto4\Server\txt\Server2.txt" 

            with open(file, 'a') as file: #abrir no modo de adição 'a'
                if status:
                    file.write(f'{time}/envio/{type}/{bytestotal}\n')
                else:
                    file.write(f'{time}/receb/{type}/{bytestotal}/{package}/{total_packages}\n')
            return None



        def makeheader(h0,h1,h2,h3,h4,h5,h6,h7,h8,h9):
            header = bytes([h0,h1,h2,h3,h4,h5,h6,h7,h8,h9])
            return  header
        
        def getDatagrama():
            type = int.from_bytes(com1.getData(1)[0], "little")
            serv = int.from_bytes(com1.getData(1)[0], "little")
            free = int.from_bytes(com1.getData(1)[0], "little")
            n_packs = int.from_bytes(com1.getData(1)[0], "little")
            n_pack = int.from_bytes(com1.getData(1)[0], "little")
            
            if type == 1:
                id = int.from_bytes(com1.getData(1)[0], "little")
            else:
                t_payload = int.from_bytes(com1.getData(1)[0], "little")
            reset_pack = int.from_bytes(com1.getData(1)[0], "little")
            last_pack = int.from_bytes(com1.getData(1)[0], "little")
            crc = com1.getData(2)[0]
            if type == 1:
                payload = 0
                eop = com1.getData(4)[0]
                return type,serv,free,n_packs,n_pack,id,reset_pack,last_pack,crc,payload,eop
            else:
                if cont != 26:
                    payload = com1.getData(114)[0]
                else:
                    payload = com1.getData(t_payload)[0]
                eop = com1.getData(4)[0]
                return type,serv,free,n_packs,n_pack,t_payload,reset_pack,last_pack,crc,payload,eop
            
        while ocioso == True:
            if com1.rx.getBufferLen() != 0:  
                type,serv,free,n_packs,n_pack,id,reset_pack,last_pack,crc,payload,eop = getDatagrama()
                write(False,type)
                if type == 1:
                    if serv == meu_serv:
                        ocioso = False
                    else:
                        time.sleep(1)
                else: 
                    time.sleep(1)
            else:
                time.sleep(1)
        print("m2")
        #m2
        header = makeheader(2,0,0,0,0,0,0,cont,0,0)
        eop_ = bytes([0XAA,0XBB,0XCC,0XDD])
        txBuffer = header + eop_
        print(txBuffer)
        com1.sendData(np.asarray(txBuffer))
        write(True,2)
        cont += 1
        ocioso = True
        while ocioso:
            if cont <= n_packs:
                t1 = time.time()
                t2 = time.time()
                while com1.rx.getBufferLen() == 0:
                    com1.rx.getBufferLen()
                    if t2 + 20 < time.time(): #m5
                        ocioso = False
                        header = makeheader(5,0,0,0,0,0,0,cont,0,0)
                        txBuffer = header + eop_
                        com1.sendData(np.asarray(txBuffer))
                        write(True,5) 
                        print("mandou m5")
                        com1.disable()
                if com1.rx.getBufferLen() !=0:
                    print(com1.rx.getBufferLen())
                    type,serv,free,n_packs,n_pack,t_payload,reset_pack,last_pack,crc,payload,eop = getDatagrama()
                    com1.rx.clearBuffer()
                    write(False,type,t_payload,n_pack,n_packs)
                    if type == 3:
                        print("crc recebido:", crc)
                        print("crc criado:", crc_from_payload(payload))
                        if crc == crc_from_payload(payload):
                            print("cont:", cont)
                            print("n_pack:", n_pack)
                            print("total:", n_packs)
                            if cont == n_pack: #m4
                                if eop == eop_:
                                    answer = answer + payload
                                    header = makeheader(4,0,0,0,0,0,0,cont,0,0)
                                    txBuffer = header + eop_
                                    com1.sendData(np.asarray(txBuffer))
                                    write(True,4)
                                    print("mandou m4 com cont =", cont)
                                    cont+=1
                                else: #m6
                                    header = makeheader(6,0,0,0,0,0,cont,cont,0,0)
                                    txBuffer = header + eop_
                                    com1.sendData(np.asarray(txBuffer))
                                    write(True,6)
                                    print("mandou m6 com cont =", cont)
                            else: #m6
                                header = makeheader(6,0,0,0,0,0,cont,cont,0,0)
                                txBuffer = header + eop_
                                com1.sendData(np.asarray(txBuffer))
                                write(True,6) 
                                print("mandou m6 com cont =", cont)
                    elif type == 5: #m5
                        time.sleep(1)
                        if t2 + 20 < time.time():
                            ocioso = False
                            header = makeheader(5,0,0,0,0,0,0,cont,0,0)
                            txBuffer = header + eop_
                            com1.sendData(np.asarray(txBuffer))
                            write(True,5)
                            print("mandou m5")
                            com1.disable()                     
                else: #m5
                    time.sleep(1)
                    if t2 + 20 > time.time():
                        ocioso = False
                        header = makeheader(5,0,0,0,0,0,0,cont,0,0)
                        txBuffer = header + eop_
                        com1.sendData(np.asarray(txBuffer))
                        write(True,5) 
                        print("mandou m5")
                        com1.disable()
                    else:
                        if t1 + 2 > time.time(): #m4
                            header = makeheader(4,0,0,0,0,0,0,cont-1,0,0)
                            txBuffer = header + eop_
                            com1.sendData(np.asarray(txBuffer))
                            write(True,4)
                            print("mandou m4 com cont =", cont)
                            t1 = time.time()

            else:
                imagemCopia = r"C:\Users\brnos\Documents\INSPER\Camadas\projeto4\img\imagemCopia.jpg"
                f = open(imagemCopia, 'wb')
                f.write(answer)
                f.close()
                com1.disable()
                ocioso = False
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
