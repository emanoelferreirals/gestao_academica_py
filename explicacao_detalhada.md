
# Explicação Detalhada do Código

Este documento contém a explicação detalhada, linha a linha, das funções presentes no código fornecido. As funções estão envolvidas principalmente em interações com a interface gráfica (GUI), manipulação de dados em JSON e gerenciamento de uma tabela de notas.

---

## Função `carregar_dados`

Esta função é responsável por carregar os dados salvos em um arquivo JSON. Se o arquivo não existir ou estiver corrompido, ela retorna uma lista vazia.

```python
def carregar_dados():
    if os.path.exists(arquivo_dados):  # Verifica se o arquivo de dados existe
        with open(arquivo_dados, "r") as f:  # Abre o arquivo para leitura
            try:
                return json.load(f)  # Tenta carregar os dados no formato JSON
            except json.JSONDecodeError:  # Se ocorrer um erro ao tentar ler o JSON
                return []  # Retorna uma lista vazia caso o JSON seja inválido
    return []  # Retorna uma lista vazia caso o arquivo não exista
```

**Explicação linha a linha:**
1. `if os.path.exists(arquivo_dados):` - Verifica se o arquivo especificado pela variável `arquivo_dados` existe no sistema.
2. `with open(arquivo_dados, "r") as f:` - Abre o arquivo no modo de leitura.
3. `return json.load(f)` - Tenta carregar o conteúdo do arquivo JSON para uma estrutura de dados Python.
4. `except json.JSONDecodeError:` - Captura o erro se o arquivo JSON estiver mal formatado.
5. `return []` - Retorna uma lista vazia se o arquivo JSON for inválido ou se ocorrer algum erro na leitura.
6. `return []` - Retorna uma lista vazia caso o arquivo não exista.

---

## Função `salvar_dados`

Esta função é responsável por salvar os dados da tabela no arquivo JSON. Ela coleta os dados da interface gráfica, organiza e escreve no arquivo.

```python
def salvar_dados():
    novos_dados = []  # Cria uma lista vazia para armazenar os dados que serão salvos
    for row in range(1, len(frame_tabela.grid_slaves()) // len(titulos) + 1):  # Percorre as linhas da tabela
        linha = []  # Cria uma lista para armazenar os dados de uma linha
        for col in range(len(titulos)):  # Percorre as colunas da tabela
            widget = frame_tabela.grid_slaves(row=row, column=col)  # Acessa o widget da célula
            if widget:  # Se o widget da célula não estiver vazio
                linha.append(widget[0].get())  # Obtém o valor do widget e adiciona na lista
        if linha:  # Se a linha não estiver vazia
            novos_dados.append(linha)  # Adiciona a linha de dados à lista de novos dados
    novos_dados.sort(key=lambda x: int(x[1]) if x[1].isdigit() else 0)  # Ordena os dados pela segunda coluna (presumivelmente um valor numérico)
    with open(arquivo_dados, "w") as f:  # Abre o arquivo para escrita
        json.dump(novos_dados, f, indent=4)  # Salva os dados no arquivo com indentação de 4 espaços
    atualizar_tabela(novos_dados)  # Atualiza a tabela com os novos dados
    btn_salvar.grid_remove()  # Remove o botão de salvar após a ação
```

**Explicação linha a linha:**
1. `novos_dados = []` - Cria uma lista vazia para armazenar os dados que serão salvos.
2. `for row in range(1, len(frame_tabela.grid_slaves()) // len(titulos) + 1):` - Itera sobre as linhas da tabela (começando da linha 1).
3. `linha = []` - Cria uma lista vazia para armazenar os dados de cada linha da tabela.
4. `for col in range(len(titulos)):` - Itera sobre as colunas da tabela.
5. `widget = frame_tabela.grid_slaves(row=row, column=col)` - Obtém o widget da célula na linha `row` e coluna `col`.
6. `if widget:` - Verifica se a célula não está vazia.
7. `linha.append(widget[0].get())` - Adiciona o valor da célula à lista `linha`.
8. `if linha:` - Verifica se a linha não está vazia.
9. `novos_dados.append(linha)` - Adiciona a linha preenchida à lista `novos_dados`.
10. `novos_dados.sort(key=lambda x: int(x[1]) if x[1].isdigit() else 0)` - Ordena os dados pela segunda coluna, assumindo que é numérica.
11. `with open(arquivo_dados, "w") as f:` - Abre o arquivo para escrita.
12. `json.dump(novos_dados, f, indent=4)` - Grava os dados no arquivo no formato JSON com indentação de 4 espaços.
13. `atualizar_tabela(novos_dados)` - Atualiza a tabela com os novos dados.
14. `btn_salvar.grid_remove()` - Remove o botão de salvar da tela.

