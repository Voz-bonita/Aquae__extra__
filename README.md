# Objetivo

Este repositório tem por objetivo organizar scripts interessantes que foram desenvolvidos para solucionar alguma demanda do [<i>aquae</i>](https://github.com/SamuelNoB/Aquae) e que sejam capazes de sustentar alguma grande utilidade sozinhos

### [`Coleta do IPCA`]

#### Motivação

Originalmente o <i>aquae</i> foi projetado utilizando preços dos equipamentos e peças necessárias para os sistemas de aproveitamento coletados em 2018, e com os fênomenos econômicos que regulam o mercado segue-se que os preços eventualmente ficaram desatualizados. Idealmente o simulador deveria se manter atualizado com o passar dos anos, para tanto começou-se por utilizar a cotação do dólar como indicador para atualização dos preços, entretanto, constatou-se que esse método gerava um sobre-preço dos equipamentos. Conversando com fornecedores destes produtos verificou-se que alguns dos mesmos estavam o utilizando o IPCA para corrigir os preços, e fazendo o mesmo no <i>aquae</i> obteve-se um retrato mais fidedigno das simulações.

### [`Coleta de Pluviometria`](Coleta_de_pluviometria/)

#### Motivação

Para a simulação do aproveitamento de água da chuva, o [<i>aquae</i>](https://github.com/SamuelNoB/Aquae) necessita dos dados sobre a chuva da região em questão, logo para expandir a inclusão do formulário em relação às cidades do Brasil precisava-se coletar os dados sobre pluviometria de mais cidades além de Brasília. O [INMET (Instituto Nacional de Meteorologia)](https://portal.inmet.gov.br/) fornece os dados da precipitação em cada cidade/estação na base de dados que pode ser acessada no próprio site.

##### [`Automação de navegador`](Coleta_de_pluviometria/Tabela_de_Pluviometria.py)

A primeira solução para o problema foi utilizar automação de navegador para acessar as tabelas com os dados, preenchendo o formulário e solicitando a tabela. Os principais problemas dessa ideia é que é um processo muito demorado fazer tantos GET requests na base de dados para obter a tabela e às vezes a tabela poderia não ser gerada por algum erro interno do site.

##### [`Requisições à API`](Coleta_de_pluviometria/Via_API.py)

A segunda solução foi utilizar as ferramentas do desenvolvedor diponíveis no navegador para encontrar o GET request que a página do INMET faz para a base de dados e utiliza essas informações para construir a tabela na página. Então com a url que leva à API é possível requisitar os dados diretamente da API sem precisar que eles sejam carregados na tabela e lendo a API no formato .json o processo de coleta ficou bem mais rápido. Outra vantagem desse método é que é possível automatizar requisições de tempos em tempos à base de dados do INMET para atulizar a base de dados do <i>aquae</i>.

##### [`Leitura de arquivos .csv`](Coleta_de_pluviometria/CSV_para_Json.py)

Pesquisando um pouco mais a fundo no site do [INMET](https://portal.inmet.gov.br/dadoshistoricos) e encontrar os dados históricos de todas as estações disponíveis separados em blocos de ano a ano e verificar que esses arquivos contém os dados diários, seguiu-se com a terceira solução, baixar todos esses zip's contendo csv's e escrever um script para extrair os dados de chuva e coloca-los em um arquivo de json, que servirá para popular a base de dados de pluviometria do <i>aquae</i> num primeiro momento.

A maior dificuldade dessa solução é que esses dados históricos tem pequenas variações de formatação e typos.

-   Sobre a formatação: existem datas que são da forma dd-mm-yyyy e outras da forma dd/mm/yyyy, tendo sido identificadas apenas essas duas até o momento (foram feitos alguns testes com regex, porém isso desacelera muito o código para coletar as informações de todos os csv).
-   Sobre os typos: encontraram-se nomes errados de estações, por exemplo em São Paulo a estação de Bebedouro tem dados apenas para 2021, porém há dados para a estação "Bebdouro" em anos anteriores.

**Obs**: Essa é visivelmente a solução que coleta os dados de forma mais rápida, entre as apresentadas aqui

##### [`Obtenção das medianas`](Coleta_de_pluviometria/Limpa_Pluviometria.py)

Dispondo dos dados de pluviometria de cada estação, organizados num [`único arquivo`](Coleta_de_pluviometria/Pluviometria_Brasil.json), seguiu-se com a obtenção de medianas de cada mês para fazer as simulações do <i>aquae</i>, excluindo para o cálculo dessas medianas os valores zerados e com isso excluindo estações que não apresentassem ao menos três valores não nulos em cada mês, uma vez que valores nulos poderiam ser valores que indicam a não medição da pluviometria e não de fato uma pluviometria nula. Obteve-se o resultado final [`Pluviometria_Mediana`](Coleta_de_pluviometria/Pluviometria_Mediana.json)
