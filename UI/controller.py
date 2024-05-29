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
        pass



    def handle_volume(self, e):
        pass


    def handle_path(self, e):
        pass
