import sys
import grafo as gf
import numpy as np
import ants as at

if __name__ == "__main__":
    
    #selecionar a seed para teste do algoritmo
    #random.seed(42)

    numAnts = int(sys.argv[1]) #numero de formigas
    numGeracoes = int(sys.argv[2]) #numero de geracoes
    evaporacao = float(sys.argv[3]) #taxa de evaporacao do feromonio

    path = sys.argv[4] #arquivo de entrada

    grafo = gf.createGraph(path) #gera o grafo atraves do arquivo
    ants = at.Colony(numAnts) #gera a populacao de formigas

    gf.movimento(ants, grafo, numGeracoes, evaporacao) #workflow do algoritmo