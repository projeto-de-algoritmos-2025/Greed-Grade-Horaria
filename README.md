# Grade Horária FCTE

**Conteúdo da Disciplina**: Algoritmos Ambiciosos

## Alunos

<table>
  <tr>
    <td align="center"><a href="https://github.com/luanasoares0901"><img style="border-radius: 60%;" src="https://github.com/luanasoares0901.png" width="200px;" alt=""/><br /><sub><b>Luana Ribeiro</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/MMcLovin"><img style="border-radius: 60%;" src="https://github.com/MMcLovin.png" width="200px;" alt=""/><br /><sub><b>Gabriel Fernando de Jesus Silva</b></sub></a><br /></td>
  </tr>
</table>

## Sobre

Este projeto tem como objetivo desenvolver uma aplicação interativa que aplica o problema de seleção de intervalos (Interval Scheduling), mas em um contexto real e intuitivo: montar a grade de disciplinas de um aluno sem sobreposição de horários. O algoritmo usado é o Interval Scheduling Ambicioso, que busca maximizar o número de atividades (aulas) sem sobreposição de horários.
Além disso, foi usado o algoritmo de minimizar atraso máximo (Scheduling to Minimize Lateness) que organiza a prioridade de entrega de atividades. Algumas disciplinas incluem atividades (tarefas) com duração (horas) e um prazo (dia da semana + hora). Após montar a grade de aulas, o app monta um "plano de estudos" com essas atividades e utiliza o EDD para ordenar as tarefas de forma a minimizar o atraso máximo.


### Exemplo grade e planejamento gerados com o algoritmo

![Disciplinas](/assets/Materias.png)
![Grade](/assets/Grade.png)
![Disciplinas](/assets/PlanodeEstudos.png)

## Linguagem e Bibliotecas

* **Linguagem**: Python
* **Principais Bibliotecas utilizadas**: Streamlit (para criação de interfaces web interativas)

## Apresentação

A apresentação do projeto pode ser acessada [aqui](https://www.youtube.com/watch?v=lM9NoJa0Y-k).

## Guia de Instalação

### Pré-requisitos

- Git (versão 2.40 ou superior);
- Python (versão 3.11 ou superior);

### Executando o projeto

- Recomendamos criar um ambiente virtual para o projeto. Para isso, utilize os comandos abaixo:

```bash
python -m venv env
source env/bin/activate  # No Windows use: env\Scripts\activate
```

- Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

- Após instalar as dependências,execute o comando:

```bash
streamlit run app.py
```
