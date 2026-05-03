import streamlit as st
from groq import Groq
import json
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Professor Bot", layout="wide")

# Conexão com o Llama 3
client = Groq(api_key="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")

# --- INTERFACE LATERAL (MENU) ---
st.sidebar.title("🍎 Professor Bot")
opcao = st.sidebar.selectbox("Ir para:", 
    ["Início", "📝 Criar Atividade", "✅ Corrigir Tarefa", "👥 Gerenciar Alunos", "📊 Relatórios"])

# Simulação de banco de dados (Para teste local)
# No futuro, conectaremos isso ao GitHub para não perder dados
if 'alunos' not in st.session_state:
    st.session_state.alunos = {}

# --- FUNÇÃO: CRIAR ATIVIDADE ---
if opcao == "📝 Criar Atividade":
    st.header("Nova Atividade")
    serie = st.selectbox("Série", ["6º Ano", "9º Ano"])
    titulo = st.text_input("Título da Atividade")
    resumo = st.text_area("Resumo da Apostila")
    
    if st.button("Gerar Atividade"):
        with st.spinner("O Llama está redigindo..."):
            prompt = f"Professor de português, {serie}. Tema: {titulo}. Base: {resumo}. Questões e gabarito."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.markdown("### Resultado:")
            st.write(res.choices[0].message.content)

# --- FUNÇÃO: GERENCIAR ALUNOS ---
elif opcao == "👥 Gerenciar Alunos":
    st.header("Gestão de Turmas")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do Aluno")
        turma = st.selectbox("Turma", ["6A", "6B", "6C", "9A", "9B", "9C"])
        if st.button("Cadastrar"):
            st.session_state.alunos[nome] = {"turma": turma, "historico": []}
            st.success(f"{nome} cadastrado!")
            
    with col2:
        st.subheader("Alunos Ativos")
        st.write(st.session_state.alunos)

# --- FUNÇÃO: CORREÇÃO ---
elif opcao == "✅ Corrigir Tarefa":
    st.header("Corretor Inteligente")
    aluno_sel = st.selectbox("Selecionar Aluno", list(st.session_state.alunos.keys()))
    respostas = st.text_area("Cole as respostas do aluno")
    
    if st.button("Analisar"):
        prompt = f"Corrija estas respostas: {respostas}. Diga se o aluno evoluiu."
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
        st.info(res.choices[0].message.content)