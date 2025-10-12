import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Organizador de Grade", layout="centered")

#TO-DO
# - Criar disciplinas que sejam de dois dias (seg e qua, por exemplo)
# - Melhorar visualização da tabela (cores, etc)
# - Apresentar relatório de execução do algoritmo


# --- Disciplinas com conflitos ---
disciplinas = [
    {"nome": "Cálculo I", "inicio": 8, "fim": 10, "dia": "Segunda"},
    {"nome": "Álgebra Linear", "inicio": 9, "fim": 11, "dia": "Segunda"},
    {"nome": "Física I", "inicio": 10, "fim": 12, "dia": "Segunda"},
    {"nome": "Programação I", "inicio": 8, "fim": 10, "dia": "Terça"},
    {"nome": "Lógica de Programação", "inicio": 9, "fim": 11, "dia": "Terça"},
    {"nome": "Estruturas de Dados", "inicio": 10, "fim": 12, "dia": "Terça"},
    {"nome": "História da Ciência", "inicio": 14, "fim": 16, "dia": "Quarta"},
    {"nome": "Química Geral", "inicio": 15, "fim": 17, "dia": "Quarta"},
    {"nome": "Inglês Técnico", "inicio": 8, "fim": 10, "dia": "Quinta"},
    {"nome": "Engenharia e Sociedade", "inicio": 10, "fim": 12, "dia": "Quinta"},
    {"nome": "Banco de Dados", "inicio": 8, "fim": 10, "dia": "Sexta"},
    {"nome": "Redes de Computadores", "inicio": 9, "fim": 11, "dia": "Sexta"},
]

# --- Algoritmo ambicioso: Interval Scheduling ---
def montar_grade(disciplinas):
    """Seleciona o maior conjunto de disciplinas sem conflitos (por dia)."""
    grade_final = []

    dias = sorted(set(d["dia"] for d in disciplinas))
    for dia in dias:
        disciplinas_dia = [d for d in disciplinas if d["dia"] == dia]
        disciplinas_dia.sort(key=lambda x: x["fim"])  # Estratégia greedy

        ultimo_fim = -1
        for d in disciplinas_dia:
            if d["inicio"] >= ultimo_fim:
                grade_final.append(d)
                ultimo_fim = d["fim"]

    return grade_final


def montar_tabela_horario(grade, inicio_horario=7, fim_horario=18):
    """Gera uma tabela (DataFrame) com horários por hora entre inicio_horario e fim_horario.
    Linhas: intervalo horário (ex: 7h, 8h...). Colunas: dias da semana.
    Cada célula contém o nome da disciplina que ocorre naquela hora naquele dia.
    """
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    horas = list(range(inicio_horario, fim_horario))  # intervalo por hora

    # Inicializa tabela vazia
    tabela = {dia: ["" for _ in horas] for dia in dias_semana}

    for d in grade:
        dia = d.get("dia")
        if dia not in dias_semana:
            continue
        nome = d.get("nome")
        inicio = int(d.get("inicio", 0))
        fim = int(d.get("fim", 0))

        # Preenche todas as horas que a disciplina ocupa
        for h_idx, h in enumerate(horas):
            if h >= inicio and h < fim:
                if tabela[dia][h_idx]:
                    # Em caso raro de sobreposição, junta os nomes
                    tabela[dia][h_idx] = tabela[dia][h_idx] + " / " + nome
                else:
                    tabela[dia][h_idx] = nome

    index_labels = [f"{h}h-{h+1}h" for h in horas]
    df_tabela = pd.DataFrame(tabela, index=index_labels)
    return df_tabela

# --- Interface ---
st.title("📚 Organizador de Grade do Aluno (Algoritmo Ambicioso)")
st.write("Monte sua grade e veja automaticamente a melhor combinação de matérias sem conflitos de horário.")

selecionadas = []
dias = sorted(set(d["dia"] for d in disciplinas))

for dia in dias:
    st.subheader(f"📅 {dia}")
    cols = st.columns(2)
    for i, d in enumerate([disc for disc in disciplinas if disc["dia"] == dia]):
        col = cols[i % 2]
        if col.checkbox(f"{d['nome']} ({d['inicio']}h - {d['fim']}h)", key=f"{dia}-{d['nome']}"):
            selecionadas.append(d)

if st.button("Gerar Grade Otimizada"):
    if not selecionadas:
        st.warning("Selecione pelo menos uma disciplina.")
    else:
        grade = montar_grade(selecionadas)

        if grade:
            st.success("Grade montada com sucesso! ✅")
            st.write("Estas são as disciplinas incluídas:")

            for d in grade:
                st.write(f"• **{d['nome']}** — {d['dia']} ({d['inicio']}h às {d['fim']}h)")

            fora = [d for d in selecionadas if d not in grade]
            if fora:
                st.write("---")
                st.warning("Disciplinas com conflito (não incluídas):")
                for d in fora:
                    st.write(f"- {d['nome']} ({d['dia']} {d['inicio']}h-{d['fim']}h)")

            
            # --- Tabela horária ---
            st.write("---")
            st.subheader("📋 Tabela Horária (visão por hora)")
            df_tabela = montar_tabela_horario(grade, inicio_horario=7, fim_horario=18)
            st.dataframe(df_tabela)

            # Botão para download CSV
            csv = df_tabela.to_csv(index=True)
            st.download_button(label="Baixar tabela como CSV", data=csv, file_name="tabela_horaria.csv", mime="text/csv")
        else:
            st.error("Nenhuma combinação possível sem conflito 😢")
