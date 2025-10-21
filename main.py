import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")
    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    # Sezione 3: Aggiunta auto
    lbl_aggiungi=ft.Text(value="aggiungi nuova automobile", size=20)
    marca_input = ft.TextField(label="Marca", width=150)
    modello_input = ft.TextField(label="Modello", width=150)
    anno_input = ft.TextField(label="Anno", width=100)
    contatore=ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)


    def minus_click(e):
        contatore.value = str(int(contatore.value) - 1)
        page.update()

    def plus_click(e):
        contatore.value = str(int(contatore.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                contatore.value,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER, spacing=10
        )
    )

    btn_aggiungi_auto = ft.ElevatedButton("Aggiungi Automobile")
    def aggiungi_auto(e):
        marca = marca_input.value.strip()
        modello = modello_input.value.strip()
        anno = anno_input.value.strip()
        posti = contatore.value.strip()

        if not marca or not modello or not anno or not posti:
            alert.show_alert("Tutti i campi devono essere compilati.")
            return

        try:
            anno = int(anno)
        except ValueError:
            alert.show_alert("Il campo 'Anno' deve essere un numero intero.")
            return

        try:
            posti = int(posti)
        except ValueError:
            alert.show_alert("Il numero di posti deve essere un numero intero.")
            return

        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
            marca_input.value = ""
            modello_input.value = ""
            anno_input.value = ""
            contatore.value = "0"
            aggiorna_lista_auto()
            page.update()
        except Exception as ex:
            alert.show_alert(f"Errore durante l'aggiunta: {ex}")

    btn_aggiungi_auto = ft.ElevatedButton("Aggiungi Automobile", on_click=aggiungi_auto)

    # --- FUNZIONI ---

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("aggiungi automobile", size=20),
        ft.Row(spacing=50,
               controls=[marca_input, modello_input, anno_input, contatore],
               alignment=ft.MainAxisAlignment.CENTER),
        btn_aggiungi_auto,


        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
