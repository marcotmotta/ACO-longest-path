from copy import deepcopy
import numpy as np
import ants as at

#valor dos pesos de todas as arestas do grafo somados
pesoGrafo = 0

#le o arquivo e cria o grafo
def createGraph(path):
    auxFile = open(path, "r")
    raw = auxFile.readlines()
    auxFile.close()

    #formata os dados para melhor leitura
    for i in range(len(raw)):
        if '\n' in raw[i]:
            raw[i] = raw[i].replace('\n', '')
        raw[i] = raw[i].split('\t')

    grafo = {}

    #cria o grafo
    for i in range(len(raw)):
        if(raw[i][0] not in grafo):
            grafo[raw[i][0]] = []
        grafo[raw[i][0]].append((raw[i][1], raw[i][2], 1))

    aux = 0
    #calcula o peso total das arestas do grafo
    for key, value in grafo.items():
        for i in range(len(value)):
            aux += int(value[i][1])
        auxList = []
        for i in range(len(value)):
            auxList.append(list(value[i]))
        grafo[key] = auxList

    global pesoGrafo
    pesoGrafo = aux

    #retorna grafo pronto em formato de dicionario
    return grafo

#workflow
def movimento(ants, grafo, geracoes, evaporacao):
    for geracao in range(geracoes): #repete o algoritmos ate o numero definido de geracoes
        for i in range(ants.numAnts): #faz o movimento de cada formiga, individualmente
            for j in range(1, len(grafo)):
                if(ants.ants[i].noAtual == str(len(grafo))): #chegou no vertine n
                    break
                #escolhe proxima aresta do movimento da formiga
                aresta = escolheAresta(grafo, ants.ants[i].noAtual, ants.ants[i])
                if(aresta == 'none'): #nao tem mais arestas possiveis para ir
                    break
                ants.ants[i].noAtual = aresta[0]
        #atualiza os feromonios e roda o algoritmo de novo
        atualizaFeromonio(grafo, ants, evaporacao)
    #seleciona melhor caminho ao final de todas as iteracoes
    caminhos(grafo, ants)

#escolhe proxima aresta do movimento atraves da funcao de probabilidade
def escolheAresta(grafo, noAtual, ant):
    arestas = []
    probabilidades = []
    denominador = 0
    for j in range(len(grafo[noAtual])):
        #escolhe apenas arestas que nao foram passadas ainda (eliminando repeticoes)
        if(grafo[noAtual][j][0] not in ant.caminho):
            #adiciona pesos e feromonios totais na funcao de probabilidade
            denominador += float(grafo[noAtual][j][1]) * float(grafo[noAtual][j][2])
    for i in range(len(grafo[noAtual])):
        #escolhe apenas arestas que nao foram passadas ainda (eliminando repeticoes)
        if(grafo[noAtual][i][0] not in ant.caminho):
            arestas.append(grafo[noAtual][i][0])
            #adiciona pesos e feromonios da aresta atual na funcao de probabilidade
            probAresta = (float(grafo[noAtual][i][1]) * float(grafo[noAtual][i][2])) / denominador
            probabilidades.append(probAresta)
    #verifica se ainda existem arestas disponiveis para escolha
    if(arestas == []):
        return 'none'
    #escolhe aresta baseada na funcao de probabilidade gerada
    posicao = np.random.choice(arestas, 1, p = probabilidades)
    #adiciona aresta escolhida no caminho da formiga atual
    ant.caminho.append(posicao[0])
    return posicao

def atualizaFeromonio(grafo, ants, evaporacao):
    for i in range(ants.numAnts):
        pesoCaminho = 0
        #procura os pesos dos caminhos das formigas
        for j in range(len(ants.ants[i].caminho) - 1):
            for value in grafo[ants.ants[i].caminho[j]]:
                if(value[0] == ants.ants[i].caminho[j+1]):
                    #armazena apenas o peso das arestas presentes nos caminhos validos
                    pesoCaminho += int(value[1])
                    break
        custoFinal = pesoCaminho / pesoGrafo
        #atualiza o feromonio de cada caminho
        for j in range(len(ants.ants[i].caminho) - 1):
            for value in grafo[ants.ants[i].caminho[j]]:
                if(value[0] == ants.ants[i].caminho[j+1]):
                    #atualiza apenas o feromonio pertencente a formigas que
                    #realizaram caminhos validos
                    value[2] = str(float(value[2]) * (1-evaporacao) + custoFinal)

def caminhos(grafo, ants):
    pesoMax = 0
    #verifica melhores caminhos entre as solucoes atuais obtidas
    for i in range(ants.numAnts):
        pesoCaminho = 0
        for j in range(len(ants.ants[i].caminho) - 1):
            for value in grafo[ants.ants[i].caminho[j]]:
                if(value[0] == ants.ants[i].caminho[j+1]):
                    pesoCaminho += int(value[1])
                    break
        if(pesoCaminho > pesoMax):
            pesoMax = pesoCaminho

    print ('melhor caminho: ', pesoMax)