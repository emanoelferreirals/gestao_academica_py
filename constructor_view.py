import tkinter as tk
from tkinter import ttk

def construtor_main(frame, elementos):
    widgets = {}
    imagens = {}  # Armazena imagens para evitar garbage collector
    
    style = ttk.Style()
    
    for key, props in elementos.items():
        props = props.copy()  # Copia para evitar modificar o original
        widget_class = props.pop('widget')  # Remove e obtém a classe do widget
        
        # Separa argumentos do grid e argumentos do widget
        grid_args = {k: props.pop(k) for k in ['row', 'column', 'columnspan', 'padx', 'pady', 'sticky'] if k in props}
        
        # Configuração especial para labels com imagem
        if 'image' in props:
            imagens[key] = tk.PhotoImage(file=props['image'])
            props['image'] = imagens[key]
        
        # Configuração para cores
        if 'background' in props or 'foreground' in props:
            style_name = f"{key}.T{widget_class.__name__}"
            style.configure(style_name, background=props.pop('background', None), foreground=props.pop('foreground', None))
            props['style'] = style_name
        
        # Tratamento especial para ttk.Combobox e OptionMenu
        if widget_class in [ttk.Combobox, tk.OptionMenu] and 'values' in props:
            var = tk.StringVar()
            props['textvariable'] = var
            if 'default' in props:
                var.set(props.pop('default'))
        
        # Cria o widget com os argumentos restantes
        widget = widget_class(frame, **props)
        
        # Aplica o grid layout
        widget.grid(
            row=grid_args.get('row', 0),
            column=grid_args.get('column', 0),
            columnspan=grid_args.get('columnspan', 1),
            padx=grid_args.get('padx', 5),
            pady=grid_args.get('pady', 5),
            sticky=grid_args.get('sticky', "w")
        )
        
        # Salva o widget criado
        widgets[key] = widget
    
    return widgets