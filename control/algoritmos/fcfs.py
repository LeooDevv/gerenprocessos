def fcfs(processos):
    tempo_atual = 0
    total_execucao = 0
    total_espera = 0

    processos_ordenados = sorted(processos, key=lambda p: p.chegada)
    
    for processo in processos_ordenados:
        if processo.chegada > tempo_atual:
            tempo_atual = processo.chegada
            
        tempo_atual += processo.adicionar_processamento(tempo_atual, tempo_atual + processo.duracao)
        
        total_execucao += processo.get_turnaround()
        total_espera += processo.get_espera()
        
    media_espera = total_espera / len(processos)
    media_execucao = total_execucao / len(processos)
    
    return media_espera, media_execucao
