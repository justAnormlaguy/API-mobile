from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from supabase import create_client, Client
import uuid
from fastapi.middleware.cors import CORSMiddleware

SUPABASE_URL = "https://fppvpwqpvjumgrvixspu.supabase.co"
SUPABASE_KEY = "sb_publishable_ppgrPprdn0v43tQRjUtXlA_DW_ULofX"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="API Biblioteca de Jogos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class LoginRequest(BaseModel):
    email: str
    password: str


class JogoRequest(BaseModel):
    nome: str
    tipo: str
    nota: int
    review: str


@app.post("/login", status_code=status.HTTP_200_OK)
def login(dados: LoginRequest):
    if dados.email == "usuario@esoft.com" and dados.password == "Abc123":
        return {"token": str(uuid.uuid4())}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@app.get("/jogos", status_code=status.HTTP_200_OK)
def listar_jogos():
    resposta = supabase.table("Jogos-API").select("*").execute()
    return resposta.data


@app.get("/jogos/{id}", status_code=status.HTTP_200_OK)
def buscar_jogo(id: int):
    resposta = supabase.table("Jogos-API").select("*").eq("id", id).execute()
    if not resposta.data:
        raise HTTPException(status_code=404, detail="Jogo nao encontrado")
    return resposta.data[0]


@@app.post("/jogos", status_code=status.HTTP_201_CREATED)
def cadastrar_jogo(jogo: JogoRequest):
    # Validação da nota
    if jogo.nota < 0 or jogo.nota > 10:
        raise HTTPException(status_code=400, detail="A nota deve ser de 0 a 10")

    resposta = supabase.table("Jogos-API").insert(jogo.dict()).execute()

    if not resposta.data:
        raise HTTPException(status_code=400, detail="Erro ao salvar no banco de dados")
    return resposta.data[0]


@app.put("/jogos/{id}", status_code=status.HTTP_200_OK)
def atualizar_jogo(id: int, jogo_atualizado: JogoRequest):
    # Validação da nota
    if jogo_atualizado.nota < 0 or jogo_atualizado.nota > 10:
        raise HTTPException(status_code=400, detail="A nota deve ser de 0 a 10")

    existente = supabase.table("Jogos-API").select("*").eq("id", id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    resposta = supabase.table("Jogos-API").update(jogo_atualizado.dict()).eq("id", id).execute()
    return resposta.data[0]

@app.delete("/jogos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_jogo(id: int):
    existente = supabase.table("Jogos-API").select("*").eq("id", id).execute()
    if not existente.data:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    supabase.table("Jogos-API").delete().eq("id", id).execute()
    return