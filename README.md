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

Este projeto tem como objetivo desenvolver uma aplicação interativa que aplica o problema de seleção de intervalos (interval scheduling), mas em um contexto real e intuitivo: montar a grade de disciplinas de um aluno sem sobreposição de horários. O algoritmo usado é o Interval Scheduling Ambicioso, que busca maximizar o número de atividades (aulas) sem sobreposição de horários.

### 🔢 Passos do algoritmo

- Ordena as disciplinas pelo horário de término (fim).

- Começa escolhendo a primeira (a que termina mais cedo).

- Para cada próxima disciplina:

- Se o inicio for maior ou igual ao fim da última escolhida, inclui.

- Caso contrário, descarta (há conflito).


### Exemplo grade gerada com o nosso algoritmo

![Disciplinas](/assets/Materias.png)
![Grade](/assets/GradeGerada.png)


## Linguagem e Bibliotecas

* **Linguagem**: Python
* **Principais Bibliotecas utilizadas**: Streamlit (para criação de interfaces web interativas)

## Apresentação

A apresentação do projeto pode ser acessada [aqui](https://www.youtube.com/watch?v=C614gKM6kvs).

## Guia de Instalação

### Pré-requisitos

- Git (versão 2.40 ou superior);
- Python (versão 3.11 ou superior);

### Executando o projeto

- Instale o Streamlit

```bash
 pip install streamlit
```

- Após instalar as dependências,execute o comando:

```bash
streamlit run app.py
```