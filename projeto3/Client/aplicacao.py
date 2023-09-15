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
import random

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
            '0': 0x00,
            '1': 0x00,
            '2': 0x00,
            '3': 0x00,
            '4': 0x00,
            '5': 0x00,
            '6': 0x00,
            '7': 0x00,
            '8': 0x00,
            '9': 0x00,
            '10': 0x00,
            '11': 0x00,
        }

        with open("img/imagem.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
            c = b

        txBuffer = c  #isso é um array de bytes
        tamanho = len(txBuffer)
        ntotal = tamanho//50
        nresto = tamanho%50

        if nresto != 0:
            ntotal += 1
        tamanhos['4'] = nresto
        
        if ntotal > 255:
            tamanhos['2'] = 255
            tamanhos['3'] = (ntotal - 255)
        else:
            tamanhos['2'] = ntotal

        n = 1
        while n <= ntotal:
            if n <= 255:
                tamanhos['0'] = n
            else:
                tamanhos['0'] = 0xff
                tamanhos['1'] = (n-255)
            
            head = bytes([tamanhos['0'], tamanhos['1'], tamanhos['2'], tamanhos['3'], tamanhos['4'], tamanhos['5'], tamanhos['6'], tamanhos['7'], tamanhos['8'], tamanhos['9'], tamanhos['10'], tamanhos['11']])
            payload = c[0:50]
            c = c[50:tamanho]
            Eop = bytes([0xff,0xff,0xff])

            txBuffer = head + payload + Eop
        
            print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))

            print("A transmissão vai começar")

            com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            time.sleep(0.05)

            txSize = com1.tx.getStatus()
            while txSize == 0:
                txSize = com1.tx.getStatus()
                        
            print('enviou = {}' .format(txSize))

            while com1.rx.getBufferLen() == 0:
                com1.rx.getBufferLen()
            
            rxBuffer, nRx = com1.getData(1)

            while rxBuffer == b'erro!':
                com1.sendData(np.asarray(txBuffer))
                time.sleep(0.05)

                txSize = com1.tx.getStatus()
                while txSize == 0:
                    txSize = com1.tx.getStatus()
                        
                print('enviou = {}' .format(txSize))

                while com1.rx.getBufferLen() == 0:
                    com1.rx.getBufferLen() == 0
                
                rxBuffer, nRx = com1.getData(1)

            n += 1


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

        t = time.time() + 5
        while com1.rx.getBufferLen() == 0 and time.time() < t:
            com1.rx.getBufferLen() == 0
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        if com1.rx.getBufferLen() == 0:
            print('Time Out')
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            com1.disable()

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
