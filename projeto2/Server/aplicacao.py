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
        total = 0
        inicia = True
        lista_comandos = []
        while inicia:
        
            n, nRx = com1.getData(1)
            n = int.from_bytes(n, "little")
            rxBuffer, nRx = com1.getData(n)
            lista_comandos.append(rxBuffer)
            total +=1
            if rxBuffer == b'\xff':
                inicia=False
        
        print(f'Total de comandos recebidos = {total} \n') 
        print(f'A lista de comandos recebidos é: \n\n {lista_comandos} \n')
        print("a recepção terminou \n")
        print("o envio vai começar \n") 

        txBuffer = total.to_bytes(3, "little")

        com1.sendData(np.asarray(txBuffer))

        txSize = com1.tx.getStatus()
        while txSize == 0:
           txSize = com1.tx.getStatus()
        print('enviou o número de comandos recebidos em {} bytes \n' .format(txSize))

        

        print("o envio terminou \n")


            

            
    
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
