import flet as ft

def criar_aba_configuracoes(estado, pagina: ft.Page):
    
    # --- Lógica de Persistência ---

    def mudar_tema(e):
        is_dark = e.control.value
        pagina.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        pagina.update()
        pagina.client_storage.set("tema_escuro", is_dark)

    def mudar_precisao(e):
        pagina.client_storage.set("precisao_decimal", e.control.value)
        pagina.snack_bar = ft.SnackBar(content=ft.Text("Precisão salva! Recalcule para aplicar."), bgcolor="green")
        pagina.snack_bar.open = True
        pagina.update()

    def mudar_cor_padrao(e):
        pagina.client_storage.set("cor_padrao_grafico", e.control.value)
        pagina.snack_bar = ft.SnackBar(content=ft.Text("Cor padrão atualizada para novos gráficos."), bgcolor="green")
        pagina.snack_bar.open = True
        pagina.update()

    def mudar_grades(e):
        pagina.client_storage.set("exibir_grades", e.control.value)
        pagina.update()

    def mudar_orientacao(e):
        pagina.client_storage.set("orientacao_grafico", e.control.value)
        pagina.update()

    # --- Carregamento Inicial ---
    
    tema_salvo = pagina.client_storage.get("tema_escuro")
    if tema_salvo is None:
        tema_salvo = pagina.theme_mode == ft.ThemeMode.DARK
    
    # PADRÃO AGORA É "Auto" (Indefinido/Automático)
    precisao_salva = pagina.client_storage.get("precisao_decimal")
    if precisao_salva is None:
        precisao_salva = "Auto"

    cor_salva = pagina.client_storage.get("cor_padrao_grafico") or "#ADD8E6"
    
    grades_salvo = pagina.client_storage.get("exibir_grades")
    if grades_salvo is None: grades_salvo = True 

    orientacao_salva = pagina.client_storage.get("orientacao_grafico") or "Vertical"

    # --- Componentes UI ---

    switch_tema = ft.Switch(
        label="Habilitar Modo Escuro",
        value=tema_salvo,
        on_change=mudar_tema
    )

    switch_grades = ft.Switch(
        label="Exibir Linhas de Grade",
        value=grades_salvo,
        on_change=mudar_grades,
        active_color=ft.Colors.BLUE
    )

    dropdown_precisao = ft.Dropdown(
        width=150,
        value=precisao_salva,
        options=[
            # NOVA OPÇÃO: Automático
            ft.dropdown.Option("Auto", "Automático (Detectar)"),
            ft.dropdown.Option("0", "0 casas (Inteiro)"),
            ft.dropdown.Option("1", "1 casa"),
            ft.dropdown.Option("2", "2 casas"),
            ft.dropdown.Option("3", "3 casas"),
            ft.dropdown.Option("4", "4 casas"),
            ft.dropdown.Option("6", "6 casas"),
        ],
        on_change=mudar_precisao,
        border_color=ft.Colors.GREY_700,
        content_padding=10
    )

    dropdown_orientacao = ft.Dropdown(
        width=150,
        value=orientacao_salva,
        options=[
            ft.dropdown.Option("Vertical", "Vertical ( | )"),
            ft.dropdown.Option("Horizontal", "Horizontal ( — )"),
        ],
        on_change=mudar_orientacao,
        border_color=ft.Colors.GREY_700,
        content_padding=10
    )

    dropdown_cor_default = ft.Dropdown(
        width=180,
        value=cor_salva,
        options=[
            ft.dropdown.Option("#ADD8E6", "Azul Claro (Padrão)"),
            ft.dropdown.Option("#90EE90", "Verde"),
            ft.dropdown.Option("#FFB6C1", "Rosa Claro"),
            ft.dropdown.Option("#D3D3D3", "Cinza"),
            ft.dropdown.Option("#FFA07A", "Salmão"),
        ],
        on_change=mudar_cor_padrao,
        border_color=ft.Colors.GREY_700,
        content_padding=10
    )

    # --- Função Auxiliar para Criar Cards ---
    def criar_card_config(icone, titulo, subtitulo, controle):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icone, size=32, color=ft.Colors.GREY_400),
                ft.Container(width=15),
                ft.Column([
                    ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(subtitulo, size=12, color=ft.Colors.GREY),
                ], spacing=2, expand=True),
                controle
            ], alignment=ft.MainAxisAlignment.START),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_800),
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.GREY)
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Configurações", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(color=ft.Colors.GREY_800),
                ft.Container(height=10),
                criar_card_config(ft.Icons.BRIGHTNESS_6, "Aparência", "Alternar entre temas claro e escuro", switch_tema),
                ft.Container(height=25),
                ft.Text("Visualização do Gráfico", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=5),
                criar_card_config(ft.Icons.GRID_ON, "Linhas de Grade", "Facilita a leitura dos valores", switch_grades),
                ft.Container(height=10),
                criar_card_config(ft.Icons.ROTATE_90_DEGREES_CCW, "Orientação", "Eixo do gráfico", dropdown_orientacao),
                ft.Container(height=10),
                criar_card_config(ft.Icons.COLOR_LENS, "Cor Padrão", "Cor inicial", dropdown_cor_default),
                ft.Container(height=25),
                ft.Text("Cálculos", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=5),
                criar_card_config(ft.Icons.FUNCTIONS, "Precisão Decimal", "Casas decimais (Auto detecta dos dados)", dropdown_precisao),
                ft.Container(height=30),
            ],
            scroll=ft.ScrollMode.AUTO
        ),
        padding=30,
        alignment=ft.alignment.top_left,
        expand=True
    )