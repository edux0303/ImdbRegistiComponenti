import networkx as nx
from itertools import combinations

from database.DAO import DAO
from model.regista import Regista


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._comp = {}
        self._solBest = []
        self._votiBest = -1
        self._n = 0

    def getGenres(self):
        return DAO.getGenres()

    # -------------------- PUNTO 1 --------------------

    def buildGraph(self, genere, voti):
        self._grafo.clear()
        self._idMap = {}

        # 1. registi, con film e voti (i voti di un film si sommano una volta sola)
        for row in DAO.getNodes(genere, voti):
            if row["id"] not in self._idMap:
                self._idMap[row["id"]] = Regista(row["id"], row["nome"])
            regista = self._idMap[row["id"]]
            if row["idFilm"] not in regista.film:
                regista.film.add(row["idFilm"])
                regista.voti += row["voti"]

        self._grafo.add_nodes_from(self._idMap.values())

        # 2. interpreti di ogni regista
        for idR, idI in DAO.getRegistiInterpreti(genere, voti):
            if idR in self._idMap:
                self._idMap[idR].interpreti.add(idI)

        # 3. archi: interpreti in comune
        for a, b in combinations(self._idMap.values(), 2):
            peso = len(a.interpreti & b.interpreti)
            if peso > 0:
                self._grafo.add_edge(a, b, weight=peso)

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda r: r.name)

    def getNumComponenti(self):
        return nx.number_connected_components(self._grafo)

    def getComponenteMax(self):
        # la componente più grande, come lista ordinata per nome
        piuGrande = max(nx.connected_components(self._grafo), key=len)
        return sorted(piuGrande, key=lambda r: r.name)

    """
    PUNTO 2
    a. L'utente sceglie un regista di partenza da ddRegista e inserisce in txtN un intero positivo N.

    b. Bottone "Trova Selezione": con un algoritmo RICORSIVO trovare un insieme di registi tale che
       - contiene ESATTAMENTE N registi;
       - il PRIMO è quello scelto dall'utente;
       - ogni regista appartiene a una COMPONENTE CONNESSA DIVERSA da quelle degli altri;
       - tra tutti gli insiemi ammissibili, MASSIMIZZA LA SOMMA DEI VOTI dei registi selezionati.

    c. Stampare:
       - i registi selezionati in ORDINE ALFABETICO, ciascuno con numero di film e voti;
       - il numero di registi;
       - i voti complessivi.
       Se ci sono meno di N componenti: messaggio.

    VALORI DI CONTROLLO (Action, V=10000)
    Anthony Russo  N=2 -> 1929101  (Anthony Russo, James Mangold)
    Anthony Russo  N=3 -> 2480346  (+ Ryan Coogler)
    Anthony Russo  N=4 -> 2991330  (+ James Gunn)
    Anthony Russo  N=5 -> 3498503  (+ Patty Jenkins)
    Ryan Coogler   N=2 -> 1879175  (Ryan Coogler + Anthony Russo O Joe Russo: pari merito)
    Fabrice du Welz N=3 -> 1939197 (Anthony/Joe Russo, Fabrice du Welz, James Mangold)

    Voti: Anthony Russo = Joe Russo 1327930 (stessa componente), James Mangold 601171,
          Ryan Coogler 551245, James Gunn 510984, Patty Jenkins 507173

    Comedy, V=10000: James Gunn N=3 -> 1231487 (Damien Chazelle, James Gunn, Peyton Reed)
                     James Gunn N=4 -> 1474247 (+ Matthew Vaughn)
    """

    def getSelezione(self,start,N):
        componenti = list(nx.connected_components(self._grafo))
        if start not in self._grafo or N < 1 or N > len(componenti):
            return None, None

        self._compId = {}
        for i, comp in enumerate(componenti):
            for a in comp:
                self._compId[a] = i
        self._solBest = []
        self._votiBest = -1

        self._ricorsione([start],N)

        return self._solBest, self._votiBest


    def _ricorsione(self,parziale,N):
        if len(parziale) == N:
            votoM = sum(r.voti for r in parziale)
            if votoM > self._votiBest:
                self._votiBest = votoM
                self._solBest = list(parziale)

            return
        for nodo in self._grafo.nodes :
            if nodo in parziale:
                continue
            usate = {self._compId[p] for p in parziale}
            if self._compId[nodo] in usate:
                continue
            parziale.append(nodo)
            self._ricorsione(parziale,N)
            parziale.pop()

"""
Punto 1:
- nodi = registi (director_mapping + names) con almeno un film del genere con >= V voti
- un oggetto Regista per id: se non è nell'idMap lo creo, poi aggiungo il film;
  i voti si sommano solo se il film è nuovo per quel regista
- interpreti dei registi con una query sola: director_mapping e role_mapping
  uniti sullo stesso film (d.movie_id = rm.movie_id), DISTINCT
- archi = interpreti in comune (combinations e intersezione dei set)
- Stampa Info: number_connected_components, max(connected_components, key=len),
  registi della più grande in ordine alfabetico con numero di film

Punto 2:
- N registi, primo fissato, ognuno in una componente connessa DIVERSA,
  massima somma dei voti (stile Chinook 29/06/2026 B)
- _compId = {regista: indice componente} con enumerate(connected_components)
- usate = {_compId[p] for p in parziale}; scarto se _compId[nodo] in usate
- caso finale len(parziale) == N: confronto con il best e return SEMPRE
- ERRORI FATTI: _ricorsione(nodo, N) invece di _ricorsione(parziale, N);
  "nodo in usate" invece di "_compId[nodo] in usate" (confronta un regista con dei numeri)

Controllo Action, V=10000: 105 nodi, 80 archi, 48 componenti (max 24)
Anthony Russo N=2 -> 1929101 (con James Mangold, NON Joe Russo) | N=3 -> 2480346



"""

