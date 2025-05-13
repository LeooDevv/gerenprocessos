import copy
import tkinter as tk
from tkinter import messagebox

from control import simular_escalonamento
from model import Processo
from view import grafico_processos

processos = []

def adicionar_processo():
    try:
        chegada = int(entrada_chegada.get())
        duracao = int(entrada_duracao.get())
        prioridade = int(entrada_prioridade.get())
        # Get the boolean value from the Tkinter variable
        usa_recurso = flag_heranca.get()

        if not (0 <= prioridade <= 10):
            raise ValueError("Prioridade deve estar entre 0 e 10")

        novo_id = max(processo.id for processo in processos) + 1 if processos else 1

        processo = Processo(novo_id, chegada, duracao, prioridade, usa_recurso)
        processos.append(processo)

        lista_processos.insert(tk.END, f"ID: {novo_id}, Chegada: {chegada}, Duração: {duracao}, Prioridade: {prioridade}, Usa Recurso: {usa_recurso}")

        
        entrada_chegada.delete(0, tk.END)
        entrada_duracao.delete(0, tk.END)
        entrada_prioridade.delete(0, tk.END)
        # entrada_heranca widget does not exist, and valor_entrada was its .get()
    
    except ValueError as e:
        messagebox.showerror("Erro", f"Entrada inválida: {e}")

def remover_processo():
    if len(lista_processos.curselection()):
        index_selecionado = lista_processos.curselection()[0]
        lista_processos.delete(index_selecionado)

        processo_selecionado = processos[index_selecionado]
        processos.remove(processo_selecionado)
    elif processos:
        processos.pop()
        lista_processos.delete(lista_processos.size() - 1)

def form_submit():
    try:
        processos_submit = copy.deepcopy(processos)
        algoritmo = algoritmo_var.get()
        quantum = quantum_entry.get()

        media_execucao, media_espera = simular_escalonamento(processos_submit, algoritmo, quantum)

        grafico_processos(processos_submit, media_execucao, media_espera)
    except Exception as e:
        messagebox.showerror("Erro", e)

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    janela.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')

def habilitar_quantum():
    if algoritmo_var.get() == 3:
        quantum_label.pack(padx=20, pady=2) # Reduced pady
        quantum_entry.pack(padx=20, pady=2) # Reduced pady
    else:
        quantum_label.pack_forget()
        quantum_entry.pack_forget()

