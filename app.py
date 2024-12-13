from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, send_from_directory
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from Model import Session, Usuario, Categoria, Filme, Avaliacao
from logger import logger
from schema import *
from flask_cors import CORS

info = Info(title="Sistema de Avaliações", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Configurar caminho do frontend
FRONTEND_PATH = "../mvp_app_front/static"

# Rota para servir o frontend
@app.route('/')
def index():
    """Serve a página inicial do frontend."""
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve arquivos estáticos do frontend."""
    return send_from_directory(FRONTEND_PATH, path)

# Tags para a documentação
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuário", description="Adição, visualização e remoção de usuários na base")
categoria_tag = Tag(name="Categoria", description="Gestão de categorias de filmes")
filme_tag = Tag(name="Filme", description="Gestão de filmes na base")
avaliacao_tag = Tag(name="Avaliação", description="Gestão de avaliações de filmes")

# Rota inicial
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

# Usuários
@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo usuário à base de dados."""
    usuario = Usuario(nome=form.nome)
    logger.debug(f"Adicionando usuário com nome: '{usuario.nome}'")
    try:
        session = Session()
        session.add(usuario)
        session.commit()
        logger.debug(f"Usuário adicionado: '{usuario.nome}'")
        return apresenta_usuario(usuario), 200
    except IntegrityError:
        session.rollback()
        error_msg = "Usuário já existe na base."
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível adicionar o usuário."
        logger.error(f"Erro ao adicionar usuário '{usuario.nome}', {str(e)}")
        return {"mesage": error_msg}, 400

@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def listar_usuarios():
    """Lista todos os usuários cadastrados."""
    try:
        logger.debug("Iniciando coleta de usuários.")
        session = Session()
        usuarios = session.query(Usuario).all()
        if not usuarios:
            logger.warning("Nenhum usuário encontrado.")
            return {"usuarios": []}, 200
        logger.debug(f"Usuários encontrados: {[u.nome for u in usuarios]}")
        return apresenta_usuarios(usuarios), 200
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {str(e)}")
        return {"mesage": "Erro interno no servidor."}, 500


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def remover_usuario(query: UsuarioBuscaSchema):
    """Remove um usuário pelo nome."""
    usuario_nome = unquote(query.nome)
    logger.debug(f"Deletando usuário '{usuario_nome}'")
    session = Session()
    count = session.query(Usuario).filter(Usuario.nome == usuario_nome).delete()
    session.commit()
    if count:
        logger.debug(f"Usuário deletado: '{usuario_nome}'")
        return {"mesage": "Usuário removido", "nome": usuario_nome}, 200
    else:
        error_msg = "Usuário não encontrado."
        logger.warning(f"Erro ao deletar usuário '{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404

# Categorias
@app.post('/categoria', tags=[categoria_tag],
          responses={"200": CategoriaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_categoria(form: CategoriaSchema):
    """Adiciona uma nova categoria."""
    categoria = Categoria(nome=form.nome)
    logger.debug(f"Adicionando categoria '{categoria.nome}'")
    session = Session()
    try:
        session.add(categoria)
        session.commit()
        return apresenta_categoria(categoria), 200
    except IntegrityError:
        session.rollback()
        error_msg = "Categoria já existe."
        logger.warning(f"Erro ao adicionar categoria '{categoria.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

@app.get('/categorias', tags=[categoria_tag],
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def listar_categorias():
    """Lista todas as categorias cadastradas."""
    logger.debug("Coletando categorias")
    session = Session()
    try:
        categorias = session.query(Categoria).all()
        logger.debug(f"Categorias encontradas: {categorias}")
        if categorias:
            response = apresenta_categorias(categorias)
            logger.debug(f"Resposta: {response}")
            return response, 200
        return {"categorias": []}, 200
    except Exception as e:
        logger.error(f"Erro ao listar categorias: {str(e)}")
        return {"message": "Erro interno no servidor."}, 500

@app.delete('/categoria', tags=[categoria_tag],
            responses={"200": CategoriaDelSchema, "404": ErrorSchema})
def remover_categoria(query: CategoriaBuscaSchema):
    """Remove uma categoria pelo nome."""
    categoria_nome = unquote(query.nome)
    logger.debug(f"Deletando categoria '{categoria_nome}'")
    session = Session()
    count = session.query(Categoria).filter(Categoria.nome == categoria_nome).delete()
    session.commit()
    if count:
        return {"mesage": "Categoria removida", "nome": categoria_nome}, 200
    else:
        return {"mesage": "Categoria não encontrada."}, 404

# Filmes
@app.post('/filme', tags=[filme_tag],
          responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_filme(form: FilmeSchema):
    """Adiciona um novo filme."""
    filme = Filme(titulo=form.titulo, categoria_id=form.categoria_id, nota=form.nota)
    logger.debug(f"Adicionando filme '{filme.titulo}'")
    session = Session()
    try:
        session.add(filme)
        session.commit()
        return apresenta_filme(filme), 200
    except IntegrityError:
        session.rollback()
        return {"mesage": "Filme já existe."}, 409
    
@app.get('/filmes', tags=[filme_tag],
         responses={"200": ListagemFilmesSchema, "404": ErrorSchema})
def listar_filmes():
    """Lista todos os filmes."""
    logger.debug("Coletando filmes")
    session = Session()
    try:
        filmes = session.query(Filme).all()
        logger.debug(f"Filmes encontrados: {filmes}")
        if filmes:
            response = apresenta_filmes(filmes)
            logger.debug(f"Resposta: {response}")
            return response, 200
        return {"filmes": []}, 200
    except Exception as e:
        logger.error(f"Erro ao listar filmes: {str(e)}")
        return {"message": "Erro interno no servidor."}, 500
    
@app.delete('/filme', tags=[filme_tag],
            responses={"200": FilmeDelSchema, "404": ErrorSchema})
def remover_filme(query: FilmeBuscaSchema):
    """Remove um filme pelo ID ou título."""
    session = Session()

    try:
        # Busca o filme com base no ID ou título
        if query.id:
            filme = session.query(Filme).filter(Filme.id == query.id).first()
        elif query.titulo:
            filme = session.query(Filme).filter(Filme.titulo == query.titulo).first()
        else:
            return {"message": "É necessário fornecer um ID ou título para remover um filme."}, 400

        # Verifica se o filme existe
        if not filme:
            return {"message": "Filme não encontrado."}, 404

        # Remove o filme
        session.delete(filme)
        session.commit()

        logger.debug(f"Filme removido: ID={filme.id}, título='{filme.titulo}'")
        return {"message": "Filme removido com sucesso!", "id": filme.id}, 200

    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao remover filme: {str(e)}")
        return {"message": "Erro interno no servidor."}, 500

    finally:
        session.close()

@app.post('/filmes/categoria', tags=[filme_tag],
          responses={"200": FilmesPorCategoriaSchema, "404": ErrorSchema})
def listar_filmes_por_categoria(form: FilmesPorCategoriaSchema):
    """Lista todos os filmes de uma categoria específica."""
    categoria_id = form.categoria_id  # Obtém o categoria_id do formulário
    logger.debug(f"Buscando filmes da categoria #{categoria_id}")
    session = Session()
    
    try:
        # Realiza a consulta para obter filmes com o categoria_id fornecido
        filmes = session.query(Filme).filter(Filme.categoria_id == categoria_id).all()
        logger.debug(f"Filmes encontrados: {filmes}")
        
        if filmes:
            # Retorna a resposta com os filmes da categoria, usando a função de apresentação
            response = apresenta_filmes_por_categoria(filmes, categoria_id)
            logger.debug(f"Resposta: {response}")
            return response, 200
        
        # Caso não encontre filmes para a categoria
        logger.warning(f"Nenhum filme encontrado para a categoria #{categoria_id}")
        return {"message": "Nenhum filme encontrado para essa categoria."}, 404
    
    except Exception as e:
        # Caso haja algum erro no processo
        logger.error(f"Erro ao listar filmes por categoria: {str(e)}")
        return {"message": "Erro interno no servidor."}, 500

# Avaliações
@app.post('/avaliacao', tags=[avaliacao_tag],
          responses={"200": AvaliacaoViewSchema, "400": ErrorSchema})
def add_avaliacao(form: AvaliacaoSchema):
    """Adiciona ou altera uma avaliação para um filme.

    Atualiza a nota média do filme com base nas avaliações.
    """
    session = Session()

    # Verifica se o filme existe
    filme = session.query(Filme).filter(Filme.id == form.filme_id).first()
    if not filme:
        return {"message": "Filme não encontrado."}, 400

    # Verifica se o usuário já avaliou o filme
    avaliacao = session.query(Avaliacao).filter(
        Avaliacao.filme_id == form.filme_id,
        Avaliacao.usuario_id == form.usuario_id
    ).first()

    if avaliacao:
        # Atualiza a avaliação existente
        avaliacao.nota = form.nota
    else:
        # Adiciona uma nova avaliação
        avaliacao = Avaliacao(
            filme_id=form.filme_id,
            usuario_id=form.usuario_id,
            nota=form.nota,
        )
        session.add(avaliacao)

    # Atualiza a nota média do filme
    avaliacoes = session.query(Avaliacao).filter(Avaliacao.filme_id == form.filme_id).all()
    filme.nota = sum(a.nota for a in avaliacoes) / len(avaliacoes)

    session.commit()

    return apresenta_avaliacao(avaliacao), 200

