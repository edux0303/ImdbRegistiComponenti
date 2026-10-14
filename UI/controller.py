import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDGeneri(self):
        for g in self._model.getGenres():
            self._view._ddGenere.options.append(ft.dropdown.Option(g))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        genere = self._view._ddGenere.value
        if genere is None:
            self._errore("Seleziona un genere!")
            return
        try:
            voti = int(self._view._txtV.value)
        except (ValueError, TypeError):
            self._errore("V deve essere un intero!")
            return
        if voti < 0:
            self._errore("V non può essere negativo!")
            return

        self._model.buildGraph(genere, voti)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {genere}, almeno {voti} voti"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._ddRegista.options.clear()
        self._view._ddRegista.value = None
        for r in self._model.getNodiOrdinati():
            self._view._ddRegista.options.append(ft.dropdown.Option(key=r.id, text=r.name))
        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {self._model.getNumComponenti()}"))

        componente = self._model.getComponenteMax()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente più grande ha {len(componente)} registi:"))
        for r in componente:
            self._view.txt_result.controls.append(ft.Text(f"{r.name} - film: {len(r.film)}"))
        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleTrovaSelezione(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        idRegista = self._view._ddRegista.value
        if idRegista is None:
            self._errore("Seleziona un regista di partenza!")
            return
        partenza = self._model._idMap[idRegista]

        try:
            n = int(self._view._txtN.value)
        except (ValueError, TypeError):
            self._errore("N deve essere un intero!")
            return
        if n < 1:
            self._errore("N deve essere almeno 1!")
            return

        numComp = self._model.getNumComponenti()
        if n > numComp:
            self._errore(f"Ci sono solo {numComp} componenti: non si possono scegliere {n} registi.")
            return

        selezione, voti = self._model.getSelezione(partenza, n)
        if selezione is None or len(selezione) == 0:
            self._errore("Nessuna selezione valida trovata.")
            return

        self._view.txt_result.controls.append(ft.Text(f"Selezione partendo da {partenza}:"))
        for r in sorted(selezione, key=lambda x: x.name):
            self._view.txt_result.controls.append(
                ft.Text(f"{r.name} - film: {len(r.film)}, voti: {r.voti}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di registi: {len(selezione)}"))
        self._view.txt_result.controls.append(ft.Text(f"Voti complessivi: {voti}"))
        self._view.update_page()