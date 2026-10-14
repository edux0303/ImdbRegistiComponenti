import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Registi Componenti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self._title = None
        self._ddGenere = None
        self._txtV = None
        self._btnCreaGrafo = None
        self._btnStampaInfo = None
        self._ddRegista = None
        self._txtN = None
        self._btnTrovaSelezione = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Registi in componenti diverse", color="blue", size=24)
        self._page.controls.append(self._title)

        # PUNTO 1
        self._ddGenere = ft.Dropdown(label="Genere", width=200)
        self._txtV = ft.TextField(label="Min voti V", width=150, value="10000")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                on_click=self._controller.handleStampaInfo)
        row1 = ft.Row([self._ddGenere, self._txtV, self._btnCreaGrafo, self._btnStampaInfo],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # PUNTO 2
        self._ddRegista = ft.Dropdown(label="Regista di partenza", width=350)
        self._txtN = ft.TextField(label="N registi", width=130)
        self._btnTrovaSelezione = ft.ElevatedButton(text="Trova Selezione",
                                                    on_click=self._controller.handleTrovaSelezione)
        row2 = ft.Row([self._ddRegista, self._txtN, self._btnTrovaSelezione],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

        # i generi si possono caricare subito, i registi solo dopo "Crea Grafo"
        self._controller.fillDDGeneri()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()