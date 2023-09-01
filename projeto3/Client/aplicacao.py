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

Comando1 = bytes([0x04, 0X00, 0X00, 0X00, 0X00]) 
Comando2 = bytes([0x04, 0X00, 0X00, 0XBB, 0X00])
Comando3 = bytes([0XBB, 0X00, 0X00]) 
Comando4 = bytes([0X00, 0XBB, 0X00]) 
Comando5 = bytes([0X00, 0X00, 0XBB]) 
Comando6 = bytes([0x02, 0X00, 0XAA])
Comando7 = bytes([0x02, 0XBB, 0X00]) 
Comando8 = bytes([0x01, 0X00])
Comando9 = bytes([0x01, 0XBB])

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
        N = random.randint(10,30)
        lista_comandos = [Comando1, Comando2, Comando3, Comando4, Comando5, Comando6, Comando7, Comando8, Comando9]
        i = 1
        while i <= N:
            comando = random.randint(0,8)
            
            txBuffer = lista_comandos[comando]  #isso é um array de bytes
        
            print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
            #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        
                
            #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
            #faça um print para avisar que a transmissão vai começar.
            print("A transmissão vai começar")
            #tente entender como o método send funciona!
            #Cuidado! Apenas trasmita arrays de bytes!
                
            
            com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            time.sleep(0.05)
            # time.sleep(0.5)  
            # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
            # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender 
            # como esse método funciona e faça-o funcionar.
            txSize = com1.tx.getStatus()
            while txSize == 0:
                txSize = com1.tx.getStatus()
                
            
            print('enviou = {}' .format(txSize))
            i += 1

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

        time.sleep(5)
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

        rxBuffer, nRx = com1.getData(2)

        if (i) != int.from_bytes(rxBuffer, "little"):
            print('ERRO!')
        else:
            print('SUCESSO!')

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
