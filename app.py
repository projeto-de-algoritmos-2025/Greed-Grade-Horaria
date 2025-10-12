import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Organizador de Grade", layout="centered")

#TO-DO
# - Criar disciplinas que sejam de dois dias (seg e qua, por exemplo) - feito
# - Melhorar visualização da tabela (cores, etc) - feito
# - Apresentar relatório de execução do algoritmo




# --- Disciplinas com possibilidade de ocorrer em pares de dias ---
disciplinas = [
    {"nome": "Cálculo I", "inicio": 8, "fim": 10, "dias": ["Segunda", "Quarta"]},
    {"nome": "Álgebra Linear", "inicio": 9, "fim": 11, "dias": ["Segunda"]},
    {"nome": "Física I", "inicio": 10, "fim": 12, "dias": ["Segunda"]},
    {"nome": "Arquitetura e Desenho", "inicio": 8, "fim": 10, "dias": ["Terça", "Quinta"]},
    {"nome": "Lógica de Programação", "inicio": 9, "fim": 11, "dias": ["Terça"]},
    {"nome": "Estruturas de Dados 1", "inicio": 10, "fim": 12, "dias": ["Terça"]},
    {"nome": "Matemática Discreta 1", "inicio": 14, "fim": 16, "dias": ["Quarta"]},
    {"nome": "Requisitos de Software", "inicio": 15, "fim": 17, "dias": ["Quarta"]},
    {"nome": "Matemática Discreta 2", "inicio": 8, "fim": 10, "dias": ["Quinta"]},
    {"nome": "Engenharia e Ambiente", "inicio": 10, "fim": 12, "dias": ["Quinta"]},
    {"nome": "Banco de Dados 1", "inicio": 8, "fim": 10, "dias": ["Sexta"]},
    {"nome": "Redes de Computadores", "inicio": 9, "fim": 11, "dias": ["Sexta"]},
    # Exemplos adicionais com par Segunda-Sexta
    {"nome": "Projeto de Algoritmos", "inicio": 13, "fim": 15, "dias": ["Segunda", "Sexta"]},
    {"nome": "Estruturas de Dados 2", "inicio": 15, "fim": 16, "dias": ["Segunda", "Sexta"]},
]

# --- Algoritmo ambicioso: Interval Scheduling ---
def montar_grade(disciplinas):
    """
    Seleciona um conjunto de disciplinas sem conflitos. Cada disciplina pode
    ocorrer em vários dias (campo 'dias'). A disciplina só é incluída se
    todos os seus dias estiverem livres no intervalo [inicio,fim).

    Implementação: ordena por hora de término (heurística gulosa) e testa
    se a disciplina conflita em algum dos seus dias com disciplinas já
    escolhidas.
    """
    # Normaliza: transforma campo 'dia' único em 'dias' se necessário
    for d in disciplinas:
        if 'dias' not in d and 'dia' in d:
            d['dias'] = [d['dia']]

    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    ocupados = {dia: [] for dia in dias_semana}  # lista de intervalos por dia

    def conflita(intervalos, s, e):
        for a, b in intervalos:
            if not (b <= s or e <= a):
                return True
        return False

    escolhidas = []
    disciplinas_sorted = sorted(disciplinas, key=lambda x: x.get('fim', 10**9))

    for disc in disciplinas_sorted:
        s = int(disc.get('inicio', 0))
        e = int(disc.get('fim', 0))
        dias = disc.get('dias', [])

        # Verifica se em algum dia há conflito
        tem_conflito = False
        for dia in dias:
            if dia not in ocupados:
                continue
            if conflita(ocupados[dia], s, e):
                tem_conflito = True
                break

        if not tem_conflito:
            escolhidas.append(disc)
            for dia in dias:
                if dia in ocupados:
                    ocupados[dia].append((s, e))

    return escolhidas


