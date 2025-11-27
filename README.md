## ✨ Funcionalidades Principais

  - **Análise Estatística Completa:** Calcula um resumo estatístico (média, mediana, mínimo, máximo), quartis, decis e todos os 99 percentis de um conjunto de dados.
  - **Múltiplas Fontes de Dados:** Carrega dados de forma flexível a partir de:
      - Listas Python
      - Arquivos `.csv`
      - Arquivos `.xlsx` (Excel)
  - **Geração de Gráficos:** Cria visualizações de boxplot e as retorna em formato **Base64**, ideal para integração com APIs e frontends web sem a necessidade de salvar arquivos em disco.
  - **Exportação de Relatórios:** Exporta todos os resultados da análise para formatos de fácil compartilhamento, como `.csv` e `.pdf`.
  - **Persistência de Dados:** Inclui um sistema de histórico que utiliza um banco de dados **SQLite** para salvar, listar e carregar análises anteriores.




## 🏛️ Arquitetura do Projeto

O backend é organizado em um design modular para garantir a separação de responsabilidades e facilitar a manutenção e escalabilidade.

  - `analysis.py` (**Motor de Análise**): O núcleo do sistema. Contém a classe `MotorAnalise`, que centraliza toda a lógica de cálculo, geração de gráficos e exportação de relatórios.
  - `database.py` (**Gerenciador de Banco de Dados**): Contém a classe `GerenciadorBancoDados`, responsável por todas as interações com o banco de dados SQLite para gerenciar o histórico das análises.
  - `teste_backend.py` (**Demonstração e Ponto de Entrada**): Um script que serve como exemplo prático de como utilizar as classes do backend em um fluxo de trabalho completo.

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3 instalado. Você precisará das seguintes bibliotecas, que podem ser instaladas via `pip`:

```sh
pip install -r requirementos.txt
```

### Dica
Usar `venv` no Visual Studio Code para que todas as bibliotecas funcionem sem problemas.

**Resumo Rápido (Faça isso no terminal)**

  - **Criar:** `python -m venv venv`
  - **Ativar (Windows):** `venv\Scripts\activate`
  - **Instalar dependências:** `pip install -r requirements.txt`
  - **Executar o App: `python main.py`**
  - **Executar o BackEnd para teste: `python .\backend\teste_backend.py`**
  - **Desativar:** `deactivate`

O `venv` cria uma "bolha" ou um ambiente isolado para cada projeto. Dentro dessa bolha, você instala apenas as bibliotecas e versões do projeto, sem interferir com outros projetos ou com a instalação principal do Python no seu computador.


### Rodando a Demonstração

Para ver o backend em ação, basta executar o script `teste_backend.py`. Ele usará um conjunto de dados de exemplo, realizará todos os cálculos, imprimirá os resultados no console e salvará (gráficos e relatórios) em uma pasta chamada `exports`.


`python .\backend\teste_backend.py`


Após a execução, você verá:

1.  As tabelas de quartis, decis e percentis impressas no terminal.
2.  Uma nova pasta `exports/` contendo:
      - `boxplot.png`: O gráfico de boxplot gerado.
      - `resultados.csv`: Um arquivo CSV com todas as métricas calculadas.
3.  Uma mensagem confirmando que a análise foi salva no banco de dados `historico_quantiscanner.db`.
