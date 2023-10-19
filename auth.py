import streamlit as st
import streamlit_authenticator as stauth
from dependencies import add_registro, consulta, consulta_geral, create_table
from time import sleep

def main():
    try:
        consulta_geral()
    except:
        create_table()

    db_query = consulta_geral()

    registers = {'usernames': {}}
    for data in db_query:
        registers['usernames'][data[1]] = {'name' : data[0], 'password' : data[2]}

    COOKIE_EXPIRY_DAYS = 30
    PREAUTHORIZED = {'emails': ['melsby@gmail.com']}

    authenticator = stauth.Authenticate(
        registers,
        'random_cookie_name',
        'random_signature_key',
        COOKIE_EXPIRY_DAYS,
        PREAUTHORIZED
    )
    # Valor default do estado "clicou_registrar"
    if 'clicou_registrar' not in st.session_state:
        st.session_state['clicou_registrar'] = False

    if st.session_state['clicou_registrar'] == False:
        login_form(authenticator=authenticator)
    else:
        username_form()


def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login')
    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'*{name} está logado!*')
        st.title('AREA DO DASHBOARD')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        clicou_em_registrar = st.button("Registrar")
        if clicou_em_registrar:
            st.session_state['clicou_registrar'] = True
            st.rerun()


def confirmation_msg():
    hashed_password = stauth.Hasher([st.session_state.pswrd]).generate()
    if st.session_state.pswrd != st.session_state.confirm_pswrd:
        st.warning('Senhas não conferem')
        sleep(3)
    elif consulta(st.session_state.user):
        st.warning('Nome de usuário já existe.')
        sleep(3)
    else:
        add_registro(st.session_state.nome,st.session_state.user, hashed_password[0])
        st.success('Registro efetuado!')
        sleep(3)

def username_form():
    with st.form(key="test", clear_on_submit=True):
        nome = st.text_input("Nome", key="nome")
        username = st.text_input("Usuário", key="user")
        password = st.text_input("Password", key="pswrd", type="password")
        confirm_password = st.text_input("Confirm Password", key="confirm_pswrd", type="password")
        submit = st.form_submit_button(
            "Salvar", on_click=confirmation_msg,
        )
    clicou_em_fazer_login = st.button("Fazer Login")
    if clicou_em_fazer_login:
        st.session_state['clicou_registrar'] = False
        st.rerun()

if __name__ == "__main__":
    main()