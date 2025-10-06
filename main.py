import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import os


load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


st.title("Agenda de Clientes 📒")

# Função para adicionar agendamento
def adicionando(cliente, oque_vai_fazer, data, horario):
    supabase.table("agenda").insert({
        "cliente": cliente,
        "oque_vai_fazer": oque_vai_fazer,
        "data": data,
        "horario": horario
    }).execute()

# Função para listar agendamentos
def mostra_lista():
    dados = supabase.table("agenda").select("*").execute()
    if dados.data:
        df = pd.DataFrame(dados.data)
        st.dataframe(df)
    else:
        st.info("Nenhum agendamento encontrado.")

# Função para atualizar agendamento
def atualizar_agendamento(id_agenda, nova_data, novo_horario, novo_servico=None):
    if novo_servico:
        supabase.table("agenda").update({
            "data": nova_data,
            "horario": novo_horario,
            "oque_vai_fazer": novo_servico
        }).eq("id", id_agenda).execute()
    else:
        supabase.table("agenda").update({
            "data": nova_data,
            "horario": novo_horario
        }).eq("id", id_agenda).execute()

# Função para deletar agendamento
def deletar_agendamento(id_agenda):
    supabase.table("agenda").delete().eq("id", id_agenda).execute()

# Menu lateral
menu = st.sidebar.radio("Menu", ["Adicionar", "Listar", "Atualizar", "Deletar"])

# Adicionar
if menu == "Adicionar":
    st.title("Cadastrar novo agendamento ✍️")
    cliente = st.text_input("Nome do cliente:")
    oque_vai_fazer = st.text_input("Serviço a ser realizado:")
    data = st.date_input("Data do agendamento:")
    horario = st.time_input("Horário do agendamento:")
    if st.button("Cadastrar Agendamento"):
        if cliente and oque_vai_fazer:
            adicionando(cliente, oque_vai_fazer, str(data), str(horario))
            st.success("Agendamento cadastrado com sucesso! ✅")
        else:
            st.warning("Preencha todos os campos antes de cadastrar.")

# Listar
if menu == "Listar":
    st.title("Agendamentos 📅")
    mostra_lista()

# Atualizar
if menu == "Atualizar":
    st.title("Atualizar agendamento ✏️")
    mostra_lista()
    id_agenda = st.number_input("Digite o ID do agendamento que deseja atualizar: ", min_value=1, step=1)
    nova_data = st.date_input("Nova data do agendamento:")
    novo_horario = st.time_input("Novo horário do agendamento:")
    novo_servico = st.text_input("Novo serviço (opcional):")
    if st.button("Atualizar Agendamento"):
        atualizar_agendamento(id_agenda, str(nova_data), str(novo_horario), novo_servico if novo_servico.strip() else None)
        st.success("Agendamento atualizado com sucesso!")

# Deletar
if menu == "Deletar":
    st.title("Excluir agendamento ❌")
    mostra_lista()
    id_agenda = st.number_input("Digite o ID do agendamento que deseja deletar: ", min_value=1, step=1)
    if st.button("Deletar Agendamento"):
        deletar_agendamento(id_agenda)
        st.success("Agendamento removido com sucesso!")