def montar_tabela_horario(grade, inicio_horario=7, fim_horario=18):
    """
    Gera uma tabela (DataFrame) com horários por hora entre inicio_horario e fim_horario.
    Suporta disciplinas com múltiplos dias (campo 'dias').
    """
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    horas = list(range(inicio_horario, fim_horario))  # intervalo por hora

    tabela = {dia: ["" for _ in horas] for dia in dias_semana}

    for d in grade:
        nome = d.get('nome')
        inicio = int(d.get('inicio', 0))
        fim = int(d.get('fim', 0))
        dias = d.get('dias', [])

        for dia in dias:
            if dia not in dias_semana:
                continue
            for h_idx, h in enumerate(horas):
                if h >= inicio and h < fim:
                    if tabela[dia][h_idx]:
                        tabela[dia][h_idx] = tabela[dia][h_idx] + ' / ' + nome
                    else:
                        tabela[dia][h_idx] = nome

    index_labels = [f"{h}h-{h+1}h" for h in horas]
    df_tabela = pd.DataFrame(tabela, index=index_labels)
    return df_tabela

# --- Interface ---
st.title("📚 Organizador de Grade do Aluno (Algoritmo Ambicioso)")
st.write("Monte sua grade e veja automaticamente a melhor combinação de matérias sem conflitos de horário.")

# Interface: mostra cada disciplina (com seus dias) e permite seleção por disciplina.
selecionadas = []
cols = st.columns(2)
for i, d in enumerate(disciplinas):
    col = cols[i % 2]
    dias_str = ", ".join(d.get('dias', d.get('dia', [])))
    label = f"{d['nome']} — {dias_str} ({d['inicio']}h - {d['fim']}h)"
    if col.checkbox(label, key=f"{d['nome']}"):
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
                dias_str = ", ".join(d.get('dias', d.get('dia', [])))
                st.write(f"• **{d['nome']}** — {dias_str} ({d['inicio']}h às {d['fim']}h)")

            fora = [d for d in selecionadas if d not in grade]
            if fora:
                st.write("---")
                st.warning("Disciplinas com conflito (não incluídas):")
                for d in fora:
                    dias_str = ", ".join(d.get('dias', d.get('dia', [])))
                    st.write(f"- {d['nome']} ({dias_str} {d['inicio']}h-{d['fim']}h)")

            
            # --- Tabela horária ---
            st.write("---")
            st.subheader("📋 Tabela Horária (visão por hora)")
            df_tabela = montar_tabela_horario(grade, inicio_horario=7, fim_horario=18)

            # Mapeia cores para cada disciplina e aplica estilo compactado às células
            vals = list(pd.unique(df_tabela.values.ravel()))
            nomes = [v for v in vals if isinstance(v, str) and v.strip()]

            palette = px.colors.qualitative.Plotly
            color_map = {nome: palette[i % len(palette)] for i, nome in enumerate(nomes)}

            def cell_style(val):
                if not isinstance(val, str) or not val:
                    return ""
                key = val.split(' / ')[0]
                color = color_map.get(key, "#ffffff")
                text_color = "#000000"
                # estilos inline para cada célula (cor de fundo + cor do texto)
                return f"background-color: {color}; color: {text_color}; padding:4px; font-size:12px; white-space:nowrap;"

            # use Styler.map (novo) quando disponível, com fallback para applymap
            try:
                styled = df_tabela.style.map(cell_style)
            except Exception:
                # versões antigas do pandas podem não ter .map no Styler
                styled = df_tabela.style.applymap(cell_style)

            # Gera HTML compacto com CSS reduzido para tornar a tabela mais harmônica
            table_html = styled.to_html()
            compact_css = """
            <style>
            .tablecompact td, .tablecompact th {padding:4px !important; font-size:12px !important; white-space:nowrap;}
            .tablecompact {border-collapse: collapse;}
            .tablecompact th {text-align: left;}
            .table-wrap {max-width: 900px; overflow-x: auto;}
            </style>
            """

            # Insere a classe .tablecompact no HTML gerado pelo Styler
            table_html = table_html.replace('<table', '<table class="tablecompact"')
            wrapped = f"<div class='table-wrap'>{compact_css}{table_html}</div>"
            st.markdown(wrapped, unsafe_allow_html=True)

            # Botão para download CSV
            csv = df_tabela.to_csv(index=True)
            st.download_button(label="Baixar tabela como CSV", data=csv, file_name="tabela_horaria.csv", mime="text/csv")
        else:
            st.error("Nenhuma combinação possível sem conflito 😢")
