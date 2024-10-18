import streamlit as st
import requests

# Base URL da API do backend (Flask)
BASE_URL = "http://127.0.0.1:5000"

# Função genérica para fazer requisições ao backend
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    url = f"{BASE_URL}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        else:
            st.error("Método HTTP não suportado.")
            return None

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            st.success("Operação realizada com sucesso!")
            return response.json()
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")

        return None

    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        return None

# Título principal com layout centralizado e espaçamento
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🚲 Empréstimo de Bikes</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #5D6D7E;'>Encontre a bike ideal para você</h4>", unsafe_allow_html=True)
st.write("")

# Sidebar para os filtros e opções
opcao = st.sidebar.selectbox(
    "Escolha uma funcionalidade",
    ["Gerenciar Usuários", "Gerenciar Bikes", "Gerenciar Empréstimos"]
)

# USUARIOS
if opcao == "Gerenciar Usuários":
    st.sidebar.header("👤 Gestão de Usuários")

    # Opções para visualizar ou gerenciar usuários
    acao_usuario = st.sidebar.selectbox("Ação", ["Visualizar Usuários", "Adicionar Usuário", "Atualizar Usuário", "Excluir Usuário"])

    if acao_usuario == "Visualizar Usuários":
        st.header("👥 Lista de Usuários")
        usuarios = fazer_requisicao('usuarios')

        if usuarios and 'usuarios' in usuarios:
            for usuario in usuarios['usuarios']:
                st.markdown(f"**ID:** {usuario['id']}, **Nome:** {usuario['nome']}, **CPF:** {usuario['cpf']}")
        else:
            st.warning("⚠️ Nenhum usuário encontrado.")

    elif acao_usuario == "Adicionar Usuário":
        st.header("➕ Adicionar Novo Usuário")
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        data_nascimento = st.date_input("Data de Nascimento")

        if st.button("Adicionar Usuário"):
            if nome and cpf and data_nascimento:
                dados_usuario = {
                    "nome": nome,
                    "cpf": cpf,
                    "data_de_nascimento": str(data_nascimento)
                }
                fazer_requisicao('usuarios', method="POST", data=dados_usuario)
            else:
                st.error("⚠️ Todos os campos são obrigatórios.")

    elif acao_usuario == "Atualizar Usuário":
        st.header("✏️ Atualizar Usuário")
        user_id = st.text_input("ID do Usuário para atualizar")
        novo_nome = st.text_input("Novo Nome")
        novo_cpf = st.text_input("Novo CPF")
        nova_data_nascimento = st.date_input("Nova Data de Nascimento")

        if st.button("Atualizar Usuário"):
            if user_id and novo_nome and novo_cpf and nova_data_nascimento:
                dados_atualizados = {
                    "nome": novo_nome,
                    "cpf": novo_cpf,
                    "data_de_nascimento": str(nova_data_nascimento)
                }
                fazer_requisicao(f'usuarios/{user_id}', method="PUT", data=dados_atualizados)
            else:
                st.error("⚠️ Todos os campos são obrigatórios.")

    elif acao_usuario == "Excluir Usuário":
        st.header("❌ Excluir Usuário")
        user_id = st.text_input("ID do Usuário para excluir")

        if st.button("Excluir Usuário"):
            if user_id:
                response = fazer_requisicao(f'usuarios/{user_id}', method="DELETE")
                if response:
                    st.success("✅ Bike excluída com sucesso!")
            else:
                st.warning("⚠️ O ID da bike é obrigatório.")

