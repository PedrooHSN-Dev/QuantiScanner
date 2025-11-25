import flet as ft

from backend.analysis import MotorAnalise
from backend.database import GerenciadorBancoDados

from frontend.views.input import criar_aba_entrada
from frontend.views.history_tab import criar_aba_historico
from frontend.views.results_tab import criar_aba_resultados
from frontend.views.dev_tab import criar_aba_dev

class EstadoApp:
    def __init__(self):
        self.motor_analise = MotorAnalise()
        self.gerenciador_bd = GerenciadorBancoDados()
        self.metricas_atuais = None
        self.boxplot_atual = None
        self.config_grafico = {
            'titulo': 'Distribuição dos Dados',
            'label_y': 'Valores',
            'cor': '#ADD8E6'
        }
        self.callback_atualizar_view_resultados = None
        self.callback_atualizar_view_historico = None
        self.callback_atualizar_view_entrada = None


def main(pagina: ft.Page):
    pagina.title = "QuantiScanner - Análise de Boxplot"
    pagina.vertical_alignment = ft.MainAxisAlignment.START
    pagina.window_width = 1200
    pagina.window_height = 700

    estado_app = EstadoApp()

    abas_principais = ft.Tabs(
        selected_index=0,
        animation_duration=350,
        tabs=[],
        expand=True
    )

    conteudo_entrada = criar_aba_entrada(estado_app, pagina, abas_principais)
    conteudo_historico = criar_aba_historico(estado_app, pagina, abas_principais)
    conteudo_resultados = criar_aba_resultados(estado_app, pagina)
    conteudo_dev = criar_aba_dev(pagina)

    abas_principais.tabs = [
        ft.Tab(text="Entrada de Dados", content=conteudo_entrada),
        ft.Tab(text="Resultados", content=conteudo_resultados),
        ft.Tab(text="Histórico", content=conteudo_historico),
        ft.Tab(text="Desenvolvedores", content=conteudo_dev)
    ]

    pagina.add(abas_principais)
    pagina.update()


if __name__ == "__main__":
    ft.app(target=main)