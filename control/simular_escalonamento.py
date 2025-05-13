from control import fcfs, sjf, round_robin, srtf, prioridade_cooperativo, prioridade_preemptivo, heranca, inversao

def simular_escalonamento(processos, algoritmo, quantum_entry=0):
    if not processos:
        raise Exception("Nenhum processo foi adicionado.")

    if algoritmo == 1:
        media_espera, media_execucao = fcfs(processos)
    elif algoritmo == 2:
        media_espera, media_execucao = sjf(processos)
    elif algoritmo == 3:
        quantum = int(quantum_entry)
        media_espera, media_execucao = round_robin(processos, quantum)
    elif algoritmo == 4:
        media_espera, media_execucao = srtf(processos)
    elif algoritmo == 5:
        media_espera, media_execucao = prioridade_cooperativo(processos)
    elif algoritmo == 6:
        media_espera, media_execucao = prioridade_preemptivo(processos)
    elif algoritmo == 7:
        media_espera, media_execucao = heranca(processos) # Call the new heranca algorithm
    elif algoritmo == 8:
        media_espera, media_execucao = inversao(processos)
    else:
        raise Exception("Selecione um algoritmo válido.")
    
    return media_execucao, media_espera
       
    
