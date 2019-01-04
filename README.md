# dafitiArt - Case
**********
Conforme proposto por email foi desenvolvido esse software para atender o case
enviado pelo Bernado Plum.

**Na Branch 'develop' como solicitado, removi o .gitignore e commitei tudo, basta dar um checkout e rodar os scripts 
para build do Docker, ou instalar as dependências do requirements.txt e rodar o Django manualmente.**

#Setup 
Caso queira fazer o setup completo, siga o roteiro a baixo com o branch 'master'

Para rodar a aplicação, deve-se copiar o arquivo .env_template para o .env e preencher as variáveis de ambiente de 
segurança do framework.

Para rodar o serviço necessita apenas entrar na pasta docker, buildar a image com o 
script ssh:
```
./build.sh
```
O Script vai buildar uma image docker chamada dafiti-art que deve ser executada com o comando:
```
./run.sh
```
O Docker vai gerenciar todo o ambiente de desenvolvimento e rodar o framework.



Além dos requisitos solicitados foram implementados outras features como o

* Django Rest Framework
* Class Based Views
* Function Based Views
* Modelos não gerenciados
* Controle de váriaveis de ambiente
* ETC.



Alguns extras como o DRF foi implementado apenas em um módulo apenas para a 
demonstração do know how com a biblioteca.