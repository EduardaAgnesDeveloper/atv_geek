from pydantic import BaseModel


class ProdutoDTO(BaseModel):
    nome: str
    desc: str 
    preco: float
    qtd_estoque: int
    categoria: str
    franquia: str 

class AtualizarEstoqueDTO(BaseModel):
    quantidade: int