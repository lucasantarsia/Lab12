from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = [2015, 2016, 2017, 2018]
        self._listCountry = self._model._allCountries

    def fillDD(self):
        # Riempio ddyear
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(str(y)))

        # Riempio ddcountry
        for c in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(str(c)))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._view.txtOut2.controls.clear()
        self._view.txtOut3.controls.clear()
        if self._view.ddyear.value is None or self._view.ddcountry.value is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno e un paese!"))
            self._view.update_page()
            return
        self._model.buildGraph(self._view.ddcountry.value, int(self._view.ddyear.value))

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero dei vertici: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero degli archi: {self._model.getNumEdges()}"))
        self._view.btn_volume.disabled = False
        self._view.update_page()



    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        listTuple = self._model.getVolumeRetailer()
        for retailer, volume in listTuple:
            self._view.txtOut2.controls.append(ft.Text(f"{retailer} --> {volume}"))
        self._view.txtN.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):
        self._view.txtOut3.controls.clear()
        try:
            N_int = int(self._view.txtN.value)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text(f"Inserire un numero intero maggiore o uguale a 2!"))
            self._view.update_page()
            return
        if N_int < 2:
            self._view.txtOut3.controls.append(ft.Text(f"Inserire un numero intero maggiore o uguale a 2!"))
            self._view.update_page()
            return
        tic = datetime.now()
        camminoOttimo, pesoOttimo = self._model.getBestPath(N_int)
        print(f"Tempo impiegato: {(datetime.now() - tic)}")
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {pesoOttimo}"))
        for i in range(0, len(camminoOttimo)-1):
            r1, r2 = camminoOttimo[i], camminoOttimo[i+1]
            self._view.txtOut3.controls.append(ft.Text(f"{r1} --> {r2}: "
                                                       f"{self._model._grafo[camminoOttimo[i]][camminoOttimo[i+1]]["weight"]}"))
        self._view.update_page()
