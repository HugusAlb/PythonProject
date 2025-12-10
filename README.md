# Sistema Escolar Santa Ursula

Um sistema desktop desenvolvido em **Python** com interface gráfica **Tkinter** para gerenciamento de alunos, notas e médias escolares. O diferencial desta aplicação é a utilização do **Google Sheets** como banco de dados em nuvem, permitindo que as informações sejam sincronizadas em tempo real.

![Status](https://img.shields.io/badge/Status-Funcional-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Database](https://img.shields.io/badge/Database-Google%20Sheets-green)

## Funcionalidades

* **Cadastro de Alunos:** Registro de Nome, Idade e Nota com ID único (UUID).
* **Banco de Dados na Nuvem:** Leitura e escrita direta no Google Sheets.
* **Busca e Filtros:** Pesquisa de alunos por nome em tempo real.
* **Gestão:** Exclusão de registros com confirmação.
* **Estatísticas:** Cálculo automático da média de notas da turma.
* **Logs de Auditoria:** Registro automático de todas as ações (cadastros e remoções) em uma aba separada com data e hora.

## Tecnologias

* **Python 3.10+**
* **Tkinter** (Interface Gráfica)
* **gspread** (API do Google Sheets)
* **oauth2client** (Autenticação)

## Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python instalado. Em seguida, instale as bibliotecas necessárias:

```bash
pip install gspread oauth2client
```
após isso só executar no terminal:

```python
python main.py
```