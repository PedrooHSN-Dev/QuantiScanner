import flet as ft

def criar_aba_resultados(estado, pagina):
    
    # ---  Definição dos Componentes de UI  ---
    
    imagem_boxplot = ft.Image(src_base64="", width=700, height=500, fit=ft.ImageFit.CONTAIN)
    
    campo_titulo_grafico = ft.TextField(label="Título", width=250, value="Distribuição dos Dados")
    campo_label_y = ft.TextField(label="Rótulo Eixo", width=150, value="Valores")
    
    dropdown_cor = ft.Dropdown(
        label="Cor",
        width=150,
        options=[
            ft.dropdown.Option("#ADD8E6", "Azul Claro"),
            ft.dropdown.Option("#90EE90", "Verde Claro"),
            ft.dropdown.Option("#FFB6C1", "Rosa Claro"),
            ft.dropdown.Option("#FFD700", "Dourado"),
            ft.dropdown.Option("#FFA07A", "Salmão"),
            ft.dropdown.Option("#D3D3D3", "Cinza"),
            ft.dropdown.Option("#FFFFFF", "Branco"),
        ],
        value="#ADD8E6"
    )

    campo_q1 = ft.TextField(label="Q1", read_only=True)
    campo_q2 = ft.TextField(label="Q2", read_only=True)
    campo_q3 = ft.TextField(label="Q3", read_only=True)
    campo_iqr = ft.TextField(label="IQR", read_only=True)

    tabela_decis = ft.DataTable(columns=[ft.DataColumn(ft.Text("Decil")), ft.DataColumn(ft.Text("Valor"))], rows=[])
    tabela_percentis = ft.DataTable(columns=[ft.DataColumn(ft.Text("Percentil")), ft.DataColumn(ft.Text("Valor"))], rows=[])
    
    campo_nome_analise = ft.TextField(label="Nome da Análise", width=350)

    placeholder_view = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                ft.Text(
                    "Execute uma análise na aba 'Entrada de Dados' para ver os resultados aqui.",
                    size=18, color="grey", text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )
    
    view_resultados = ft.Column(visible=False, scroll=ft.ScrollMode.ADAPTIVE, spacing=20)


    def atualizar_view():
        if not estado.metricas_atuais:
            placeholder_view.visible = True
            view_resultados.visible = False
            imagem_boxplot.src_base64 = None
            # Limpeza dos campos...
            for campo in [campo_q1, campo_q2, campo_q3, campo_iqr]: campo.value = ""
            tabela_decis.rows.clear()
            tabela_percentis.rows.clear()
            pagina.update()
            return

        # --- Lógica de Preferências ---
        
        # 1. Precisão Decimal
        precisao = int(pagina.client_storage.get("precisao_decimal") or 4)
        formato = f".{precisao}f"

        # 2. Cor Padrão
        cor_salva = pagina.client_storage.get("cor_padrao_grafico")
        if cor_salva and dropdown_cor.value == "#ADD8E6": 
             dropdown_cor.value = cor_salva
        
        # 3. Recuperar Grade e Orientação
        usar_grades = pagina.client_storage.get("exibir_grades")
        if usar_grades is None: usar_grades = True # Padrão True se não existir
        
        orientacao = pagina.client_storage.get("orientacao_grafico")
        eh_horizontal = (orientacao == "Horizontal")

        # --- Fim da Lógica de Preferências ---

        campo_titulo_grafico.value = estado.config_grafico.get('titulo', 'Distribuição dos Dados')
        campo_label_y.value = estado.config_grafico.get('label_y', 'Valores')
        dropdown_cor.value = estado.config_grafico.get('cor', dropdown_cor.value)

        # Gera o gráfico passando os novos parâmetros
        if not estado.boxplot_atual:
            estado.boxplot_atual = estado.motor_analise.gerar_boxplot(
                titulo=campo_titulo_grafico.value,
                label_y=campo_label_y.value,
                cor=dropdown_cor.value,
                horizontal=eh_horizontal,
                exibir_grades=usar_grades
            )
        
        imagem_boxplot.src_base64 = estado.boxplot_atual

        # Preencher campos com formatação
        quartis = estado.metricas_atuais['quartis']
        campo_q1.value = f"{quartis['Q1']:{formato}}"
        campo_q2.value = f"{quartis['Q2 (Mediana)']:{formato}}"
        campo_q3.value = f"{quartis['Q3']:{formato}}"
        campo_iqr.value = f"{quartis['Intervalo Interquartil (IQR)']:{formato}}"

        # Preencher tabelas com formatação
        decis = estado.metricas_atuais['tabelas_resumo']['decis']
        tabela_decis.rows.clear()
        tabela_decis.rows.extend([
            ft.DataRow(cells=[ft.DataCell(ft.Text(item['decil'])), ft.DataCell(ft.Text(f"{item['valor']:{formato}}"))])
            for item in decis
        ])

        percentis = estado.metricas_atuais['tabelas_resumo']['percentis']
        tabela_percentis.rows.clear()
        tabela_percentis.rows.extend([
            ft.DataRow(cells=[ft.DataCell(ft.Text(item['percentil'])), ft.DataCell(ft.Text(f"{item['valor']:{formato}}"))])
            for item in percentis
        ])

        placeholder_view.visible = False
        view_resultados.visible = True
        pagina.update()

    def atualizar_grafico_personalizado(e):
        if not estado.metricas_atuais:
            return

        # Recuperar preferências para o botão "Atualizar" também
        usar_grades = pagina.client_storage.get("exibir_grades")
        if usar_grades is None: usar_grades = True
        
        orientacao = pagina.client_storage.get("orientacao_grafico")
        eh_horizontal = (orientacao == "Horizontal")

        try:
            estado.boxplot_atual = estado.motor_analise.gerar_boxplot(
                titulo=campo_titulo_grafico.value, 
                label_y=campo_label_y.value,
                cor=dropdown_cor.value,
                horizontal=eh_horizontal,
                exibir_grades=usar_grades
            )
            imagem_boxplot.src_base64 = estado.boxplot_atual
            
            # Atualiza config global para salvar depois
            estado.config_grafico['cor'] = dropdown_cor.value
            estado.config_grafico['titulo'] = campo_titulo_grafico.value
            
            pagina.snack_bar = ft.SnackBar(content=ft.Text("Gráfico atualizado!"), bgcolor="blue")
            pagina.snack_bar.open = True
            pagina.update()
        except Exception as err:
            pagina.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao atualizar: {err}"), bgcolor="red")
            pagina.snack_bar.open = True
            pagina.update()

    def salvar_analise(e):
        nome_analise = campo_nome_analise.value
        if not nome_analise:
            pagina.snack_bar = ft.SnackBar(content=ft.Text("Dê um nome para a análise."), bgcolor="red")
            pagina.snack_bar.open = True
            pagina.update()
            return
        try:
            estado.config_grafico = {
                'titulo': campo_titulo_grafico.value,
                'label_y': campo_label_y.value,
                'cor': dropdown_cor.value
            }
            
            dados_completos = {
                **estado.metricas_atuais,
                'config_grafico': estado.config_grafico
            }
            
            estado.gerenciador_bd.salvar_analise(nome_analise, dados_completos)
            pagina.snack_bar = ft.SnackBar(content=ft.Text(f"Salvo: {nome_analise}"), bgcolor="green")
            if estado.callback_atualizar_view_historico:
                estado.callback_atualizar_view_historico()
            campo_nome_analise.value = ""
        except Exception as err:
            pagina.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao salvar: {err}"), bgcolor="red")
        pagina.snack_bar.open = True
        pagina.update()

    def processar_exportacao(e: ft.FilePickerResultEvent):
        if not e.path:
            return
        try:
            tipo_exportacao = seletor_arquivo.data
            
            if tipo_exportacao == "csv":
                estado.motor_analise.exportar_metricas_para_csv(estado.metricas_atuais, e.path)
                msg = "CSV exportado!"
            elif tipo_exportacao == "pdf":
                estado.motor_analise.exportar_relatorio_completo_para_pdf(estado.metricas_atuais, estado.boxplot_atual, e.path)
                msg = "PDF exportado!"
            elif tipo_exportacao == "png":
                import base64
                img_bytes = base64.b64decode(estado.boxplot_atual)
                with open(e.path, 'wb') as f:
                    f.write(img_bytes)
                msg = "PNG exportado!"
            pagina.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor="green")
        except Exception as err:
            pagina.snack_bar = ft.SnackBar(content=ft.Text(f"Erro: {err}"), bgcolor="red")
        pagina.snack_bar.open = True
        pagina.update()

    # ---  Montagem da Interface e Callbacks ---
    
    estado.callback_atualizar_view_resultados = atualizar_view
    
    seletor_arquivo = ft.FilePicker(on_result=processar_exportacao)
    pagina.overlay.append(seletor_arquivo)

    btn_atualizar_grafico = ft.ElevatedButton("Atualizar", icon=ft.Icons.REFRESH, on_click=atualizar_grafico_personalizado)
    
    btn_salvar = ft.ElevatedButton("Salvar", on_click=salvar_analise, icon=ft.Icons.SAVE)
    
    def exportar_csv(e):
        seletor_arquivo.data = "csv"
        seletor_arquivo.save_file(file_name="metricas.csv")

    def exportar_pdf(e):
        seletor_arquivo.data = "pdf"
        seletor_arquivo.save_file(file_name="relatorio.pdf")

    def exportar_png(e):
        seletor_arquivo.data = "png"
        seletor_arquivo.save_file(file_name="grafico.png")

    btn_csv = ft.ElevatedButton("CSV", on_click=exportar_csv, icon=ft.Icons.TABLE_VIEW)
    btn_pdf = ft.ElevatedButton("PDF", on_click=exportar_pdf, icon=ft.Icons.PICTURE_AS_PDF)
    btn_png = ft.ElevatedButton("PNG", on_click=exportar_png, icon=ft.Icons.IMAGE)

    view_resultados.controls = [
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.PALETTE, color="grey"),
                    campo_titulo_grafico,
                    campo_label_y,
                    dropdown_cor,
                    btn_atualizar_grafico
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            ),
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREY),
            border_radius=10
        ),
        ft.Row(
            controls=[
                ft.Container(
                    content=imagem_boxplot,
                    border=ft.border.all(1, color="grey"), border_radius=10, padding=25,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Decis", size=20, weight=ft.FontWeight.BOLD), bgcolor="lightgrey", padding=10, border_radius=ft.border_radius.only(top_left=20, top_right=10)),
                        tabela_decis
                    ]),
                    border=ft.border.all(1), border_radius=20,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Percentis", size=30, weight=ft.FontWeight.BOLD), bgcolor="lightgrey", padding=30, border_radius=ft.border_radius.only(top_left=20, top_right=10)),
                        ft.Column([tabela_percentis], scroll=ft.ScrollMode.ADAPTIVE, height=350)
                    ]),
                    border=ft.border.all(1), border_radius=20,
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        ft.Row(
            controls=[
                    ft.Container(
                    content=ft.Column([
                        ft.Container(ft.Text("Quartis", size=20, weight=ft.FontWeight.BOLD), bgcolor="lightgrey", padding=15, border_radius=ft.border_radius.only(top_left=10, top_right=10)),
                        ft.Row([campo_q1, campo_q3]),
                        ft.Row([campo_q2, campo_iqr])
                    ]),
                    border=ft.border.all(1), border_radius=5, padding=15,
                )
            ]
        ),
        ft.Divider(),
        ft.Row(
            controls=[
                campo_nome_analise,
                btn_salvar,
                btn_csv,
                btn_pdf,
                btn_png
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20
        )
    ]

    return ft.Container(
        content=ft.Stack(controls=[placeholder_view, view_resultados]),
        padding=10
    )