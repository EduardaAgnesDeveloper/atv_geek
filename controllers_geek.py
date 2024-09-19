from fastapi import APIRouter, status, HTTPException
from models import ProdutosGeekModel
from services import ProdutosGeekService
from dados import ProdutoDTO, AtualizarEstoqueDTO

router = APIRouter()
produto_service = ProdutosGeekService()

@router.get("/{id}", response_model=ProdutosGeekModel)
def get_product_by_id(id: int):
    produto = produto_service.get_product_by_id(id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto

@router.get("/")
def products_list(
    nome: str = None,
    preco: float = None,
    categoria: str = None,
    franquia: str = None
):
    return produto_service.get_all_products(nome, preco, categoria, franquia)

@router.post("/", response_model=ProdutosGeekModel, status_code=status.HTTP_201_CREATED)
def add_product(product: ProdutoDTO):
    novo_produto = ProdutosGeekModel(
        nome=product.nome,
        desc=product.desc,
        preco=product.preco,
        qtd_estoque=product.qtd_estoque,
        categoria=product.categoria,
        franquia=product.franquia
    )
    return produto_service.save_product(novo_produto)

@router.put("/{id}", response_model=ProdutosGeekModel)
def update_product(id: int, product: ProdutoDTO):
    db_produto = ProdutosGeekModel(
        id=id, 
        nome=product.nome,
        desc=product.desc,
        preco=product.preco,
        qtd_estoque=product.qtd_estoque,
        categoria=product.categoria,
        franquia=product.franquia
    )
    return produto_service.update_product(db_produto, id)

@router.put("/estoque/{id}", response_model=ProdutosGeekModel)
def atualizar_estoque(id: int, dds: AtualizarEstoqueDTO):
    produto = produto_service.get_product_by_id(id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    try:
        produto_atualizado = produto_service.atualizar_estoque(id, dds)
        return produto_atualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    produto_service.delete_product(id)
    return {"detail": "Produto excluído com sucesso"}
