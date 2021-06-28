# Instruções
- As questões devem ser respondidas neste próprio documento `markdown`.
- Quaisquer referências, como papers, páginas web, imagens, etc, podem ser utilizadas para composição das respostas. Porém, é recomendado que as respostas sejam objetivas e diretas.
- Não há uma resposta correta para cada pergunta, de forma que a avaliação não será feita com comparação da resposta fornecida com um gabarito. A ideia da proposta é fornecer a oportunidade de demonstrar o conhecimento na construção de uma solução para o cenário proposto, levantar possíveis limitações, impedimentos e como os problemas podem ser evitados ou minimizados, sem que seja necessário dedicar tempo com experimentos, treinos e determinação de parâmetros de forma empírica.


# Perguntas

1-Explique, de forma objetiva, qual abordagem seria escolhida para solução do problema proposto. Caso a abordagem envolva Redes Neurais, descreva qual seria a arquitetura de rede utilizada e por que.
R: A solu��o deve ser constru�da por camadas. A primeira camada seria utilizando uma rede classificadora para separa as regi�es do texto para localizar o campo de assinaturas. Como num cen�rio podemos ter milhares de usa rios para determinar a sua assinatura temos que combinar t�cnicas de processamento de imagem.Atrav�s de uma banco de dados de imagens com assinaturas cadastradas do usu�rio realizamos uma compara��o entre as imagens aplicando uma t�cnica para analisar o contorno da assinatura com varia��o de p�xel. Selecionamos registros chaves para analisar e comparar. Realizamos a compara��o de histograma entre as imagens. Compara��o de contornos e suas varia��es com dilata��o e eros�o da imagem. Leitura de OCR para determinar letras e n�meros que podem estar nas assinaturas.

2-Liste e explique qual a linguagem, framework, pacotes e ferramentas seriam utilizados para construção da solução.
R:A linguagem ultiliza seria Python, e os frameworks seria OpenCV,Numpy,Pandas,Django,Os,scikit-learn,PyQt5,csv e outros pacotes de manipula��es de arquivos. Para rede neural usu�rio a Darknet e Yolov4

3-Quais os principais parâmetros da solução e como melhor otimizar a escolha de tais parâmetros?
R: Para a parte da rede neural podemos otimizar o peso do modelo para determinar os par�metros de calibra��o de rede. Para a parte podemos determinar as porcentagens dos filtros que devemos aplicar para otimizar a solu��o. Depois de tudo pronta podemos usar modelos como tensorrt para acelerar o processo.

4-Quais limitações podem impactar a solução proposta, seja em relação à própria abordagem escolhida ou em relação ao dataset fornecido para treino e teste?
R:O acesso � base de dados ou cria��o da base de dados. A n�o disponibilidade do servidor para teste e treino.

5-Qual seria o prazo proposto para o desenvolvimento da solução proposta?
R: 2 semanas seria um tempo vi�vel para uma proposta inicial

6-Considerando um cenário real de uso do método desenvolvido para detecção de fraudes em assinatura, o erro mais prejudicial seria retornar que uma assinatura é legítima quando se trata de uma assinatura forjada. Como minimizar este tipo de erro?
R: Seria a utiliza��o de uma chave token que usu�rio dever ter inserido junto ao documento e com a valida��o das duas seria dado a aprova��o,

7-O que poderia ser alterado na disposição de dados para auxiliar o resultado da solução proposta?
R: Poderia ser variado as cores das assinaturas, rota��es leves,e outros par�metros das imagens. Cadastros de mais assinaturas reais para o dataset. Assinaturas com nomes completos.