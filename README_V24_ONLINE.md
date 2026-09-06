# AH TECH Gestão Premium V24 — Online

## Objetivo
Esta versão transforma o armazenamento central em uma arquitetura web com **FastAPI + PostgreSQL**, sessão autenticada e armazenamento central de imagens. Dois computadores em redes diferentes acessam a mesma URL pela Internet.

## O que fica centralizado
- vendas e itens
- ordens de serviço
- estoque/produtos
- clientes
- gastos fixos e variáveis
- contas a receber
- agenda
- metas e relatórios
- personalização
- logo do sistema/login
- imagens dos produtos
- histórico de sincronização

As imagens enviadas em `data:image/...` são extraídas automaticamente para a tabela `media` do PostgreSQL e o estado passa a guardar uma URL `/api/media/<id>`. Isso evita inflar o JSON com base64 repetido.

## Arquitetura
`Navegador Casa/Loja -> HTTPS -> FastAPI -> PostgreSQL`

O frontend e a API são servidos pelo mesmo processo, evitando CORS desnecessário e permitindo cookie de sessão HttpOnly.

## Requisito para funcionar fora da rede local
O pacote é **cloud-ready**, mas você precisa publicar o servidor em um VPS/cloud ou serviço compatível com Docker. Não é seguro expor diretamente a porta do banco PostgreSQL.

### Opção recomendada
1. Contrate um VPS pequeno (Linux/Docker).
2. Aponte um domínio, por exemplo `gestao.seudominio.com.br`, para o VPS.
3. Coloque HTTPS na frente do container (Caddy, Nginx Proxy Manager ou proxy da Cloudflare).
4. Suba `docker compose up -d --build`.
5. Configure `.env` com senhas fortes.
6. Acesse a mesma URL em casa e na loja.

## Teste local
1. Copie `.env.example` para `.env` e troque as senhas.
2. Execute `docker compose up -d --build`.
3. Abra `http://IP-DO-SERVIDOR:8080`.
4. Entre com `AHTECH_ADMIN_EMAIL` e `AHTECH_ADMIN_PASSWORD`.

Para produção com HTTPS, altere `AHTECH_COOKIE_SECURE=0`.

## Migração da V23
Copie a pasta `database/` da V23 para dentro desta pasta e execute `MIGRAR_V23_PARA_ONLINE.py`. Ele lê o `database/ahtech.db`, autentica no servidor online e envia o estado para o PostgreSQL.

## Conflitos
O servidor mantém uma revisão monotônica. Se o PC A e o PC B tentarem salvar versões diferentes do mesmo estado, o segundo recebe `409 revision_conflict` e carrega o estado mais recente, evitando sobrescrita silenciosa.

## Backups
Use o botão de backup do sistema para exportar um backup lógico do estado. Para produção, configure também backup automático do PostgreSQL no provedor/VPS.

## Segurança
- PostgreSQL não deve ser publicado na Internet.
- Use HTTPS.
- Use senha forte para banco, administrador e chave de sessão.
- Faça backup automático.
- Não compartilhe a conta de administrador.
- O endpoint de imagens usa UUIDs aleatórios e cache imutável; as imagens não são listadas publicamente.

## Produção com HTTPS
Use `docker-compose.prod.yml` + `Caddyfile`. No DNS, aponte o domínio para o IP público do VPS e preencha `DOMAIN` no `.env`. O Caddy termina TLS e encaminha para a aplicação; o PostgreSQL permanece isolado na rede Docker.

## Alternativa sem abrir portas
Você pode colocar a aplicação atrás de um túnel privado/seguro (por exemplo, Cloudflare Tunnel ou VPN como Tailscale). O princípio continua o mesmo: casa e loja acessam a mesma URL segura, e a porta do PostgreSQL não fica exposta.
