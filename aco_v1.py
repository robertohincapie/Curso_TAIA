# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:42:21 2023

@author: 000010478
"""
import numpy as np
import matplotlib.pyplot as plt

M=2 #Número de hormigas

class ant:
    def __init__(self, ro, v=1, dt=0.5, T=None, id=0):
        self.ro=ro
        self.ro_ant=ro
        self.angle=np.random.uniform(0,2*np.pi)
        self.v=v
        self.dt=dt
        self.estado='buscar'
        self.T=T
        self.id=id
        self.historia=[ro]   
    def hormiga_perdida(self):
        if(self.T.Z[int(self.ro[0]), int(self.ro[1])]==0): #Se salió de la región
            self.angle=np.random.uniform(0,2*np.pi)
            self.ro=self.T.ro.copy()
            self.estado='buscar'
    def mover_aleatorio(self):
        #print('Mover aleatorio')
        self.angle+=np.random.randn()*0.2
        self.ro=self.ro+self.dt*self.v*np.array([np.cos(self.angle),np.sin(self.angle)])
        self.historia.append(self.ro)
    def mover_hacia_comida(self):
        #print('Mover hacia comida')
        u=-self.T.phFood[int(self.ro[0])][int(self.ro[1])]/(np.linalg.norm(self.T.phFood[int(self.ro[0])][int(self.ro[1])])+1e-10)
        self.ro=self.ro+self.dt*self.v*u
        self.angle=np.arctan2(u[1], u[0])
        self.historia.append(self.ro)
    def mover_hacia_nido(self):
        #print('Mover hacia nido')
        u=self.T.phFood[int(self.ro[0])][int(self.ro[1])]/(np.linalg.norm(self.T.phFood[int(self.ro[0])][int(self.ro[1])])+1e-10)
        self.ro=self.ro+self.dt*self.v*u
        self.angle=np.arctan2(u[1], u[0])
        self.historia.append(self.ro)
    def buscar_nido(self):
        #print('Buscar nido')
        u=-self.T.ph[int(self.ro[0])][int(self.ro[1])]/(np.linalg.norm(self.T.ph[int(self.ro[0])][int(self.ro[1])])+1e-10)
        self.ro=self.ro+self.dt*self.v*u
        self.angle=np.arctan2(u[1], u[0])
        self.historia.append(self.ro)
    def cambiar_feromonas(self):
        if(self.estado=='buscar'):
            self.T.ph[int(self.ro[0])][int(self.ro[1])]=self.T.ph[int(self.ro[0])][int(self.ro[1])]+(self.ro-self.ro_ant)
        else:
            self.T.phFood[int(self.ro[0])][int(self.ro[1])]=self.T.phFood[int(self.ro[0])][int(self.ro[1])]+(self.ro-self.ro_ant)
            
    def mover(self):
        #print('Movimiento de hormiga: ', self.id)
        #print(self.ro)
        self.ro_ant=self.ro.copy()
        i,j=int(self.ro[0]),int(self.ro[1])
        if(self.estado=='buscar'):
            if(np.linalg.norm(self.T.phFood[int(self.ro[0])][int(self.ro[1])])==0 or np.random.rand()<0.1):
                self.mover_aleatorio()
            else: #Hay rastro hacia la comida
                self.mover_hacia_comida()
            self.cambiar_feromonas()
            #Verificar por comida en el entorno
            for rfi, comida, ind in zip(self.T.rf, self.T.comida, range(len(self.T.comida))):
                for di in     [-1,-1, -1, 0, 1,1, 1,  0]:
                    for dj in [-1, 0,  1, 1, 1,0,-1, -1]:
                        if(int(self.ro[0]+di)==rfi[0] and int(self.ro[1])+dj==rfi[1] and comida>0): #Encontró comida
                            self.estado='traer'
                            self.T.comida[ind]-=1
                        break
                    
        if(self.estado=='traer'):
            Feromonas_regreso=np.linalg.norm(self.T.phFood[i][j])
            Feromonas_busqueda=np.linalg.norm(self.T.ph[i][j])
            if(Feromonas_regreso>0 and Feromonas_regreso>Feromonas_busqueda):
                self.mover_hacia_nido()
            if(Feromonas_regreso==0 or Feromonas_regreso<Feromonas_busqueda):
                if(Feromonas_busqueda>0):
                    self.buscar_nido()
                else:
                    self.mover_aleatorio()
            #if(Feromonas_regreso==0 or Feromonas_regreso<Feromonas_busqueda):
            #    self.mover_aleatorio()
            self.cambiar_feromonas()
            if(int(self.ro[0])==self.T.ro[0] and int(self.ro[1])==self.T.ro[1]): #Ya regresó al hormiguero
                self.estado='buscar'
        self.hormiga_perdida()
        
class terreno:
    def __init__(self, L=80, M=10, ro=np.array([30,30]), rf=[np.array([10,20]), np.array([60,60]), np.array([60,62]), np.array([60,40]), np.array([60,41]), np.array([60,39])]):
        self.L=L
        self.M=M
        self.Z=np.zeros((L,L), dtype=int)
        self.ph=[[np.array([0,0]) for i in range(L)] for j in range(L)]
        self.phFood=[[np.array([0,0]) for i in range(L)] for j in range(L)]
        self.y, self.x=np.meshgrid(range(L), range(L))
        #Agregado de regiones propias del terreno
        esferas=[(L/2,L/2, L/4), (L/4,L/3, L/4), (3*L/4,3*L/4, L/4.5)]
        for i in range(len(self.x)):
            for j in range(len(self.x[0])):
                for xi, yi, ri in esferas: 
                    if((self.x[i,j]-xi)**2+(self.y[i,j]-yi)**2<ri**2):
                        self.Z[i,j]=1
                        #self.ph[i,j]=0
                        #self.phFood[i,j]=0
        self.ro=ro
        self.rf=rf
        self.comida=[50 for i in range(len(self.rf))]
        self.ants=[ant(ro=self.ro, T=self,id=i) for i in range(self.M)]
    
    def dibujar(self):
        xib=[a.ro[0] for a in self.ants if a.estado=='buscar']
        yib=[a.ro[1] for a in self.ants if a.estado=='buscar']
        xit=[a.ro[0] for a in self.ants if a.estado=='traer']
        yit=[a.ro[1] for a in self.ants if a.estado=='traer']
        
        plt.subplot(1,2,1)
        plt.gca().clear()
        Z=[[np.linalg.norm(self.ph[i][j]) for j in range(self.L)] for i in range(self.L)]
        plt.contourf(self.x, self.y, Z, vmin=0, cmap=plt.get_cmap('Blues'), levels=50)
        plt.plot(self.ro[0], self.ro[1], 'sr')
        for rfi, comida in zip(self.rf, self.comida):
            plt.plot(rfi[0], rfi[1], 'sg')
            plt.text(rfi[0], rfi[1], str(comida))
            
        plt.plot(xib,yib, '.k')
        plt.plot(xit,yit, '.r')
        plt.subplot(1,2,2)
        plt.gca().clear()
    
        Z=[[np.linalg.norm(self.phFood[i][j]) for j in range(self.L)] for i in range(self.L)]
        plt.contourf(self.x, self.y, Z, vmin=0, cmap=plt.get_cmap('Blues'), levels=50)
        plt.plot(self.ro[0], self.ro[1], 'sr')
        for rfi, comida in zip(self.rf, self.comida):
            plt.plot(rfi[0], rfi[1], 'sg')
            plt.text(rfi[0], rfi[1], str(comida))
        plt.plot(xib,yib, '.k')
        plt.plot(xit,yit, '.r')
        
        
    def mover(self):
        #self.ph+=(self.Z-1)
        for a in self.ants: 
            a.mover()
        Kev=0.95
        self.ph=[[self.ph[i][j]*Kev for j in range(self.L)] for i in range(self.L)]
        self.phFood=[[self.phFood[i][j]*Kev for j in range(self.L)] for i in range(self.L)]
            
plt.close('all')
plt.figure(figsize=(11,5))
T=terreno(M=200)
for i in range(1600):
    T.mover()
    T.dibujar()
    #plt.title(str(np.max(T.ph))+str(np.min(T.ph)))
    plt.pause(0.1)