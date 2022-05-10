# Objetivo

Este repositório tem por objetivo organizar scripts interessantes que foram desenvolvidos para solucionar alguma demanda do [Aquae](https://github.com/SamuelNoB/Aquae) e que sejam capazes de sustentar alguma grande utilidade sozinhos

### Coleta_de_Pluviometria

Para a simulação do aproveitamento de água da chuva, o [Aquae](https://github.com/SamuelNoB/Aquae) necessita dos dados sobre a chuva da região em questão, logo para expandir a inclusão do formulário em relação às cidades do Brasil precisava-se coletar os dados sobre pluviometria de mais cidades além de Brasília. O [INMET (Instituto Nacional de Meteorologia)](https://portal.inmet.gov.br/) fornece os dados da precipitação em cada cidade/estação na base de dados que pode ser acessada no próprio site.

A primeira solução para o problema foi utilizar automação de navegador para acessar as tabelas com os dados, preenchendo o formulário e solicitando a tabela. Os principais problemas dessa ideia é que é um processo muito demorado fazer tantos GET requests na base de dados para obter a tabela e às vezes a tabela poderia não ser gerada por algum erro interno do site.

A segunda solução foi utilizar as ferramentas do desenvolvedor diponíveis no navegador para encontrar o GET request que a página do INMET faz para a base de dados e utiliza essas informações para construir a tabela na página. Então com a url que leva à API é possível requisitar os dados diretamente da API sem precisar que eles sejam carregados na tabela e lendo a API no formato .json o processo de coleta ficou bem mais rápido. Outra vantagem desse método é que é possível automatizar requisições de tempos em tempos à base de dados do INMET para atulizar a base de dados do <i>aquae</i>.
