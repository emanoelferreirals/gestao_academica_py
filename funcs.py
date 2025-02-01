import json, os

def formatar_email_user(email):
    return email.replace("@","_").replace(".com","")

def cadastrar_user(dados):
    # dados precisa é um dicionário
    usuario = formatar_email_user(dados["cadastro"]["email"])

    if os.path.exists(f"database/alunos/{usuario}.json"):
        return False
    else:
        with open(f"database/alunos/{usuario}.json","w") as aluno:
            json.dump(dados,aluno,indent=4)
        return True
    