import flet as ft

def criar_aba_dev(page: ft.Page):

    backend = ft.Container(
        content=ft.Column([
            ft.Text("Back-End", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
            ft.Text("(Lógica de Cálculos Estatísticos e Banco de Dados)", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
            ft.Text("Pedro Henrique Silva do Nascimento", size=18),
            ft.Text("Yuri Nascimento Pinheiro", size=18),
            ft.Text("Kauã de Sousa Campos", size=18),
            ft.Text("Wanderson Carvalho da Silva Júnior", size=18),
            ft.Text("Paulo Henrique Andrade Chaveiro", size=18)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        border=ft.border.all(2, ft.Colors.BLUE_200),
        border_radius=10,
        width=720,
        alignment=ft.alignment.center
    )

    frontend = ft.Container(
        content=ft.Column([
            ft.Text("Front-End", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
            ft.Text("(Visualização do Gráfico e Interface do Programa)", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
            ft.Text("Ricardo Gomes da Silva", size=18),
            ft.Text("Weberth Silva de Souza", size=18),
            ft.Text("Eric Faria dos Santos", size=18),
            ft.Text("Pedro Henrique da Silva Sousa", size=18),
            ft.Text("Brian Gustavo Rodrigues Ribeiro", size=18)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
            border=ft.border.all(2, ft.Colors.BLUE_200),
            border_radius=10,
            width=720,
            alignment=ft.alignment.center
    )

    return ft.Column(
        [
            ft.Text("Créditos de Desenvolvimento", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Divider(height=20, thickness=2, color=ft.Colors.BLUE_GREY_100),
            
            backend,
            ft.Container(height=30), 
            frontend
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.ADAPTIVE, 
        expand=True
    )