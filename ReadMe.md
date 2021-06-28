# Nuevo Test Ia
![Build Status](https://www.python.org/static/community_logos/python-powered-w-100x40.png) ![colab](https://user-images.githubusercontent.com/4096485/86174097-b56b9000-bb29-11ea-9240-c17f6bacfc34.png)
## Sumario
-Instalação
-01-Wheres Wally
-02-Spam Detection
-03-FraudDetection

## Resumo
Este repositório contem 3 desafios para testar a capacidade de trabalhar com ia. Este desafio foi proposto pela empresa Nuevo.
Os 3 Desafios são:
-01-Wheres Wally - Desafio de Classificação de imagens
-02-Spam Detection-  Classificação de textos
-03-FraudDetection - Criação de Solução Anti-Fraude pelo usuário

## Instalção
Faça download do repositório e utilize o seguinte comando:
```sh
 python -m pip3 install -r requirements.txt
```
## 01-Wheres Wally
Este desafio o objetivo era localizar o personagem Wally e determinar a posição do centro da image Wally nas imagens  de testes.

### Dataset
O dataset possui algumas falhas de anotações e deveriam ser arrumadas. Usando a Ferramenta [Labelme](https://github.com/wkentaro/labelme) foi refeito as anotações incorretas e depois usando a ferramenta [Roboflow](https://roboflow.com/) foi convertido para o formato Yolo(.txt) para poder realizar o treinamento.
O Yolo é um dos algorítimos de Object Detection com maior poder de detecção, você pode encontrar no repositório da [Darknet](https://github.com/AlexeyAB/darknet)
Foi utilizando um algorítimo pessoal de data argumentation para treinar o dataset. Conseguimos uma proporção de imagem de 1x288 resultando em 36864 imagens
Separando em proporção de 80 % para treino e 20 % para teste

### Treinamento
O treinamento foi realizado no GCP-GOOGLE CLOUD PLATAFORM levando cerca de 5 horas para obter uma acurácia de 97%

### Inferencia
Para realizar o Test criado uma GUI para otimizar o tempo de resultado
Para rodar código use o comando na pasta do 01-Wheres Wally
```sh
python main.py
```

O Script yolo_image.py que faz o processamento yolo para uma imagem esta na pasta scr
O Modelo esta na pasta cfg
Os pesos estão neste [link](https://drive.google.com/drive/folders/1bFNLJi6V8tIhBoJRih-VIYhaUIcdLl2-?usp=sharing) e você pode anexa-lo na pasta weights
As Classes estão na pasta classes.
Ao executar o comando uma GUI sera aberta
Passos
-1 Selecione o modelo(cfg)
-2 Selecione os pesos(weights)
-3 Selecione a pasta das imagens
-4 Navegue entre as imagens usando o Botão Next Image,Back Image
-5 Pode clicar duas vezes no nome das imagens na Lista de Imagens ou na Tabela de Resultados de todas as imagens para se mover também
-6 Você pode salvar os resultados usando o botão save results
7- Você pode usuario pode Clear Results para limpar os resultados

Na Tabela de Resultado Individua temos como saída a classe, os centroides e a precisão da classificação.
Na Tabela de Todos os Resultados temos como saída a classe, os centroides e a precisão da classificação de todas as imagens
Na tela de "Disposição da Imagem"  temos a imagem com seu bounding box, sua precisão e o tempo de processamento

### Conclução
O método utilizando uma GUI facilitou os testes e validação do modelo. Com os centroides resultados pelo modelo devemos realizar uma escala de razão entre tamanho utilizado para inferência e o tamanho original da imagem para determinar o valor correto do centroide.

## 02-Spam Detection
Neste desafio o objetivo era criar uma classe chamada c com dois métodos: E Um método prob_spam , que deve retornar a probabilidade, entre 0 e 1, de que a mensagem de entrada seja spam e um método is_spam , que deve retornar um valor booliano de True se a mensagem for um spam e False se a mensagem for um ham . Para construção do método is_spam , considere um cenário real em que o usuário final não aceita que spam seja direcionado para sua caixa de entrada, mas não se importa se alguns ham sejam classificados como spam.
Também era necessário criar um programa de testes dos métodos da classe SpamDetection

### Modelo
O modelo foi pre disposto e sem encontra na pasta Model. Ele possui a extensão .pkl

### Dataset
O Dataset para treino e validação se encontra na pasta TrainingSet em formato csv e Dataset de test esta na pasta TestSet. Os Dataset de treino e validação possui duas colunas a mensagem e o tipo da mensagem(ham ou spam). No Dataset de test existe apenas a coluna com as mensagens.

### Infencia
O Script com a classe SpamDetection esta na pasta scr. O Usuário precisa passar uma string com a mensagem e o caminho do modelo. Para facilitar o teste foi criado uma GUI onde que o usuário seleciona o caminho do modelo e o caminho de um arquivo csv para os testes. Na pasta 02-SpamDetection use o comando:
```sh
python main.py
```

Apos executar o comando uma GUI sera aberta
Passos
-1 Selecione o modelo(pkl)
-2 Selecione o arquivo csv para tests
-3 Navegue entre as strings usando o Botão Next Image,Back Image
-5 Pode clicar duas vezes no nome da string na Tabela de String
-6 Você pode salvar os resultados usando o botão save results
7- Você pode usuário pode Clear Results para limpar os resultados

Como Resultado na Tabela de Classificação temos A mensagem original, a sua probabilidade de ser um spam,se é true ou false que ela é um spam e na coluna a mensagem verificada se for do tipo Ham

### Algorítimo de teste
Foi criado um arquivo chamado testmodel.py onde que o usuário insere o caminho do modelo e caminho do arquivo csv de treino e através da biblioteca [Unites](https://docs.python.org/3/library/unittest.html)
Os testes realizados foram:
- método prob_spam estava acima de 0.5 para spam 2 teste
- método is_spam resultava True ou False -2 teste
- análise da mensagem retornada quando era ham

### Conclusão
As classificações foram realizados com sucesso e através da GUI criada foi otimizado o tempo para realizar estas.
O Algorítimo de teste executou todos os testes para determinar o tempo de processamento das funções.

## 03-FraudDetection
Neste desafio deve ser criado uma proposta de solução e responder o questionário disponível. Foi disponibilizado as imagens de assinaturas para analisar o dataset
As respostas estão no arquivo markdown disponível na pasta 03-FraudDetection

.
