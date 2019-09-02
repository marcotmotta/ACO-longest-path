from copy import deepcopy
import numpy as np
import grafo as gf

#classe que representa o conjunto de formigas
class Colony:
    def __init__(self, num):
        self.ants = [] #conjunto de solucoes
        self.numAnts = num #numero de formigas

        #inicializa solucoes com valores vazios
        for i in range(self.numAnts):
            ant = deepcopy(Ant())
            self.ants.append(ant)

#classe que representa uma unica formiga
class Ant:
    def __init__(self):
        self.caminho = ['1'] #caminho atual, iniciando sempre no vertice 1 do grafo
        self.noAtual = '1' #ultimo no visitado pela formiga (variavel auxiliar)