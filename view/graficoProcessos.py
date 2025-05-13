import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk

def centralizar_grafico(fig):
    janela_temporaria = tk.Tk()
    janela_temporaria.withdraw()

    largura_tela = janela_temporaria.winfo_screenwidth()
    altura_tela = janela_temporaria.winfo_screenheight()

    largura_janela = fig.canvas.manager.window.winfo_width()
    altura_janela = fig.canvas.manager.window.winfo_height()

    pos_x = (largura_tela // 2) - int(1.5 * largura_janela)
    pos_y = (altura_tela // 2) - int(1.5 * altura_janela)

    fig.canvas.manager.window.wm_geometry(f"+{pos_x}+{pos_y}")

    janela_temporaria.destroy()

def grafico_processos(processos, media_execucao, media_espera):
    plt.style.use('seaborn-v0_8-whitegrid') # Using a base style for a cleaner look

    fig, ax = plt.subplots(figsize=(10, 6)) # Adjusted figure size
    fig.patch.set_facecolor('#F0F0F0') # Set figure background color
    ax.set_facecolor('#F0F0F0') # Set axes background color
    
    text_color = '#333333'
    font_family = 'Segoe UI' # Attempt to use Segoe UI, matplotlib will fallback if not found

    plt.rcParams['font.family'] = font_family
    plt.rcParams['text.color'] = text_color
    plt.rcParams['axes.labelcolor'] = text_color
    plt.rcParams['xtick.color'] = text_color
    plt.rcParams['ytick.color'] = text_color
    plt.rcParams['axes.titlecolor'] = text_color
    plt.rcParams['axes.edgecolor'] = '#CCCCCC' # Lighter edge color for axes

    fig.canvas.manager.set_window_title('Gráfico de Escalonamento')
    
    if not processos or not any(p.processamentos for p in processos):
        # Handle case with no process data to avoid errors
        ax.text(0.5, 0.5, "Não há dados de processo para exibir.", ha='center', va='center', fontsize=12, color=text_color)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Escalonamento de Processos', fontsize=16, fontweight='bold', color=text_color)
        plt.tight_layout()
        plt.draw()
        centralizar_grafico(fig)
        plt.show()
        return

    tempo_maximo = max([max([p.fim for p in processo.processamentos]) for processo in processos if processo.processamentos]) + 1
    ax.set_xlim(-0.5, tempo_maximo + 2) # Adjusted xlim for text
    ax.set_ylim(0.5, len(processos) + 0.5) # Adjusted ylim based on number of processes

    # Define colors from the theme
    color_execucao = '#4e609c'  # Blue from theme
    color_espera = '#b8b8b8'    # Orange/Red from theme

    for i, processo in enumerate(sorted(processos, key=lambda p: p.id)):
        y_pos = i + 1 # Use index for y position to ensure consistent spacing
        for instante in range(tempo_maximo):
            estado = processo.verificar_estado(instante)

            if estado == "Execução":
                ax.barh(y_pos, 1, left=instante, color=color_execucao, edgecolor=color_execucao, height=0.6)
            elif estado == "Espera":
                ax.barh(y_pos, 1, left=instante, color=color_espera, edgecolor=color_espera, height=0.6)

        espera = processo.get_espera()
        turnaround = processo.get_turnaround()
        # Position text to the right of the bars
        ax.text(tempo_maximo + 0.2, y_pos, f"T: {turnaround}\nE: {espera}", va='center', ha='left', fontsize=9, color=text_color)

    ax.set_yticks([i + 1 for i in range(len(processos))])
    ax.set_yticklabels([f'P{p.id}' for p in sorted(processos, key=lambda p: p.id)], fontsize=10)
    
    ax.set_xlabel('Tempo', fontsize=12, fontweight='bold', color=text_color)
    ax.set_ylabel('Processo ID', fontsize=12, fontweight='bold', color=text_color)
    ax.set_title('Escalonamento de Processos', fontsize=16, fontweight='bold', color=text_color)

    # Customizing grid
    ax.grid(True, linestyle='--', alpha=0.7, color='#CCCCCC')
    ax.set_axisbelow(True) # Ensure grid is behind bars

    execucao_patch = mpatches.Patch(color=color_execucao, label=f'Execução (Média: {media_execucao:.2f} u.t.)')
    espera_patch = mpatches.Patch(color=color_espera, label=f'Espera (Média: {media_espera:.2f} u.t.)')
    
    legend = ax.legend(handles=[execucao_patch, espera_patch], loc='lower center',
                       bbox_to_anchor=(0.5, -0.25), ncol=2, fontsize=10, frameon=True)
    legend.get_frame().set_facecolor('#E0E0E0')
    legend.get_frame().set_edgecolor('#B0B0B0')
    for text in legend.get_texts():
        text.set_color(text_color)


    #fig.canvas.manager.window.wm_iconbitmap("assets/icon.ico")

    plt.tight_layout(rect=[0, 0.05, 1, 0.95]) # Adjust layout to make space for legend
    plt.subplots_adjust(bottom=0.2) # Ensure bottom legend is visible

    plt.draw()
    
    centralizar_grafico(fig)
    plt.show()
