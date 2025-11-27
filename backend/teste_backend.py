import os
import base64
from datetime import datetime
import pandas as pd

# Importa as classes dos outros arquivos
from analysis import MotorAnalise
from database import GerenciadorBancoDados

def executar_demonstracao():
    """Simula como uma aplicação usaria as classes de backend."""
    
    motor = MotorAnalise()
    db = GerenciadorBancoDados()

    print("🚀 BEM-VINDO AO DEMO DO BACKEND QUANTISCANNER 🚀")
    
    try:
        # 1. Carregar dados
        dados_exemplo = [10, 12, 15, 15, 17, 18, 20, 22, 25, 30, 31, 35, 40, 42, 50]
        motor.carregar_dados_de_lista(dados_exemplo)
        print("\n✅ Dados de exemplo carregados com sucesso!")
        
        # 2. Calcular todas as métricas
        resultados = motor.calcular_todas_metricas()
        print("\n📊 Métricas Calculadas:")

        # 3. Exibir os resultados no console
        
        # Adicionado: Exibição dos Quartis
        print("\n--- Resumo dos Quartis ---")
        for chave, valor in resultados['quartis'].items():
            print(f"{chave}: {valor:.2f}")

        # Mantido: Exibição dos Decis
        print("\n--- Tabela de Decis ---")
        print(pd.DataFrame(resultados['tabelas_resumo']['decis']))

        # Adicionado: Exibição dos Percentis
        print("\n--- Tabela de Percentis (P1 a P99) ---")
        print(pd.DataFrame(resultados['tabelas_resumo']['percentis']))

        # 4. Gerar e salvar artefatos (gráficos e relatórios)
        diretorio_saida = "exports"
        if not os.path.exists(diretorio_saida):
            os.makedirs(diretorio_saida)
            
        # Gerar e salvar Boxplot
        boxplot_base64 = motor.gerar_boxplot()
        with open(os.path.join(diretorio_saida, "boxplot.png"), "wb") as f:
            f.write(base64.b64decode(boxplot_base64))
        
        print(f"\n🖼️ Gráfico de Boxplot salvo na pasta '{diretorio_saida}'.")
        
        # Exportar métricas para CSV
        motor.exportar_metricas_para_csv(resultados, os.path.join(diretorio_saida, "resultados.csv"))
        print(f"📄 Métricas exportadas para '{os.path.join(diretorio_saida, 'resultados.csv')}'.")

        # 5. Salvar a análise no banco de dados
        nome_analise = f"Análise de Teste - {datetime.now().strftime('%H:%M')}"
        id_salvo = db.salvar_analise(nome_analise, motor.dados)
        print(f"\n💾 Análise salva no histórico com o nome: '{nome_analise}' (ID: {id_salvo})")

    except ValueError as e:
        print(f"\n❌ ERRO: {e}")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")
    finally:
        # 6. Fechar a conexão com o banco de dados
        db.fechar_conexao()
        print("\n🔌 Conexão com o banco de dados fechada.")

# Garante que a demonstração só rode quando executarmos este arquivo diretamente
if __name__ == "__main__":
    executar_demonstracao()