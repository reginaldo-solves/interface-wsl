# Instalador do Ambiente de Desenvolvimento WSL

Um script Python automatizado com uma interface gráfica moderna em Tkinter que instala o WSL (Subsistema Windows para Linux) e a distribuição Debian no seu sistema Windows.

## Recursos

- ✨ **Interface gráfica moderna** com bordas arredondadas e fontes em negrito
- 🔐 **Coleta segura de credenciais** para configuração de usuários do WSL
- 💾 **Criação automática de arquivo .env** para armazenar credenciais
- ✅ **Verificação de instalação do WSL** - detecta se o WSL já está instalado
- 🐧 **Instalação automatizada do Debian** via PowerShell
- 👤 **Configuração de usuário** - configura automaticamente seu nome de usuário e senha no Debian

## Requisitos

- Windows 10 versão 2004 ou superior (Build 19041 ou superior) ou Windows 11
- Privilégios de administrador
- Python 3.6 ou superior
- Conexão com a internet

## Instalação

1. Certifique-se de que o Python esteja instalado em seu sistema
2. Baixe o arquivo `wsl_installer.py` para o local desejado

## Uso

### Executando o Script

**Importante:** Este script requer privilégios de administrador.

#### Método 1: Executar como Administrador
1. Clique com o botão direito do mouse em Prompt de Comando ou PowerShell
2. Selecione "Executar como administrador"
3. Navegue até o diretório do script:

``bash

cd C:\Users\Reginaldo\Desktop\debian-docker

```
4. Execute o script:

``bash

python wsl_installer.py

```

#### Método 2: Execução Direta (solicitará privilégios de administrador)
1. Clique duas vezes em `wsl_installer.py`
2. Se solicitado, permita o acesso de administrador

### Usando a Interface

1. **Digite o Nome de Usuário**: Digite o nome de usuário Linux desejado
2. **Digite a Senha**: Digite a senha Linux desejada
3. **Clique em "INSTALAR WSL E DEBIAN"**: Inicie o processo de instalação

A interface irá:
- Exibir e ocultar a imagem gradualmente durante o processo de instalação
- Mostrar mensagens de progresso
- Salvar suas credenciais em um arquivo `.env`
- Configurar o Debian automaticamente Suas credenciais

## O que acontece durante a instalação

### Etapa 1: Verificação do WSL
- Verifica se o WSL já está instalado
- Caso não esteja instalado, baixa e instala o WSL
- **Observação:** Se o WSL for uma instalação recente, você precisará reiniciar o computador

### Etapa 2: Instalação do Debian
- Executa o comando do PowerShell para baixar a distribuição Debian
- Instala o Debian como uma distribuição WSL

### Etapa 3: Configuração do usuário
- Cria sua conta de usuário no Debian
- Define sua senha
- Adiciona seu usuário ao grupo sudo
- Configura o Debian para usar sua conta por padrão

### Etapa 4: Salvar credenciais
- Cria um arquivo `.env` no mesmo diretório do script
- Armazena seu nome de usuário e senha para referência

## Arquivos de saída

Após a instalação bem-sucedida, você encontrará:

- `.env` - Contém suas credenciais do WSL:

``

WSL_USERNAME=seu_nome_de_usuário
WSL_PASSWORD=sua_senha

``

## Acessando seu ambiente Debian

Após a instalação, você pode acessar o Debian das seguintes maneiras:

1. Abrindo o Prompt de Comando ou o PowerShell
2. Digitando:

``bash

wsl

```

Ou especificamente para Debian:
```bash
wsl -d Debian
```

## Solução de problemas

### Erro "Administrador necessário"
- Certifique-se de estar executando o script com privilégios de administrador
- Clique com o botão direito do mouse no Prompt de Comando/PowerShell e selecione "Executar como administrador"

### Mensagem "Reinicialização necessária"
- Esta mensagem aparece quando o WSL é instalado pela primeira vez
- Reinicie o computador e execute o script novamente

### Falha na instalação
- Verifique sua conexão com a internet
- Certifique-se de que o Windows esteja atualizado
- Verifique se você tem espaço suficiente em disco (pelo menos 1 GB livre)

## Observações de segurança

- O arquivo `.env` contém suas credenciais em texto simples Texto
- Mantenha este arquivo em segurança e não o compartilhe.
- Considere adicionar `.env` ao seu `.gitignore` se estiver usando controle de versão.

## Design

A interface é inspirada em telas de login modernas com:
- Elementos de design arredondados e com efeito vítreo
- Fontes em negrito e legíveis (Segoe UI)
- Efeitos de foco suaves
- Esquema de cores profissional (#2c3e50, #34495e, #3498db)

## Licença

Uso e modificações gratuitas.