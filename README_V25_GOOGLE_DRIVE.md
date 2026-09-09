# AH TECH Gestão Premium V25 — Google Drive Cloud

A V25 usa a conta Google para autenticação e o Google Drive como armazenamento central dos dados e imagens.

## O que é sincronizado
- vendas
- produtos e estoque
- clientes
- ordens de serviço
- gastos fixos e variáveis
- contas a receber
- agenda
- metas
- relatórios e configurações
- logo e imagens de produtos
- backups JSON

## Estrutura criada no Drive
AH TECH GESTÃO CLOUD/
- ahtech-data.json
- Mídia/
- backups-AAAA-MM-DD.json

## Configuração obrigatória
Edite `google-drive-config.js` e informe o OAuth Client ID criado no Google Cloud.

No Google Cloud:
1. Crie um projeto.
2. Ative Google Drive API.
3. Configure a tela de consentimento OAuth.
4. Crie OAuth Client ID para aplicativo Web.
5. Cadastre a URL HTTPS onde o sistema será publicado em Origens JavaScript autorizadas.
6. Coloque o Client ID em `google-drive-config.js`.

## Publicação
Google Drive não é um servidor de páginas web. O HTML precisa ser publicado em um endereço HTTPS, por exemplo:
- GitHub Pages
- Cloudflare Pages
- Netlify
- Vercel
- hospedagem própria

Depois, em qualquer computador, abra a mesma URL e clique em `Entrar com Google Drive`, usando a mesma conta Google.

## Segurança
- O sistema não armazena a senha Google.
- A autorização usa Google Identity Services/OAuth.
- O escopo utilizado é `drive.file`, limitado aos arquivos criados pelo aplicativo.
- O PostgreSQL/VPS não é necessário para esta modalidade.
- Não coloque credenciais privadas no HTML.

## Observação sobre concorrência
A V25 verifica a revisão do arquivo antes de gravar. Se outro computador salvar primeiro, o sistema carrega os dados mais recentes e solicita uma nova gravação, evitando sobrescrita silenciosa.

## Imagens
As imagens são convertidas em arquivos individuais dentro da pasta `Mídia`. O estado do sistema guarda referências `gdrive://ID`. Ao abrir em outro computador, o sistema baixa as imagens autorizadas e cria URLs temporárias para a interface.


## V25.3
A tela de login agora mostra a mensagem técnica retornada pela Google Drive API, em vez de esconder a causa atrás do erro genérico. Também orienta a verificar se a Google Drive API está habilitada no projeto.


## V25.3 — correção do acesso ao banco

Esta versão usa o escopo OAuth `https://www.googleapis.com/auth/drive` porque o sistema precisa localizar e ler a pasta/banco AH TECH já existente no Google Drive, inclusive quando esses arquivos foram criados por uma versão anterior do sistema. O Google documenta que `drive.file` é limitado aos arquivos criados ou abertos pelo aplicativo, enquanto `drive` permite acesso aos arquivos do Drive conforme a autorização concedida.

Após publicar a V25.3, faça login novamente e aceite a nova permissão do Google Drive. Se o navegador mantiver a autorização antiga, remova o acesso do aplicativo nas configurações da Conta Google e entre novamente.
