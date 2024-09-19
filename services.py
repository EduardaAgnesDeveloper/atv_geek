from sqlmodel import Session, select
from sqlalchemy import update
from fastapi import status, HTTPException
from database import get_engine
from models import ProdutosGeekModel
from dados import ProdutoDTO, AtualizarEstoqueDTO

class ProdutosGeekService:
    def __init__(self):
        self.session = Session(get_engine())

    def get_product_by_id(self, id: int):
        query = select(ProdutosGeekModel).where(ProdutosGeekModel.id == id)
        return self.session.exec(query).one_or_none()

    def get_all_products(self, nome: str = None, preco: float = None, categoria: str = None, franquia: str = None):
        filters = []
        if nome is not None:
            filters.append(ProdutosGeekModel.nome == nome)
        if preco is not None:
            filters.append(ProdutosGeekModel.preco == preco)
        if categoria is not None:
            filters.append(ProdutosGeekModel.categoria == categoria)
        if franquia is not None:
            filters.append(ProdutosGeekModel.franquia == franquia)

        query = select(ProdutosGeekModel)
        if filters:
            query = query.where(*filters)

        return self.session.exec(query).all()

    def save_product(self, product: ProdutosGeekModel):
        self.session.add(product)
        self.session.commit()
        return self.session.refresh(product)

    def atualizar_estoque(self, id: int, dados_estoque: AtualizarEstoqueDTO):
        produto = self.get_product_by_id(id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")

        nova_quantidade = produto.qtd_estoque + dados_estoque.quantidade

        if nova_quantidade < 0:
            raise HTTPException(status_code=400, detail="Estoque insuficiente.")

        produto.qtd_estoque = nova_quantidade
        self.session.commit()
        return self.session.refresh(produto)

    def delete_product(self, id: int):
        produto = self.get_product_by_id(id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado.")
        
        if produto.qtd_estoque > 0:
            raise HTTPException(status_code=400, detail="Não é possível excluir um produto com estoque disponível.")

        self.session.delete(produto)
        self.session.commit()
        return {"ok": status.HTTP_200_OK}
