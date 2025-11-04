import flet as ft
from UI.alert import AlertManager
'''
    VIEW:
    - Rappresenta l'interfaccia utente
    - Riceve i dati dal MODELLO e li presenta senza modificarli
'''

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab06"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

        # Elementi UI
        self.txt_titolo = None
        self.txt_responsabile = None

        # Non obbligatorio mettere già qui tutti gli elementi UI

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        """ Imposta il controller alla pagina """
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge Elementi di UI alla pagina e la aggiorna. """
        self.txt_titolo = ft.Text(value=self.controller.get_nome(), size=38, weight=ft.FontWeight.BOLD)
        self.txt_responsabile = ft.Text(
            value=f"Responsabile: {self.controller.get_responsabile()}",
            size=16,
            weight=ft.FontWeight.BOLD
        )

        # TextField per responsabile
        self.input_responsabile = ft.TextField(value=self.controller.get_responsabile(), label="Responsabile",width=400)

        # ListView per mostrare la lista di auto aggiornata
        self.lista_auto = ft.ListView(spacing=5, padding=10, auto_scroll=True, height=250, width=600)

        # TextField per ricerca auto per modello
        self.input_modello_auto = ft.TextField(label="Modello", width=400)

        # ListView per mostrare il risultato della ricerca auto per modello
        self.lista_auto_ricerca = ft.ListView(spacing=5, padding=10, auto_scroll=True, height=250, width=600)

        # --- PULSANTI e TOGGLE associati a EVENTI ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)
        pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=self.controller.conferma_responsabile)

        # Altri Pulsanti da implementare (es. "Mostra" e "Cerca")
        # TODO
        self.pulsante_mostra = ft.ElevatedButton("Mostra", on_click=self.controller.handle_mostra_automobili)
        self.pulsante_cerca = ft.ElevatedButton("Cerca", on_click = self.controller.handle_cerca_automobili)

        # --- LAYOUT ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            self.txt_responsabile,
            ft.Divider(),

            # Sezione 2
            ft.Text("Modifica Informazioni", size=20),
            ft.Row(spacing=200,
                   controls=[self.input_responsabile, pulsante_conferma_responsabile],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),

            # Sezione 3
            # TODO
            ft.Text("Automobili", size=20),
            self.pulsante_mostra,
            ft.Row(
                controls=[self.lista_auto],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Divider(),

            # Sezione 4
            # TODO
            ft.Text("Cerca Automobile", size=20),
            ft.Row(
                controls=[self.input_modello_auto, self.pulsante_cerca],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            ft.Row(
                controls=[self.lista_auto_ricerca],
                alignment=ft.MainAxisAlignment.CENTER
            )

        )

    def cambia_tema(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
    
    def update_lista_auto(self, automobili):
        self.lista_auto.controls.clear()
        if not automobili:
            self.lista_auto.controls.append(ft.Text("Nessuna automobile trovata nel database."))
        else:
            for auto in automobili:
                stato = "DISPONIBILE" if auto.disponibile else "NON DISPONIBILE"
                self.lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        self.update()

    def update_lista_ricerca(self, automobili):
        """ Popola la ListView della Sezione 4 con i dati dal controller. """
        self.lista_auto_ricerca.controls.clear()
        if not automobili:
            self.lista_auto_ricerca.controls.append(ft.Text("Nessuna automobile trovata per questo modello."))
        else:
            for auto in automobili:
                stato = "DISPONIBILE" if auto.disponibile else "NON DISPONIBILE"
                self.lista_auto_ricerca.controls.append(ft.Text(f"{stato} {auto}"))
        self.update()
