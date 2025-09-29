import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class MotorAnalise:
    """Realiza todos os cálculos e a lógica de análise de dados."""

    def __init__(self):
        self.dados = None

    def carregar_dados_de_lista(self, lista_dados):
        if len(lista_dados) < 2:
            raise ValueError("São necessários pelo menos 2 números.")
        self.dados = sorted([float(x) for x in lista_dados])
        return True

    def carregar_dados_de_csv(self, caminho_arquivo):
        df = pd.read_csv(caminho_arquivo)
        lista_dados = df.iloc[:, 0].dropna().tolist()
        self.carregar_dados_de_lista(lista_dados)
        return True

    def carregar_dados_de_excel(self, caminho_arquivo):
        df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        lista_dados = df.iloc[:, 0].dropna().tolist()
        self.carregar_dados_de_lista(lista_dados)
        return True
    
    def calcular_todas_metricas(self):
        if self.dados is None:
            raise ValueError("Nenhum dado carregado para análise.")

        resumo = { "contagem": len(self.dados), "min": np.min(self.dados), "max": np.max(self.dados), "media": np.mean(self.dados), "mediana": np.median(self.dados) }
        q1, q2, q3 = np.percentile(self.dados, [25, 50, 75])
        quartis = { "Q1": q1, "Q2 (Mediana)": q2, "Q3": q3, "Intervalo Interquartil (IQR)": q3 - q1 }
        decis = {f"D{i}": np.percentile(self.dados, i * 10) for i in range(1, 10)}
        todos_percentis_pontos = range(1, 100)
        todos_percentis = {f"P{i}": np.percentile(self.dados, i) for i in todos_percentis_pontos}
        tabelas_resumo = {
            "decis": [{"decil": chave, "valor": round(valor, 4)} for chave, valor in decis.items()],
            "percentis": [{"percentil": chave, "valor": round(valor, 4)} for chave, valor in todos_percentis.items()]
        }
        return { "resumo": resumo, "quartis": quartis, "tabelas_resumo": tabelas_resumo, "dados_brutos": self.dados }

    def _gerar_grafico_como_base64(self, funcao_plot):
        fig = plt.figure(figsize=(8, 6))
        funcao_plot()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return img_base64

    def gerar_boxplot(self):
        def plot():
            plt.boxplot(self.dados, patch_artist=True, boxprops=dict(facecolor='lightblue'))
            plt.title('Boxplot dos Dados')
            plt.ylabel('Valores')
            plt.grid(True, linestyle='--', alpha=0.6)
        return self._gerar_grafico_como_base64(plot)
        
    def exportar_metricas_para_csv(self, metricas, caminho_arquivo):
        dados_decis = metricas['tabelas_resumo']['decis']
        dados_percentis = metricas['tabelas_resumo']['percentis']
        todas_metricas = {**metricas['resumo'], **metricas['quartis']}
        df1 = pd.DataFrame(list(todas_metricas.items()), columns=['Métrica', 'Valor'])
        df2 = pd.DataFrame(dados_decis).rename(columns={'decil': 'Métrica', 'valor': 'Valor'})
        df3 = pd.DataFrame(dados_percentis).rename(columns={'percentil': 'Métrica', 'valor': 'Valor'})
        df_final = pd.concat([df1, df2, df3], ignore_index=True)
        df_final.to_csv(caminho_arquivo, index=False)
        
    def exportar_relatorio_completo_para_pdf(self, metricas, boxplot_base64, caminho_arquivo):
        c = canvas.Canvas(caminho_arquivo, pagesize=letter)
        largura, altura = letter
        
        c.drawString(72, altura - 72, "Relatório de Análise Estatística")
        
        texto = c.beginText(72, altura - 108)
        texto.setFont("Helvetica", 10)
        
        resumo_geral = {**metricas['resumo'], **metricas['quartis']}
        for chave, valor in resumo_geral.items():
            texto.textLine(f"{chave}: {valor:.4f}")
        
        c.drawText(texto)
        
        if boxplot_base64:
            imagem_bytes = base64.b64decode(boxplot_base64)
            imagem = io.BytesIO(imagem_bytes)
            c.drawImage(imagem, 72, altura - 400, width=400, height=300)

        c.save()
        return True