
# Projeto de Aplicativo de Inventário de Estoque

## Descrição
Este projeto é um aplicativo de inventário de estoque desenvolvido em Python, utilizando o framework Kivy para a interface do usuário. O aplicativo permite aos usuários gerenciar contagens de estoque, operando com um banco de dados MySQL e oferecendo funcionalidades tanto online quanto offline.

## Características

- **Tela de Parametrização de Contagem**: Permite ao usuário inserir informações sobre a contagem atual e o número do operador.
- **Tela de Contagem**: Fornece campos para registrar endereço, código e quantidade de itens, com a busca de descrições de itens no banco de dados.
- **Gerenciamento de Banco de Dados**: Utiliza MySQL para armazenamento de dados.
- **Funcionalidade Offline**: Permite operações offline com sincronização posterior quando a conexão é restabelecida.
- **Validações**: Inclui validações para evitar contagens duplicadas no mesmo endereço para uma dada contagem.
- **Barra de Navegação**: Facilita a navegação entre as telas de parametrização e contagem.

## Como Configurar

### Pré-requisitos
- Python 3.x
- Kivy
- MySQL
- mysql-connector-python

### Instalação
1. Clone o repositório ou baixe o código fonte.
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o MySQL e crie o banco de dados e tabelas conforme as instruções no script SQL fornecido.

### Execução
Para executar o aplicativo, navegue até o diretório do projeto e execute o arquivo principal:
```bash
python main.py
```

## Estrutura do Projeto

- `main.py`: Arquivo principal que inicia o aplicativo.
- `screens.py`: Define as telas do aplicativo.
- `db_manager.py`: Gerencia as operações do banco de dados.
- `offline_queue.py`: Gerencia a fila de operações offline.
- `README.md`: Este arquivo.

## Contribuições
Contribuições são bem-vindas! Se você tem sugestões para melhorar este aplicativo, sinta-se à vontade para fazer um fork do repositório e enviar um pull request.

Para projetos destinados a uso livre e estudos, a Licença MIT é uma ótima opção. Ela é uma das licenças de software mais permissivas e é amplamente utilizada na comunidade de código aberto. Com a Licença MIT, os usuários podem fazer praticamente qualquer coisa com o seu projeto, incluindo usá-lo, modificá-lo e distribuí-lo, desde que incluam o aviso de direitos autorais e de permissão original.

Aqui está um exemplo do texto da Licença MIT que você pode incluir no seu projeto:

---

## Licença MIT

Copyright (c) 2023 Alexsandro Dos Santos Furtado

A permissão é concedida, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o "Software"), para lidar com o Software sem restrição, incluindo, sem limitações, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, e permitir que as pessoas a quem o Software é fornecido o façam, sujeitas às seguintes condições:

O aviso de direitos autorais acima e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do Software.

O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM PROPÓSITO ESPECÍFICO E NÃO INFRINGIMENTO. EM NENHUM CASO OS AUTORES OU DETENTORES DE DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM AÇÃO DE CONTRATO, TORTURA OU OUTRA FORMA, DECORRENTE DE, FORA DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.
