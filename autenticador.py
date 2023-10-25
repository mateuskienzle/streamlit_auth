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

if __name__ == "__main__":
    main()