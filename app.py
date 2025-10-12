import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Organizador de Grade", layout="centered")

# TO-DO
# - Apresentar relatório de execução do algoritmo
# - Adicionar horarios e atividades mais desafiadoras para o algoritmo
# - Atualizar README com instruções de uso, nova parte do plano de estudos e bibliotecas usadas
# 

# DONE
# - Criar disciplinas que sejam de dois dias (seg e qua, por exemplo) - feito
# - Melhorar visualização da tabela (cores, etc) - feito
# - Adicionar atividades para cada disciplina e montar plano de estudos (EDD) - feito
# - Adicionar gráfico de Gantt para o plano de estudos - feito
# - Remover o array de disciplinas do app.py e colocar em outro arquivo - feito



# Extrai lista de disciplinas para o módulo externo `disciplinas.py`
from disciplinas import disciplinas

def schedule_minimize_lateness(jobs):
    """
    jobs: lista de dicts com 'nome', 'p' (duração em horas), 'd' (deadline numérico)
    Retorna: schedule (lista com start/finish/lateness) e L_max
    """
    jobs_sorted = sorted(jobs, key=lambda x: x['d'])
    t = 0
    schedule = []
    L_max = 0
    for job in jobs_sorted:
        start = t
        finish = start + job['p']
        lateness = max(0, finish - job['d'])
        schedule.append({'nome': job.get('nome', ''), 'p': job['p'], 'd': job['d'], 'start': start, 'finish': finish, 'lateness': lateness})
        L_max = max(L_max, lateness)
        t = finish
    return schedule, L_max

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
    if col.checkbox(label, key=f"{d['nome']}-{i}"):
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

            # --- Plano de estudos (EDD) ---
            # Coleta atividades das disciplinas escolhidas
            atividades = []
            dia_to_index = {"Segunda": 0, "Terça": 1, "Quarta": 2, "Quinta": 3, "Sexta": 4}
            for d in grade:
                for a in d.get('atividades', []):
                    # converte deadline (dia,hora) para um número contínuo em horas
                    day = a.get('deadline_day')
                    hour = a.get('deadline_hour', 23)
                    day_idx = dia_to_index.get(day, 4)
                    # por simplicidade, definimos d = day_idx*24 + hour
                    deadline_num = day_idx * 24 + int(hour)
                    atividades.append({'nome': a.get('nome', d.get('nome')), 'p': int(a.get('duracao', 1)), 'd': deadline_num})

            if atividades:
                st.write('---')
                st.subheader('📝 Plano de Estudos (ordem EDD para minimizar L_max)')

                schedule, L_max = schedule_minimize_lateness(atividades)

                # Mostra tabela das atividades agendadas (com labels legíveis)
                df_sched = pd.DataFrame(schedule)
                # converte start/finish numericos para dia/hora legível
                def to_label(t):
                    day = int(t) // 24
                    hour = int(t) % 24
                    inv = {v: k for k, v in dia_to_index.items()}
                    return f"{inv.get(day,'?')} {hour}h"

                df_sched['start_label'] = df_sched['start'].apply(to_label)
                df_sched['finish_label'] = df_sched['finish'].apply(to_label)
                # deadline legível
                df_sched['d_label'] = df_sched['d'].apply(to_label)
                st.table(df_sched[['nome', 'p', 'd_label', 'start_label', 'finish_label', 'lateness']])
                st.write(f"**Máxima lateness (L_max):** {L_max} horas")

                # Gantt simples com plotly (converte horas numericas para datetimes)
                # usa a segunda-feira da semana atual como data base para que o eixo X mostre dias/horas
                today = datetime.today()
                monday = today - timedelta(days=today.weekday())
                base_date = pd.Timestamp(monday.date())
                df_fig = pd.DataFrame(schedule)
                df_fig['Start_dt'] = pd.to_datetime(df_fig['start'], unit='h', origin=base_date)
                df_fig['Finish_dt'] = pd.to_datetime(df_fig['finish'], unit='h', origin=base_date)
                df_fig = df_fig.sort_values('Start_dt')
                if not df_fig.empty:
                    fig = px.timeline(df_fig, x_start='Start_dt', x_end='Finish_dt', y='nome', color='nome')
                    fig.update_yaxes(autorange='reversed')
                    # formata o eixo X para mostrar dia abreviado e hora
                    fig.update_xaxes(tickformat='%a %H:%M')
                    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=300)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Nenhuma combinação possível sem conflito 😢")