def criar_janela():
    global entrada_chegada, entrada_duracao, entrada_prioridade, lista_processos, algoritmo_var, quantum_label, quantum_entry, flag_heranca
    
    janela = tk.Tk()
    janela.title("Simulador de Escalonamento")
    #janela.iconbitmap("assets/icon.ico")
    janela.configure(bg="#F0F0F0")
    janela.resizable(False, False)

    centralizar_janela(janela, 800, 700)

    algoritmo_var = tk.IntVar()
    flag_heranca = tk.BooleanVar(value=False)

    processos_label = tk.Label(janela, text="Defina os Processos",
                    font=("Segoe UI", 18, "bold"), # Slightly smaller font
                    fg="#333333",
                    bg="#F0F0F0")
    processos_label.pack(pady=(10,5)) # Reduced padding


    input_form_frame = tk.Frame(janela, bg="#F0F0F0")
    input_form_frame.pack(pady=5, padx=20, fill="x") # Reduced pady

    # Input field styling
    label_font = ("Segoe UI", 11) # Slightly smaller font
    entry_font = ("Segoe UI", 11) # Slightly smaller font
    entry_config = {"bd": 1, "relief": tk.SOLID, "highlightthickness": 1, "highlightbackground": "#CCCCCC", "highlightcolor": "#4e609c", "font": entry_font, "justify": "center", "width": 15}
    label_config = {"font": label_font, "bg": "#F0F0F0", "fg": "#333333"}


    tk.Label(input_form_frame, text="Chegada:", **label_config).grid(row=0, column=0, padx=10, pady=(5,2), sticky="w") # Reduced pady
    entrada_chegada = tk.Entry(input_form_frame, **entry_config)
    entrada_chegada.grid(row=1, column=0, padx=10, pady=2) # Reduced pady

    tk.Label(input_form_frame, text="Duração:", **label_config).grid(row=0, column=1, padx=10, pady=(5,2), sticky="w") # Reduced pady
    entrada_duracao = tk.Entry(input_form_frame, **entry_config)
    entrada_duracao.grid(row=1, column=1, padx=10, pady=2) # Reduced pady

    tk.Label(input_form_frame, text="Prioridade (0-10):", **label_config).grid(row=0, column=2, padx=10, pady=(5,2), sticky="w")
    entrada_prioridade = tk.Entry(input_form_frame, **entry_config)
    entrada_prioridade.grid(row=1, column=2, padx=10, pady=2)

    # Label for resource usage radio buttons
    tk.Label(input_form_frame, text="Uso de Recurso:", **label_config).grid(row=0, column=3, padx=10, pady=(5,2), sticky="w") # Moved to row 0, column 3
    
    # Radio buttons for resource usage
    radio_recurso_frame = tk.Frame(input_form_frame, bg="#F0F0F0")
    radio_recurso_frame.grid(row=1, column=3, padx=10, pady=2, sticky="w") # Moved to row 1, column 3, removed columnspan

    radio_button_config = {"font": ("Segoe UI", 10), "fg": "#333333", "bg": "#F0F0F0", "activebackground": "#F0F0F0", "activeforeground": "#4e609c", "selectcolor": "#E0E0E0"}
    tk.Radiobutton(radio_recurso_frame, text="Sim", variable=flag_heranca, value=True, **radio_button_config).pack(side=tk.LEFT, padx=(0,5)) # Reduced padx
    tk.Radiobutton(radio_recurso_frame, text="Não", variable=flag_heranca, value=False, **radio_button_config).pack(side=tk.LEFT)


    buttons_form_frame = tk.Frame(janela, bg="#F0F0F0")
    buttons_form_frame.pack(pady=8) # Reduced pady

    button_font = ("Segoe UI", 11, "bold") # Slightly smaller font
    add_button_config = {"font": button_font, "fg": "#FFFFFF", "bg": "#4e609c", "activeforeground": "#FFFFFF", "activebackground": "#005A9E", "relief": tk.FLAT, "padx": 8, "pady": 3} # Reduced padding
    remove_button_config = {"font": button_font, "fg": "#FFFFFF", "bg": "#4e609c", "activeforeground": "#FFFFFF", "activebackground": "#A82F00", "relief": tk.FLAT, "padx": 8, "pady": 3} # Reduced padding, bg changed

    tk.Button(buttons_form_frame, text="Adicionar Processo", command=adicionar_processo, **add_button_config).grid(row=0, column=0, padx=10)
    tk.Button(buttons_form_frame, text="Remover Processo", command=remover_processo, **remove_button_config).grid(row=0, column=1, padx=10)

    lista_processos = tk.Listbox(janela, width=60, height=5, bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground="#CCCCCC", highlightcolor="#4e609c", font=("Segoe UI", 10), justify="center", bg="#FFFFFF", fg="#333333", selectbackground="#4e609c", selectforeground="#FFFFFF") # Reduced height and font
    lista_processos.pack(padx=20, pady=5, fill="x") # Reduced pady


    algoritmo_label = tk.Label(janela, text="Escolha o Algoritmo de Escalonamento",
                    font=("Segoe UI", 18, "bold"), # Slightly smaller font
                    fg="#333333",
                    bg="#F0F0F0")
    algoritmo_label.pack(pady=(10,5)) # Reduced padding

    # Algorithm Selection Group
    algoritmo_group = tk.LabelFrame(janela, text="Algoritmos de Escalonamento", font=("Segoe UI", 12, "bold"), fg="#333333", bg="#F0F0F0", padx=10, pady=5, bd=1, relief=tk.SOLID) # Reduced font, padx, pady
    algoritmo_group.pack(pady=5, padx=20, fill="x") # Reduced pady


    algo_radio_config = {"font": ("Segoe UI", 10), "fg": "#333333", "bg": "#F0F0F0", "activebackground": "#F0F0F0", "activeforeground": "#4e609c", "selectcolor": "#E0E0E0", "anchor": "w"} # Slightly smaller font

    # Radio buttons within the LabelFrame
    tk.Radiobutton(algoritmo_group, text="1. FCFS (First-Come, First-Served)", variable=algoritmo_var, value=1, command=habilitar_quantum, **algo_radio_config).grid(row=0, column=0, padx=10, pady=2, sticky="w") # Reduced pady
    tk.Radiobutton(algoritmo_group, text="2. SJF (Shortest Job First)", variable=algoritmo_var, value=2, command=habilitar_quantum, **algo_radio_config).grid(row=1, column=0, padx=10, pady=2, sticky="w") # Reduced pady
    tk.Radiobutton(algoritmo_group, text="3. Round Robin", variable=algoritmo_var, value=3, command=habilitar_quantum, **algo_radio_config).grid(row=2, column=0, padx=10, pady=2, sticky="w") # Reduced pady
    tk.Radiobutton(algoritmo_group, text="4. SRTF (Shortest Remaining Time First)", variable=algoritmo_var, value=4, command=habilitar_quantum, **algo_radio_config).grid(row=0, column=1, padx=10, pady=2, sticky="w") # Reduced pady
    tk.Radiobutton(algoritmo_group, text="5. Prioridade Cooperativo", variable=algoritmo_var, value=5, command=habilitar_quantum, **algo_radio_config).grid(row=1, column=1, padx=10, pady=2, sticky="w") # Reduced pady
    tk.Radiobutton(algoritmo_group, text="6. Prioridade Preemptivo", variable=algoritmo_var, value=6, command=habilitar_quantum, **algo_radio_config).grid(row=2, column=1, padx=10, pady=2, sticky="w") # Reduced pady
    tk.Radiobutton(algoritmo_group, text="7. Herança de Prioridade", variable=algoritmo_var, value=7, command=habilitar_quantum, **algo_radio_config).grid(row=3, column=0, padx=10, pady=2, sticky="w")  # Reduced pady
    tk.Radiobutton(algoritmo_group, text="8. Inversão de Prioridade", variable=algoritmo_var, value=8, command=habilitar_quantum, **algo_radio_config).grid(row=3, column=1, padx=10, pady=2, sticky="w") # Reduced pady
    
    # Configure column weights for better spacing in the LabelFrame
    algoritmo_group.grid_columnconfigure(0, weight=1)
    algoritmo_group.grid_columnconfigure(1, weight=1)


    quantum_label = tk.Label(janela, text="Informe o quantum para Round Robin:", font=("Segoe UI", 11), fg="#333333", bg="#F0F0F0") # Slightly smaller font
    quantum_entry_config = entry_config.copy()
    quantum_entry_config["width"] = 8
    quantum_entry_config["font"] = ("Segoe UI", 11) # Matched font
    quantum_entry = tk.Entry(janela, **quantum_entry_config)
    quantum_entry.insert(0, "2")

    # Simular button styling and placement
    simular_button_frame = tk.Frame(janela, bg="#F0F0F0")
    simular_button_frame.pack(pady=(10,15), fill="x", padx=20) # Reduced pady
    
    simular_button_config = {"font": ("Segoe UI", 14, "bold"), "fg": "#FFFFFF", "bg": "#28A745", "activeforeground": "#FFFFFF", "activebackground": "#218838", "relief": tk.FLAT, "pady": 5} # Reduced pady, removed height/width
    tk.Button(simular_button_frame, text="Simular Escalonamento", command=form_submit, **simular_button_config).pack(expand=True, fill="x", ipady=5) # Added ipady for internal padding

    janela.mainloop()


