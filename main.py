import flet as ft
from flet import colors as Colors  
from flet import icons as Icons    
import datetime
import asyncio

# Forzamos compatibilidad global
ft.Colors = ft.colors
ft.Icons = ft.icons

async def main(page: ft.Page):
    page.title = "Google Suite Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.padding = 15

    # ==========================================
    # 1. SECCIÓN: RELOJ Y CRONÓMETRO
    # ==========================================
    lbl_clock_time = ft.Text("00:00:00", size=50, weight=ft.FontWeight.BOLD)
    lbl_clock_date = ft.Text("", size=16, color=ft.Colors.ON_SURFACE_VARIANT)
    lbl_chrono = ft.Text("00:00:00", size=40, weight=ft.FontWeight.BOLD)

    chrono_state = {"running": False, "s": 0, "m": 0, "h": 0}

    btn_chrono_start = ft.ElevatedButton(
        content=ft.Text("Iniciar"),
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )
    btn_chrono_reset = ft.OutlinedButton(content=ft.Text("Reiniciar"))

    async def toggle_chrono(e):
        chrono_state["running"] = not chrono_state["running"]
        btn_chrono_start.content.value = "Pausar" if chrono_state["running"] else "Iniciar"
        btn_chrono_start.bgcolor = ft.Colors.RED if chrono_state["running"] else ft.Colors.BLUE
        await page.update_async()

    async def reset_chrono(e):
        chrono_state.update({"running": False, "s": 0, "m": 0, "h": 0})
        lbl_chrono.value = "00:00:00"
        btn_chrono_start.content.value = "Iniciar"
        btn_chrono_start.bgcolor = ft.Colors.BLUE
        await page.update_async()

    btn_chrono_start.on_click = toggle_chrono
    btn_chrono_reset.on_click = reset_chrono

    view_clock = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ACCESS_TIME_FILLED, size=50, color=ft.Colors.BLUE),
                        lbl_clock_time,
                        lbl_clock_date
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                margin=ft.margin.only(top=30, bottom=40)
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Cronómetro", size=20, weight=ft.FontWeight.BOLD),
                        lbl_chrono,
                        ft.Row([btn_chrono_start, btn_chrono_reset], alignment=ft.MainAxisAlignment.CENTER)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=True
    )

    # ==========================================
    # 2. SECCIÓN: GALERÍA
    # ==========================================
    grid_photos = ft.GridView(expand=True, runs_count=3, spacing=8, run_spacing=8)

    async def open_gallery(e):
        await gallery_picker.pick_files_async(
            allow_multiple=True,
            file_type=ft.FilePickerFileType.IMAGE
        )

    async def display_gallery(e):
        if not e.files:
            return
        grid_photos.controls.clear()
        for f in e.files:
            grid_photos.controls.append(
                ft.Container(
                    content=ft.Image(src=f.path, fit=ft.ImageFit.COVER, border_radius=8),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                )
            )
        await page.update_async()

    gallery_picker = ft.FilePicker(on_result=display_gallery)

    btn_open_gallery = ft.FilledButton(
        content=ft.Text("Abrir Galería"),
        on_click=open_gallery
    )

    view_gallery = ft.Column(
        controls=[
            ft.Text("Google Galería", size=24, weight=ft.FontWeight.BOLD),
            btn_open_gallery,
            ft.Divider(),
            grid_photos
        ],
        expand=True,
        visible=False
    )

    # ==========================================
    # 3. SECCIÓN: EXPLORADOR DE ARCHIVOS
    # ==========================================
    list_files = ft.ListView(expand=True, spacing=4)

    async def open_files(e):
        await files_picker.pick_files_async(allow_multiple=True)

    async def display_files(e):
        if not e.files:
            return
        list_files.controls.clear()
        for f in e.files:
            list_files.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.INSERT_DRIVE_FILE, color=ft.Colors.BLUE_200),
                    title=ft.Text(f.name),
                    subtitle=ft.Text(f"{f.size} bytes" if f.size else "Tamaño desconocido")
                )
            )
        await page.update_async()

    files_picker = ft.FilePicker(on_result=display_files)

    btn_open_files = ft.FilledButton(
        content=ft.Text("Abrir Archivos"),
        on_click=open_files
    )

    view_files = ft.Column(
        controls=[
            ft.Text("Google Files", size=24, weight=ft.FontWeight.BOLD),
            btn_open_files,
            ft.Divider(),
            list_files
        ],
        expand=True,
        visible=False
    )

    # ==========================================
    # NAVEGACIÓN
    # ==========================================
    async def on_nav_change(e):
        idx = e.control.selected_index
        view_clock.visible = (idx == 0)
        view_gallery.visible = (idx == 1)
        view_files.visible = (idx == 2)
        await page.update_async()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationDestination(icon=ft.Icons.ACCESS_TIME, label="Reloj"),
            ft.NavigationDestination(icon=ft.Icons.IMAGE_OUTLINED, label="Galería"),
            ft.NavigationDestination(icon=ft.Icons.FOLDER_OPEN, label="Archivos")
        ]
    )

    # ==========================================
    # MOTOR DEL RELOJ (Compatibilidad Universal)
    # ==========================================
    async def clock_and_chrono_engine():
        while True:
            try:
                now = datetime.datetime.now()
                lbl_clock_time.value = now.strftime("%H:%M:%S")
                lbl_clock_date.value = now.strftime("%A, %d de %B")

                if chrono_state["running"]:
                    chrono_state["s"] += 1
                    if chrono_state["s"] >= 60:
                        chrono_state["s"] = 0
                        chrono_state["m"] += 1
                    if chrono_state["m"] >= 60:
                        chrono_state["m"] = 0
                        chrono_state["h"] += 1

                    lbl_chrono.value = f"{chrono_state['h']:02d}:{chrono_state['m']:02d}:{chrono_state['s']:02d}"

                await page.update_async()
                await asyncio.sleep(1)

            except Exception as ex:
                print("Error en el motor:", ex)
                break

    # Montaje seguro de Overlays
    page.overlay.extend([gallery_picker, files_picker])

    # Construcción asíncrona limpia
    await page.add_async(view_clock, view_gallery, view_files)
    
    # Iniciamos la tarea en segundo plano de manera nativa con asyncio
    asyncio.create_task(clock_and_chrono_engine())

# ==========================================
# CONFIGURACIÓN DE MONTAJE FASTAPI
# ==========================================
import flet_fastapi
app = flet_fastapi.app(main)
