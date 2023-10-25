import streamlit as st
import streamlit_authenticator as stauth

COOKIE_EXPIRY_DAYS = 14
PREAUTHORIZED = {'emails': ['teste@teste.com']}
def main():
    authenticator = stauth.Authenticate(
        {'usernames': {'teste': {'name': 'testando', 'password': 'blabla'},}},
        
        'teste',
        'teste',
        COOKIE_EXPIRY_DAYS,
        PREAUTHORIZED
        )

    if 'clicou_registrar' not in st.session_state:
        st.session_state['clicou_registrar'] = False

    if st.session_state['clicou_registrar'] == False:
        login_form(authenticator=authenticator)
    else:
        pass

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

if __name__ == "__main__":
    main()