---

## Função `detectar_mudanca`

Essa função é chamada sempre que um campo de entrada (como uma combobox ou entry) é alterado, para exibir o botão de salvar.

```python
def detectar_mudanca(event):
    btn_salvar.grid(row=3, column=0, pady=10)  # Exibe o botão de salvar ao detectar uma mudança em qualquer campo
```

**Explicação linha a linha:**
1. `btn_salvar.grid(row=3, column=0, pady=10)` - Exibe o botão de salvar na posição especificada (linha 3, coluna 0) com um espaço de 10 pixels de padding vertical.

---

## Função `adicionar_linha`

Essa função adiciona uma nova linha na tabela, criando novos campos de entrada (comboboxes e entries) para que o usuário preencha os dados.

```python
def adicionar_linha():
    row = len(frame_tabela.grid_slaves()) // len(titulos) + 1  # Calcula a próxima linha disponível
    criar_linha(row)  # Cria a nova linha na tabela
    btn_salvar.grid(row=3, column=0, pady=10)  # Exibe o botão de salvar
```

**Explicação linha a linha:**
1. `row = len(frame_tabela.grid_slaves()) // len(titulos) + 1` - Calcula a próxima linha disponível na tabela.
2. `criar_linha(row)` - Chama a função `criar_linha` para adicionar uma nova linha na tabela.
3. `btn_salvar.grid(row=3, column=0, pady=10)` - Exibe o botão de salvar.

---

## Função `criar_linha`

Essa função cria os widgets (comboboxes e entries) para cada célula de uma linha na tabela.

```python
def criar_linha(row, valores=None):
    cmb_materia = ttk.Combobox(frame_tabela, values=materias, state="readonly", width=15)  # Cria o combobox para matérias
    cmb_materia.grid(row=row, column=0, padx=5, pady=5)  # Posiciona o combobox na tabela
    cmb_materia.bind("<<ComboboxSelected>>", detectar_mudanca)  # Detecta mudanças na seleção da matéria
    
    cmb_periodo = ttk.Combobox(frame_tabela, values=semestres, state="readonly", width=10)  # Cria o combobox para períodos
    cmb_periodo.grid(row=row, column=1, padx=5, pady=5)  # Posiciona o combobox na tabela
    cmb_periodo.bind("<<ComboboxSelected>>", detectar_mudanca)  # Detecta mudanças na seleção do período
    
    if valores:  # Se valores forem passados, preenche os campos com esses valores
        cmb_materia.set(valores[0])  # Define a matéria selecionada
        cmb_periodo.set(valores[1])  # Define o período selecionado
    
    for col in range(2, 6):  # Cria os campos de notas (n1, n2, n3, n4)
        entry = ttk.Entry(frame_tabela, width=5)  # Cria um campo de entrada para a nota
        entry.grid(row=row, column=col, padx=5, pady=5)  # Posiciona o campo na tabela
        entry.bind("<KeyRelease>", detectar_mudanca)  # Detecta quando uma tecla for pressionada
        if valores:  # Se houver valores passados, insere-os nos campos
            entry.insert(0, valores[col])  # Insere o valor nos campos de nota
```

**Explicação linha a linha:**
1. `cmb_materia = ttk.Combobox(...)` - Cria um combobox para selecionar a matéria, com uma lista de matérias.
2. `cmb_materia.grid(...)` - Posiciona o combobox na tabela.
3. `cmb_materia.bind("<<ComboboxSelected>>", detectar_mudanca)` - Detecta mudanças na seleção da matéria e chama `detectar_mudanca`.
4. `cmb_periodo = ttk.Combobox(...)` - Cria um combobox para selecionar o período (semestre).
5. `cmb_periodo.grid(...)` - Posiciona o combobox para o período na tabela.
6. `cmb_periodo.bind(...)` - Detecta mudanças na seleção do período.
7. `if valores:` - Se a função for chamada com valores específicos, preenche os campos com esses valores.
8. `for col in range(2, 6):` - Cria os campos de entrada para as notas (n1, n2, n3, n4).

---
