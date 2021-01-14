import os
import random
import time
import serial
import pygame

class Interfaz():
    def __init__(self, x,y):
        pygame.init()
        self.current_path = os.path.dirname(__file__)
        self.win = pygame.display.set_mode((x,y))
        self.gotas = []
        self.animacion_gota = [pygame.image.load(os.path.join(self.current_path, 'agua1.png')).convert_alpha(),pygame.image.load(os.path.join(self.current_path, 'agua2.png')).convert_alpha(),pygame.image.load(os.path.join(self.current_path, 'agua3.png')).convert_alpha(),pygame.image.load(os.path.join(self.current_path, 'agua4.png')).convert_alpha()]
        self.fondo = pygame.image.load(os.path.join(self.current_path, 'tierra.png')).convert_alpha()

    def cargarComponentes(self):                
        self.win.blit(self.fondo,(0,0))
        pygame.display.update()
        pygame.display.set_caption("Sensor de Humedad en la Tierra")
        pygame.display.set_icon(self.animacion_gota[0])
    
    def actualizarTexto(self,porcentaje):
        myfont = pygame.font.SysFont('Comic Sans MS', 27) 
        texto = 'Humedad :'+str("{:.2f}".format(porcentaje))+"%"
        textsurface = myfont.render(texto, True, (0, 0, 0))
        self.win.blit(textsurface,(260,10))

    def ejecutar(self):
        self.cargarComponentes()
        arduino = Arduino()

        calculos = Calculos()
        
        porcentaje = calculos.calcularPorcentaje("00000000")
        self.actualizarTexto(porcentaje)
        aux_por = porcentaje        

        clk = pygame.time.Clock()
        run = True
        i=0
        

        while run:
                                            

            clk.tick(240)                          
            self.win.blit(self.fondo,(0,0))
            porcentaje = calculos.calcularPorcentaje(arduino.leerArduino())            
            cambios = porcentaje - aux_por
            print(porcentaje)
            if(cambios//5 < 0):
                
                for i in range(0,int(-cambios//5)):
                    if len(self.gotas) > 1:
                        self.gotas.pop()    
                    else:
                        self.gotas[0].y_init = 697
            else:
                for i in range(0,int(cambios//5)):
                    if(len(self.gotas)<=20):
                        self.gotas.append(Agua(random.randint(2,5),random.randint(75,450),random.randint(290,500)))                
            self.actualizarTexto(porcentaje)                    

            try:
                for i in self.gotas:
                    i.caer(self.win,self.animacion_gota)
            except:
                print("Error")
            
            aux_por = porcentaje
            pygame.display.update()        
            event = pygame.event.get()
            for i in event:
                if(i.type == pygame.QUIT):                                                                                                    
                    run = False
                    
                    

        #pygame.display.quit()
        pygame.quit()            
        arduino.close()
                


class Agua():
    def __init__(self,velocidad,x,y):
        self.x = x
        self.y = y
        self.vel = velocidad
        self.k = 0
        self.caida = y
        self.y_init = y
    
    def caer(self,win,animacion_gota):
        win.blit(animacion_gota[self.k//3],(self.x,self.caida))
        self.caida += self.vel
        self.k +=1
        if(self.k + 1 > 12):
            self.k=0
        if( self.caida >= 697):
            self.caida = self.y_init

class Arduino():
    def __init__(self):
        self.arduino = serial.Serial('COM4',9600)
        time.sleep(2)
        print("Conexion establecida")
    
    def leerArduino(self):        
        return self.arduino.readline().decode("ascii")
    
    def close(self):
        self.arduino.close()

class Calculos():
    #def __init__(self,secuencia):
        #self.secuencia = secuencia

    def __convertirBinario(self, secuencia):
        numero = 0
        exp = 1
        for i in range(len(secuencia)-1,-1,-1): 
            try:
                numero += int(secuencia[i])*exp
                exp *= 2        
            except :
                print(secuencia[i])
        return numero
    

    def calcularPorcentaje(self,secuencia):
        numero = self.__convertirBinario(secuencia)
        Vsal = numero * 0.019607
        v2 = 2.5 - (Vsal * 1/2)
        DR = (5-2*v2)*1000000/(5-v2)
        Rsen = 1000000 - DR
        HR = 100*Rsen/1000000
        HR = 100 - HR
        return HR



def main():
    
    interfaz = Interfaz(500,697)    
    interfaz.ejecutar()


if __name__ == "__main__":
    
        
    main()

#Configuración de la interfaz



