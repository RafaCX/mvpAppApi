## Requisitos

Antes de executar a aplicação, certifique-se de ter:

- Python instalado na versão 3.7 ou superior.
- `pip` configurado corretamente para gerenciar pacotes Python.
- As dependências listadas no arquivo `requirements.txt`.

Recomenda-se fortemente o uso de um ambiente virtual para evitar conflitos de dependências.

---

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar a API:

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_REPOSITORIO>
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv env
   ```

3. Ative o ambiente virtual:
   - **Linux/macOS**:
     ```bash
     source env/bin/activate
     ```
   - **Windows**:
     ```cmd
     .\env\Scripts\Activate
     ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Instale o Swagger (documentação automática):
   ```bash
   pip install -U flask-openapi3-swagger
   ```

---

## Executando a API

1. Inicie o servidor Flask:
   ```bash
   flask run --host 0.0.0.0 --port 5000 --reload
   ```

   O parâmetro `--reload` é útil em modo de desenvolvimento, pois reinicia o servidor automaticamente ao detectar mudanças no código.

2. Acesse a API no navegador ou por ferramentas como **Postman** ou **cURL**:
   - [http://localhost:5000/#/](http://localhost:5000/#/)