# BIKES
elif opcao == "Gerenciar Bikes":
    st.sidebar.header("🚲 Gestão de Bikes")

    # Opções para visualizar ou gerenciar bikes
    acao_bike = st.sidebar.selectbox("Ação", ["Visualizar Bikes", "Adicionar Bike", "Atualizar Bike", "Excluir Bike"])

    if acao_bike == "Visualizar Bikes":
        st.header("🚲 Lista de Bikes")
        bikes = fazer_requisicao('bikes')

        if bikes and 'bikes' in bikes:
            for bike in bikes['bikes']:
                st.markdown(f"**ID:** {bike['id']}, **Marca:** {bike['marca']}, **Modelo:** {bike['modelo']}, **Cidade:** {bike['cidade']}")
        else:
            st.warning("⚠️ Nenhuma bike encontrada.")

    elif acao_bike == "Adicionar Bike":
        st.header("➕ Adicionar Nova Bike")
        marca = st.text_input("Marca da bike:")
        modelo = st.text_input("Modelo da bike:")
        cidade = st.text_input("Cidade:")

        if st.button("Adicionar Bike"):
            if marca and modelo and cidade:
                bike_data = {
                    "marca": marca,
                    "modelo": modelo,
                    "cidade": cidade
                }
                response = fazer_requisicao('bikes', method="POST", data=bike_data)
                if response:
                    st.success("✅ Bike adicionada com sucesso!")
            else:
                st.warning("⚠️ Todos os campos são obrigatórios.")

    elif acao_bike == "Atualizar Bike":
        st.header("✏️ Atualizar Bike")
        id_bike = st.text_input("ID da Bike para atualizar:")
        marca_editar = st.text_input("Nova Marca:")
        modelo_editar = st.text_input("Novo Modelo:")
        cidade_editar = st.text_input("Nova Cidade:")

        if st.button("Atualizar Bike"):
            if id_bike and (marca_editar or modelo_editar or cidade_editar):
                data_atualizar = {}
                if marca_editar:
                    data_atualizar['marca'] = marca_editar
                if modelo_editar:
                    data_atualizar['modelo'] = modelo_editar
                if cidade_editar:
                    data_atualizar['cidade'] = cidade_editar

                response = fazer_requisicao(f'bikes/{id_bike}', method="PUT", data=data_atualizar)
                if response:
                    st.success("✅ Bike atualizada com sucesso!")
            else:
                st.warning("⚠️ Preencha o ID e ao menos um campo para atualização.")

    elif acao_bike == "Excluir Bike":
        st.header("❌ Excluir Bike")
        id_bike = st.text_input("ID da Bike para excluir")

        if st.button("Excluir Bike"):
            if id_bike:
                response = fazer_requisicao(f'bikes/{id_bike}', method="DELETE")
                if response:
                    st.success("✅ Bike excluída com sucesso!")
            else:
                st.warning("⚠️ O ID da bike é obrigatório.")

# EMPRESTIMOS
if opcao == "Gerenciar Empréstimos":
    st.sidebar.header("📄 Gestão de Empréstimos")

    # Opções para visualizar ou gerenciar empréstimos
    acao_emprestimo = st.sidebar.selectbox("Ação", ["Visualizar Empréstimos", "Criar Empréstimo", "Finalizar Empréstimo"])

    if acao_emprestimo == "Visualizar Empréstimos":
        st.header("📄 Lista de Empréstimos")
        emprestimos = fazer_requisicao('emprestimos')

        if emprestimos and 'emprestimos' in emprestimos:
            for emprestimo in emprestimos['emprestimos']:
                st.markdown(f"**ID Empréstimo:** {emprestimo['_id']}, **Usuário:** {emprestimo['usuario_id']}, **Bike:** {emprestimo['bike_id']}, **Data de aluguel:** {emprestimo['data_aluguel']}")
        else:
            st.warning("⚠️ Nenhum empréstimo encontrado.")

    elif acao_emprestimo == "Criar Empréstimo":
        st.header("➕ Criar Novo Empréstimo")
        user_id = st.text_input("ID do Usuário")
        bike_id = st.text_input("ID da Bike")

        if st.button("Criar Empréstimo"):
            if user_id and bike_id:
                dados_emprestimo = {
                    "usuario_id": user_id,
                    "bike_id": bike_id
                }
                fazer_requisicao(f'emprestimos/usuarios/{user_id}/bikes/{bike_id}', method="POST", data=dados_emprestimo)
            else:
                st.error("⚠️ Todos os campos são obrigatórios.")

    elif acao_emprestimo == "Finalizar Empréstimo":
        st.header("❌ Finalizar Empréstimo")
        emprestimo_id = st.text_input("ID do Empréstimo para finalizar")

        if st.button("Finalizar Empréstimo"):
            if emprestimo_id:
                fazer_requisicao(f'emprestimos/{emprestimo_id}', method="DELETE", data={"status": "finalizado"})
            else:
                st.warning("⚠️ O ID do empréstimo é obrigatório.")


