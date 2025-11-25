import flet as ft

def criar_aba_entrada(estado, pagina, abas_principais):
    """
    Cria a view (aba) para a entrada de dados do usuário
    """
    
    def atualizar_campos_resumo():
        """Função auxiliar para preencher os campos de resumo."""
        if estado.metricas_atuais:
            resumo = estado.metricas_atuais['resumo']
            campo_qtd_dados.value = str(resumo['contagem'])
            campo_media.value = f"{resumo['media']:.4f}"
            campo_mediana.value = f"{resumo['mediana']:.4f}"
            campo_valor_min.value = f"{resumo['min']:.4f}"
            campo_valor_max.value = f"{resumo['max']:.4f}"
        else: 
            for campo in [campo_qtd_dados, campo_media, campo_mediana, campo_valor_min, campo_valor_max]:
                campo.value = ""
        pagina.update()

    def processar_resultado_seletor_arquivos(e: ft.FilePickerResultEvent):
        """Usa o backend para processar arquivos CSV ou Excel."""
        if not e.files:
            return

        caminho_arquivo = e.files[0].path
        nome_arquivo = e.files[0].name
        
        try:
            texto_status.value = f"Carregando {nome_arquivo}..."
            texto_status.color = "blue"
            pagina.update()
            
            if nome_arquivo.endswith('.csv'):
                estado.motor_analise.carregar_dados_de_csv(caminho_arquivo)
            elif nome_arquivo.endswith(('.xlsx', '.xls')):
                estado.motor_analise.carregar_dados_de_excel(caminho_arquivo)
            
            estado.metricas_atuais = estado.motor_analise.calcular_todas_metricas()
            
            texto_status.value = f"✓ Arquivo '{nome_arquivo}' processado com sucesso!"
            texto_status.color = "green"
            atualizar_campos_resumo()

        except Exception as ex:
            texto_status.value = f"Erro ao processar arquivo: {ex}"
            texto_status.color = "red"
            estado.metricas_atuais = None
            atualizar_campos_resumo()

    def processar_calculo_manual(e):
        """Usa o backend para processar os dados do campo de texto."""
        texto = entrada_manual.value.strip()
        if not texto:
            texto_status.value = "Por favor, insira alguns valores."
            texto_status.color = "red"
            pagina.update()
            return
            
        try:
            lista_dados = [float(x.strip()) for x in texto.split(",") if x.strip()]
            
            estado.motor_analise.carregar_dados_de_lista(lista_dados)
            estado.metricas_atuais = estado.motor_analise.calcular_todas_metricas()
            
            texto_status.value = f"✓ {len(lista_dados)} valores processados com sucesso!"
            texto_status.color = "green"
        
            atualizar_campos_resumo()

        except Exception as ex:
            texto_status.value = f"Erro: {ex}"
            texto_status.color = "red"
            estado.metricas_atuais = None
            atualizar_campos_resumo()

    def navegar_para_resultados(e):
        """Navega para a aba de resultados após gerar o gráfico."""
        if not estado.metricas_atuais:
            texto_status.value = "Calcule os dados antes de gerar o gráfico."
            texto_status.color = "red"
            pagina.update()
            return

        try:
            estado.boxplot_atual = estado.motor_analise.gerar_boxplot()

            if estado.callback_atualizar_view_resultados:
                estado.callback_atualizar_view_resultados()

            abas_principais.selected_index = 1
            pagina.update()

        except Exception as ex:
            texto_status.value = f"Erro ao gerar gráfico: {ex}"
            texto_status.color = "red"
            pagina.update()
            
    def limpar_valores(e):
        """Limpa os valores atuais e reseta os campos."""
        estado.metricas_atuais = None
        estado.boxplot_atual = None
        entrada_manual.value = ""
        texto_status.value = ""
        atualizar_campos_resumo()

        if estado.callback_atualizar_view_resultados:
             estado.callback_atualizar_view_resultados()  

        pagina.update()
    
    
    # --- COMPONENTES DA UI ---

    seletor_de_arquivos = ft.FilePicker(on_result=processar_resultado_seletor_arquivos)
    pagina.overlay.append(seletor_de_arquivos)

    campo_qtd_dados = ft.TextField(label="Qtd Dados", read_only=True, width=200, border_color="white")
    campo_media = ft.TextField(label="Média", read_only=True, width=200, border_color="white")
    campo_mediana = ft.TextField(label="Mediana", read_only=True, width=200, border_color="white")
    campo_valor_min = ft.TextField(label="Valor Mínimo", read_only=True, width=200, border_color="white")
    campo_valor_max = ft.TextField(label="Valor Máximo", read_only=True, width=200, border_color="white")
    
    entrada_manual = ft.TextField(
        label="Dados",
        hint_text="Dados",
        width=300,
        multiline=False,
        border_color="white"
    )
    
    texto_status = ft.Text("", color="green", size=14)

    btn_calcular = ft.ElevatedButton("Calcular", on_click=processar_calculo_manual, bgcolor="blue", color="white")
    btn_csv = ft.ElevatedButton(
        "Importar CSV",
        on_click=lambda _: seletor_de_arquivos.pick_files(allowed_extensions=["csv"]),
        bgcolor="lightblue", color="black"
    )
    btn_excel = ft.ElevatedButton(
        "Importar Excel",
        on_click=lambda _: seletor_de_arquivos.pick_files(allowed_extensions=["xlsx"]),
        bgcolor="lightblue", color="black"
    )
    
    btn_limpar = ft.ElevatedButton(
        "Limpar", 
        on_click=limpar_valores, 
        bgcolor="red", 
        color="white", 
        height=50)
    
    btn_gerar = ft.ElevatedButton(
        "Gerar Gráfico e Quartis",
        on_click=navegar_para_resultados, 
        bgcolor="blue", 
        color="white",
        height=50)

    # --- 3. LAYOUT FINAL ---
    
    return ft.Row(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Inserir Dados", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Valores separados por vírgula (outros caracteres não são aceitos)", size=15),
                    ft.Text("Utilize ponto para valores decimais:", size=13),
                    ft.Row([entrada_manual, btn_calcular], spacing=10),
                    ft.Row([btn_csv, btn_excel, btn_limpar], spacing=10),
                    texto_status,
                    ft.Container(height=20),
                    btn_gerar,
                ]),
                padding=30, border=ft.border.all(1), border_radius=10
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Resumo Estatístico", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([campo_qtd_dados, campo_valor_min], spacing=20),
                    ft.Row([campo_media, campo_valor_max], spacing=20),
                    ft.Row([campo_mediana]),
                ]),
                padding=40, border=ft.border.all(1), border_radius=10, expand=True
            )
        ],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START
    )