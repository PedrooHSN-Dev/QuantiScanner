import flet as ft

def atualizar_view(estado, pagina):
    """
    Atualiza a view de resultados com base no estado.
    Se o estado for nulo, reseta a view para o placeholder.
    """
    if not estado.metricas_atuais:
        placeholder_view.visible = True
        view_resultados.visible = False
        
        imagem_boxplot.src_base64 = None
        campo_q1.value = ""
        campo_q2.value = ""
        campo_q3.value = ""
        campo_iqr.value = ""
        tabela_decis.rows.clear()
        tabela_percentis.rows.clear()
        
        pagina.update()
        return

    imagem_boxplot.src_base64 = estado.boxplot_atual
    
    quartis = estado.metricas_atuais['quartis']
    campo_q1.value = f"{quartis['Q1']:.4f}"
    campo_q2.value = f"{quartis['Q2 (Mediana)']:.4f}"
    campo_q3.value = f"{quartis['Q3']:.4f}"
    campo_iqr.value = f"{quartis['Intervalo Interquartil (IQR)']:.4f}"

    decis = estado.metricas_atuais['tabelas_resumo']['decis']
    tabela_decis.rows.clear()
    tabela_decis.rows.extend([
        ft.DataRow(cells=[ft.DataCell(ft.Text(item['decil'])), ft.DataCell(ft.Text(str(item['valor'])))])
        for item in decis
    ])
    
    percentis = estado.metricas_atuais['tabelas_resumo']['percentis']
    tabela_percentis.rows.clear()
    tabela_percentis.rows.extend([
        ft.DataRow(cells=[ft.DataCell(ft.Text(item['percentil'])), ft.DataCell(ft.Text(str(item['valor'])))])
        for item in percentis
    ])

    placeholder_view.visible = False
    view_resultados.visible = True
    pagina.update()

def criar_aba_resultados(estado, pagina):

    estado.callback_atualizar_view_resultados = lambda: atualizar_view(estado, pagina)

    def salvar_analise(e):
        nome_analise = campo_nome_analise.value
        if not nome_analise:
            pagina.snack_bar = ft.SnackBar(content=ft.Text("Por favor, dê um nome para a análise."), bgcolor="red")
            pagina.snack_bar.open = True
            pagina.update()
            return
        
        try:
            estado.gerenciador_bd.salvar_analise(nome_analise, estado.metricas_atuais)
            pagina.snack_bar = ft.SnackBar(content=ft.Text(f"Análise '{nome_analise}' salva com sucesso!"), bgcolor="green")
            
            if estado.callback_atualizar_view_historico:
                estado.callback_atualizar_view_historico()

            campo_nome_analise.value = ""
        except Exception as err:
            pagina.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao salvar: {err}"), bgcolor="red")
        
        pagina.snack_bar.open = True
        pagina.update()

    def processar_resultado_exportacao(e: ft.FilePickerResultEvent):
        if not e.path:
            return

        caminho_salvar = e.path
        try:
            if e.data == "csv":
                estado.motor_analise.exportar_metricas_para_csv(estado.metricas_atuais, caminho_salvar)
                msg = "Métricas exportadas para CSV com sucesso!"
            elif e.data == "pdf":
                estado.motor_analise.exportar_relatorio_completo_para_pdf(estado.metricas_atuais, estado.boxplot_atual, caminho_salvar)
                msg = "Relatório PDF exportado com sucesso!"
            
            pagina.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor="green")
        except Exception as err:
            pagina.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao exportar: {err}"), bgcolor="red")
        
        pagina.snack_bar.open = True
        pagina.update()

    seletor_salvar_arquivo = ft.FilePicker(on_result=processar_resultado_exportacao)
    pagina.overlay.append(seletor_salvar_arquivo)
    
    global imagem_boxplot, campo_q1, campo_q2, campo_q3, campo_iqr, tabela_decis, tabela_percentis, placeholder_view, view_resultados

    imagem_boxplot = ft.Image(src_base64="", width=700, height=500, fit=ft.ImageFit.CONTAIN)
    
    campo_q1 = ft.TextField(label="Q1", read_only=True)
    campo_q2 = ft.TextField(label="Q2", read_only=True)
    campo_q3 = ft.TextField(label="Q3", read_only=True)
    campo_iqr = ft.TextField(label="IQR", read_only=True)

    tabela_decis = ft.DataTable(columns=[ft.DataColumn(ft.Text("Decil")), ft.DataColumn(ft.Text("Valor"))], rows=[])
    tabela_percentis = ft.DataTable(columns=[ft.DataColumn(ft.Text("Percentil")), ft.DataColumn(ft.Text("Valor"))], rows=[])
    
    campo_nome_analise = ft.TextField(label="Nome da Análise", width=350)
    
    btn_salvar = ft.ElevatedButton("Salvar Análise", on_click=salvar_analise, icon="save")
    btn_exportar_csv = ft.ElevatedButton("Exportar CSV", on_click=lambda _: seletor_salvar_arquivo.save_file(file_name="metricas.csv", data="csv"), icon="table_view")
    btn_exportar_pdf = ft.ElevatedButton("Exportar PDF", on_click=lambda _: seletor_salvar_arquivo.save_file(file_name="relatorio.pdf", data="pdf"), icon="picture_as_pdf")
    
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
    
    view_resultados = ft.Column(
        visible=False,
        scroll=ft.ScrollMode.ADAPTIVE,
        spacing=20,
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        content=imagem_boxplot,
                        border=ft.border.all(1), border_radius=10, padding=25,
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
                    btn_exportar_csv,
                    btn_exportar_pdf
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20
            )
        ]
    )

    return ft.Container(
        content=ft.Stack(controls=[placeholder_view, view_resultados]),
        padding=10
    )