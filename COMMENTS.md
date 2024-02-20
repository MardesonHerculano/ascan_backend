# Comments

Espaço para documentar a evolução, problemas e ideias que surgiram conforme o desafio foi sendo feito

#### Utilização do SQLITE
```
feature/add-sqlite
```
Nessa branch configurei e instalei o sqlite com um banco de testes e dois endpoints: `/write` e `/read`
Para ver como a integração iria funcionar, escrevendo e exibindo dados simples de um banco `user` que, recebendo o `full_name` registra o `id` como PRIMARY KEY e o, `created_at` como um timestamp.
Esse é um dos bancos do desafio, então já servirá como base para o restante.