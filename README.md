# PyTranslator

PyTranslator é uma ferramenta poderosa projetada para automatizar a tradução de nomes de arquivos em diretórios especificados para o português, gerenciar a cópia e o renomeamento de arquivos com base nesses nomes traduzidos. Este projeto utiliza a API do Google Translate para as traduções e fornece uma interface de log para facilitar o monitoramento do processo.

## Descrição

Este script Python automatiza o processo de detecção e tradução de idiomas de nomes de arquivos. Se o nome do arquivo não está em português, o script tenta traduzi-lo e gerencia a cópia e o renomeamento de arquivos de maneira eficiente. É equipado com um sistema robusto de log que registra cada etapa do processo, tratando erros e re-tentativas de forma inteligente.

## Como Utilizar

### Pré-requisitos

Para utilizar esta ferramenta, você precisará de Python 3.x instalado em sua máquina, além das bibliotecas necessárias listadas nos arquivos `requirements.txt` e `requirements.dev.txt`.

### Instalação

Clone o repositório para a sua máquina local e instale as dependências necessárias:

```bash
pip3 install -r requirements.txt
pip3 install -r requirements.dev.txt
```

### Execução

Após instalar as dependências, você pode executar o script da seguinte forma:

```bash
python __main__.py --input=caminho_para_o_diretório_de_entrada --output=caminho_para_o_diretório_de_saída
```

Você pode omitir --input e --output se desejar utilizar os diretórios padrão (./input e ./output).

### Exemplos

```bash
python __main__.py --input=./minha_pasta --output=./pasta_destino
```

Este comando processará todos os arquivos em ./minha_pasta, traduzindo os nomes para português e os copiando para ./pasta_destino.

##### Made with ❤️ by fagundesjg

Se você encontrar este projeto útil, considere dar uma estrela no GitHub!
