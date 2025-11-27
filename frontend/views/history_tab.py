import flet as ft

def criar_aba_historico(estado, pagina, abas_principais):
    
    history_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome da Análise")),
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    rename_field = ft.TextField(label="Novo nome")

    rename_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Renomear Análise"),
        content=rename_field,
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(e)),
            ft.FilledButton("Salvar", on_click=lambda e: save_rename(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def atualizar_lista_historico():
        try:
            history_data = estado.gerenciador_bd.obter_historico()
            history_table.rows.clear()

            for item in history_data:
                analysis_id, name, timestamp = item
                history_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(analysis_id))),
                            ft.DataCell(ft.Text(name)),
                            ft.DataCell(ft.Text(timestamp)),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon="play_arrow",
                                        tooltip="Carregar Análise",
                                        data=analysis_id,
                                        on_click=carregar_analise,
                                    ),
                                    ft.IconButton(
                                        icon="edit",
                                        tooltip="Renomear",
                                        data={"id": analysis_id, "name": name},
                                        on_click=abrir_dialogo_renomear,
                                    )
                                ])
                            ),
                        ]
                    )
                )
            pagina.update()
        except Exception as e:
            pagina.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar histórico: {e}"), bgcolor="red")
            pagina.snack_bar.open = True
            pagina.update()

    estado.callback_atualizar_view_historico = atualizar_lista_historico

    def carregar_analise(e):
        analysis_id = e.control.data
        try:
            dados_carregados = estado.gerenciador_bd.carregar_analise(analysis_id)
            if not dados_carregados:
                raise ValueError("Análise não encontrada.")

            estado.motor_analise.carregar_dados_de_lista(dados_carregados['dados_brutos'])
            estado.metricas_atuais = estado.motor_analise.calcular_todas_metricas()
            
            if 'config_grafico' in dados_carregados:
                estado.config_grafico = dados_carregados['config_grafico']
            else:
                estado.config_grafico = {
                    'titulo': 'Distribuição dos Dados',
                    'label_y': 'Valores',
                    'cor': '#ADD8E6'
                }
            
            estado.boxplot_atual = estado.motor_analise.gerar_boxplot(
                titulo=estado.config_grafico['titulo'],
                label_y=estado.config_grafico['label_y'],
                cor=estado.config_grafico['cor']
            )

            if estado.callback_atualizar_view_entrada:
                estado.callback_atualizar_view_entrada()
            if estado.callback_atualizar_view_resultados:
                estado.callback_atualizar_view_resultados()

            abas_principais.selected_index = 1
            
            pagina.snack_bar = ft.SnackBar(ft.Text(f"Análise ID {analysis_id} carregada."), bgcolor="green")
            pagina.snack_bar.open = True
            pagina.update()

        except Exception as err:
            pagina.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar análise: {err}"), bgcolor="red")
            pagina.snack_bar.open = True
            pagina.update()

    def abrir_dialogo_renomear(e):
        data = e.control.data
        rename_field.value = data['name']
        rename_dialog.data = data['id'] 
        pagina.dialog = rename_dialog
        rename_dialog.open = True
        pagina.update()

    def close_dialog(e):
        rename_dialog.open = False
        pagina.update()

    def save_rename(e):
        analysis_id = rename_dialog.data
        novo_nome = rename_field.value
        if not novo_nome:
            rename_field.error_text = "O nome não pode ser vazio."
            pagina.update()
            return
            
        try:
            estado.gerenciador_bd.renomear_analise(analysis_id, novo_nome)
            rename_dialog.open = False
            pagina.snack_bar = ft.SnackBar(ft.Text("Análise renomeada com sucesso!"), bgcolor="green")
            pagina.snack_bar.open = True
            atualizar_lista_historico()
            pagina.update()
        except Exception as err:
            pagina.snack_bar = ft.SnackBar(ft.Text(f"Erro ao renomear: {err}"), bgcolor="red")
            pagina.snack_bar.open = True
            pagina.update()
    
    atualizar_lista_historico()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Text("Histórico de Análises", size=22, weight=ft.FontWeight.BOLD),
            ft.Text("Carregue uma análise anterior ou gerencie os nomes."),
            ft.Divider(),
            history_table,
        ]
    )