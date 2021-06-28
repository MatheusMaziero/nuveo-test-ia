# InstruÃ§Ãµes
- As questÃµes devem ser respondidas neste prÃ³prio documento `markdown`.
- Quaisquer referÃªncias, como papers, pÃ¡ginas web, imagens, etc, podem ser utilizadas para composiÃ§Ã£o das respostas. PorÃ©m, Ã© recomendado que as respostas sejam objetivas e diretas.
- NÃ£o hÃ¡ uma resposta correta para cada pergunta, de forma que a avaliaÃ§Ã£o nÃ£o serÃ¡ feita com comparaÃ§Ã£o da resposta fornecida com um gabarito. A ideia da proposta Ã© fornecer a oportunidade de demonstrar o conhecimento na construÃ§Ã£o de uma soluÃ§Ã£o para o cenÃ¡rio proposto, levantar possÃ­veis limitaÃ§Ãµes, impedimentos e como os problemas podem ser evitados ou minimizados, sem que seja necessÃ¡rio dedicar tempo com experimentos, treinos e determinaÃ§Ã£o de parÃ¢metros de forma empÃ­rica.


# Perguntas

1-Explique, de forma objetiva, qual abordagem seria escolhida para soluÃ§Ã£o do problema proposto. Caso a abordagem envolva Redes Neurais, descreva qual seria a arquitetura de rede utilizada e por que.
R: A solução deve ser construída por camadas. A primeira camada seria utilizando uma rede classificadora para separa as regiões do texto para localizar o campo de assinaturas. Como num cenário podemos ter milhares de usa rios para determinar a sua assinatura temos que combinar técnicas de processamento de imagem.Através de uma banco de dados de imagens com assinaturas cadastradas do usuário realizamos uma comparação entre as imagens aplicando uma técnica para analisar o contorno da assinatura com variação de píxel. Selecionamos registros chaves para analisar e comparar. Realizamos a comparação de histograma entre as imagens. Comparação de contornos e suas variações com dilatação e erosão da imagem. Leitura de OCR para determinar letras e números que podem estar nas assinaturas.

2-Liste e explique qual a linguagem, framework, pacotes e ferramentas seriam utilizados para construÃ§Ã£o da soluÃ§Ã£o.
R:A linguagem ultiliza seria Python, e os frameworks seria OpenCV,Numpy,Pandas,Django,Os,scikit-learn,PyQt5,csv e outros pacotes de manipulações de arquivos. Para rede neural usuário a Darknet e Yolov4

3-Quais os principais parÃ¢metros da soluÃ§Ã£o e como melhor otimizar a escolha de tais parÃ¢metros?
R: Para a parte da rede neural podemos otimizar o peso do modelo para determinar os parâmetros de calibração de rede. Para a parte podemos determinar as porcentagens dos filtros que devemos aplicar para otimizar a solução. Depois de tudo pronta podemos usar modelos como tensorrt para acelerar o processo.

4-Quais limitaÃ§Ãµes podem impactar a soluÃ§Ã£o proposta, seja em relaÃ§Ã£o Ã  prÃ³pria abordagem escolhida ou em relaÃ§Ã£o ao dataset fornecido para treino e teste?
R:O acesso à base de dados ou criação da base de dados. A não disponibilidade do servidor para teste e treino.

5-Qual seria o prazo proposto para o desenvolvimento da soluÃ§Ã£o proposta?
R: 2 semanas seria um tempo viável para uma proposta inicial

6-Considerando um cenÃ¡rio real de uso do mÃ©todo desenvolvido para detecÃ§Ã£o de fraudes em assinatura, o erro mais prejudicial seria retornar que uma assinatura Ã© legÃ­tima quando se trata de uma assinatura forjada. Como minimizar este tipo de erro?
R: Seria a utilização de uma chave token que usuário dever ter inserido junto ao documento e com a validação das duas seria dado a aprovação,

7-O que poderia ser alterado na disposiÃ§Ã£o de dados para auxiliar o resultado da soluÃ§Ã£o proposta?
R: Poderia ser variado as cores das assinaturas, rotações leves,e outros parâmetros das imagens. Cadastros de mais assinaturas reais para o dataset. Assinaturas com nomes completos.