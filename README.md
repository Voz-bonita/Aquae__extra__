# Objetivo

Este repositório tem por objetivo organizar scripts interessantes que foram desenvolvidos para solucionar alguma demanda do [Aquae](https://github.com/SamuelNoB/Aquae) e que sejam capazes de sustentar alguma grande utilidade sozinhos

### Coleta_de_Pluviometria

Para a simulação do aproveitamento de água da chuva, o [Aquae](https://github.com/SamuelNoB/Aquae) necessita dos dados sobre a chuva da região em questão, logo para expandir a inclusão do formulário em relação às cidades do Brasil precisava-se coletar os dados sobre pluviometria de mais cidades além de Brasília. O [INMET (Instituto Nacional de Meteorologia)](https://portal.inmet.gov.br/) fornece os dados da precipitação em cada cidade/estação na base de dados que pode ser acessada no próprio site.

A primeira solução para o problema foi utilizar automação de navegador para acessar as tabelas com os dados, preenchendo o formulário e solicitando a tabela. Os principais problemas dessa ideia é que é um processo muito demorado fazer tantos GET requests na base de dados para obter a tabela e às vezes a tabela poderia não ser gerada por algum erro interno do site.
