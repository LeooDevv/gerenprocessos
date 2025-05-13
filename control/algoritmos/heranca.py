def heranca(processos):
    """
    Simula o escalonamento com herança de prioridade.
    Regra: Se um processo de alta prioridade precisa de um recurso atualmente
           detido por um processo de baixa prioridade, o processo de baixa
           prioridade herda temporariamente a prioridade do processo de alta.
    """
    if not processos:
        return 0, 0

    tempo_atual = 0
    total_espera = 0
    total_execucao = 0

    # Armazena as prioridades originais para referência
    original_priorities = {p.id: p.prioridade for p in processos}
    
    # Lista de processos que ainda não completaram sua execução
    processos_a_escalonar = list(processos) # Trabalha com a lista de processos fornecida (que já é uma cópia)

    while any(p.tempo_restante > 0 for p in processos_a_escalonar):
        # Filtra processos que já chegaram e ainda precisam executar
        processos_prontos_candidatos = [
            p for p in processos_a_escalonar if p.chegada <= tempo_atual and p.tempo_restante > 0
        ]

        if not processos_prontos_candidatos:
            # Se não há processos prontos, avança o tempo para a próxima chegada relevante
            if any(p.tempo_restante > 0 for p in processos_a_escalonar):
                try:
                    tempo_atual = min(p.chegada for p in processos_a_escalonar if p.tempo_restante > 0 and p.chegada > tempo_atual)
                except ValueError: # Ocorre se todos os restantes já chegaram mas não estão prontos (improvável aqui)
                    break 
                continue
            else: # Todos os processos foram concluídos
                break
        
        # Calcula a prioridade efetiva para cada candidato nesta rodada de decisão
        for p_cand in processos_prontos_candidatos:
            p_cand.effective_priority = original_priorities[p_cand.id] # Começa com a prioridade original
            if p_cand.usa_recurso:
                max_inherited_priority_from_waiter = original_priorities[p_cand.id]
                for p_waiter in processos_prontos_candidatos:
                    # Verifica se p_waiter é diferente, também usa recurso, e tem prioridade original maior
                    if p_waiter.id != p_cand.id and \
                       p_waiter.usa_recurso and \
                       original_priorities[p_waiter.id] > original_priorities[p_cand.id]:
                        
                        if original_priorities[p_waiter.id] > max_inherited_priority_from_waiter:
                            max_inherited_priority_from_waiter = original_priorities[p_waiter.id]
                
                # Atualiza a prioridade efetiva de p_cand se uma maior foi encontrada
                if max_inherited_priority_from_waiter > p_cand.effective_priority:
                    p_cand.effective_priority = max_inherited_priority_from_waiter
        
        # Seleciona o processo para executar
        # Critério primário: maior prioridade efetiva
        # Critério de desempate: menor tempo de chegada (FCFS)
        processos_prontos_candidatos.sort(key=lambda p: p.chegada) # Para desempate FCFS
        processos_prontos_candidatos.sort(key=lambda p: p.effective_priority, reverse=True) # Prioridade efetiva

        processo_atual = processos_prontos_candidatos[0]

        # Simula a execução por uma unidade de tempo
        tempo_consumido = processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)
        tempo_atual += tempo_consumido
                
        if processo_atual.tempo_restante == 0:
            total_espera += processo_atual.get_espera()
            total_execucao += processo_atual.get_turnaround()
            # O processo será filtrado da lista de candidatos na próxima iteração
            # pela condição p.tempo_restante > 0

    # Limpa o atributo temporário, se existir (boa prática)
    for p_obj in processos:
        if hasattr(p_obj, 'effective_priority'):
            del p_obj.effective_priority
            
    if not processos: # Caso a lista original de processos seja vazia
        return 0, 0
        
    media_espera = total_espera / len(processos)
    media_execucao = total_execucao / len(processos)
    
    return media_espera, media_execucao