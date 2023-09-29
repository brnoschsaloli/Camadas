#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


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
serialName = "COM3"                  # Windows(variacao de)

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
            
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Ela sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        tamanhos = {
            'h0': 0x00,
            'h1': 0x00,
            'h2': 0x00,
            'h3': 0x00,
            'h4': 0x00,
            'h5': 0x00,
            'h6': 0x00,
            'h7': 0x00,
            'h8': 0x00,
            'h9': 0x00,
        }

        with open("img/imagem.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
            c = b

        txBuffer = c  #isso é um array de bytes
        tamanho = len(txBuffer)
        ntotal = tamanho//114
        nresto = tamanho%114

        if nresto != 0:
            ntotal += 1
            
        tamanhos['h2'] = nresto
        tamanhos['h3'] = ntotal
 

        Eop = bytes([0xAA,0xBB,0xCC,0xDD])

        handshake = True
        tamanhos['h0'] = 0x01
        tamanhos['h1'] = 0x13
        head = bytes([tamanhos['h0'], tamanhos['h1'], tamanhos['h2'], tamanhos['h3'], tamanhos['h4'], tamanhos['h5'], tamanhos['h6'], tamanhos['h7'], tamanhos['h8'], tamanhos['h9']])
        txBuffer = head + Eop
        while handshake is True:
            com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            time.sleep(0.05)

            txSize = com1.tx.getStatus()
            while txSize == 0:
                txSize = com1.tx.getStatus()
                                
            print('enviou = {}' .format(txSize))

            t = time.time() + 5
            while com1.rx.getBufferLen() == 0 and time.time() < t:
                com1.rx.getBufferLen() 
            
            if com1.rx.getBufferLen() == 0:
                handshake = True

            else:
                tipo = com1.getData(1)
                com1.rx.clearBuffer()
                if int.from_bytes(tipo, "little") == 2:
                    handshake = False

        cont = 1
        while cont <= ntotal:
            tamanhos['h0'] = 0x03
            tamanhos['h4'] = cont
            head = bytes([tamanhos['h0'], tamanhos['h1'], tamanhos['h2'], tamanhos['h3'], tamanhos['h4'], tamanhos['h5'], tamanhos['h6'], tamanhos['h7'], tamanhos['h8'], tamanhos['h9'], tamanhos['h10'], tamanhos['h11']])
            payload = c[0:114]
            c = c[114:tamanho]
            txBuffer = head + payload + Eop
        
            print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))

            print("A transmissão vai começar")

            com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            time.sleep(0.05)

            txSize = com1.tx.getStatus()
            while txSize == 0:
                txSize = com1.tx.getStatus()
                        
            print('enviou = {}' .format(txSize))

            timer1 = time.time()
            timer2 = time.time()
            verificação = True
            while verificação:

                if com1.rx.getBufferLen() != 0:
                    tipo = com1.getData(1)
                    com1.rx.clearBuffer()
                    if int.from_bytes(tipo, "little") == 4:
                        verificação = False
                        cont += 1

                else:
                    if (time.time() - timer1) > 5:
                        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
                        time.sleep(0.05)

                        txSize = com1.tx.getStatus()
                        while txSize == 0:
                            txSize = com1.tx.getStatus()
                            
                        print('enviou = {}' .format(txSize))

                        timer1 = time.time()
                    
                    if (time.time() - timer2) > 20:
                        tamanhos['h0'] = 0x05
                        head = bytes([tamanhos['h0'], tamanhos['h1'], tamanhos['h2'], tamanhos['h3'], tamanhos['h4'], tamanhos['h5'], tamanhos['h6'], tamanhos['h7'], tamanhos['h8'], tamanhos['h9'], tamanhos['h10'], tamanhos['h11']])
                        txBuffer = head + payload + Eop
                        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
                        time.sleep(0.05)

                        txSize = com1.tx.getStatus()
                        while txSize == 0:
                            txSize = com1.tx.getStatus()
                            
                        print('enviou = {}' .format(txSize))

                        print("-------------------------")
                        print("Comunicação encerrada")
                        print("-------------------------")
                        com1.disable()

                    else:
                        if com1.rx.getBufferLen() != 0:
                            tipo = com1.getData(1)
                            if int.from_bytes(tipo, "little") == 6:
                                h1 = com1.getData(1)
                                h2 = com1.getData(1)
                                h3 = com1.getData(1)
                                h4 = com1.getData(1)
                                h5 = com1.getData(1)
                                h6 = com1.getData(1)
                                com1.rx.clearBuffer()
                                cont = int.from_bytes(h6, "little")
                                tamanhos['h0'] = 0x03
                                tamanhos['h4'] = cont
                                head = bytes([tamanhos['h0'], tamanhos['h1'], tamanhos['h2'], tamanhos['h3'], tamanhos['h4'], tamanhos['h5'], tamanhos['h6'], tamanhos['h7'], tamanhos['h8'], tamanhos['h9'], tamanhos['h10'], tamanhos['h11']])
                                txBuffer = head + payload + Eop
                                com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
                                time.sleep(0.05)

                                txSize = com1.tx.getStatus()
                                while txSize == 0:
                                    txSize = com1.tx.getStatus()
                                            
                                print('enviou = {}' .format(txSize))

                                timer1 = time.time()
                                timer2 = time.time()

                        
        #Envia bit final    
        txBuffer = bytes([0x01, 0xFF])  #isso é um array de bytes
        
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
            #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
                
            
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            # time.sleep(0.5)  
            # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
            # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender 
            # como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        while txSize == 0:
            txSize = com1.tx.getStatus()
                
        print('enviou = {}' .format(txSize))

        while com1.rx.getBufferLen() == 0:
            com1.rx.getBufferLen()
            
        rxBuffer, nRx = com1.getData(1)

        if rxBuffer == b'\x11':
            print('Erro')
            com1.disable()
        else:
            # Encerra comunicação
            print("Sucesso")

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
