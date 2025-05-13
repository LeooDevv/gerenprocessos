def inversao(processos_param):
    if not processos_param:
        return 0, 0

    tempo_atual = 0
    processo_detentor_recurso = None
    
    for p in processos_param:
        p.primeira_execucao_concedida = False
        p.tentativas_bloqueadas_ts = []
        p.foi_bloqueado_na_primeira_exec_garantida = False # Reset this new flag

    while any(p.tempo_restante > 0 for p in processos_param):
        processos_candidatos = [
            p for p in processos_param 
            if p.chegada <= tempo_atual and p.tempo_restante > 0
        ]

        if not processos_candidatos:
            min_proxima_chegada = float('inf')
            found_pending_arrival = False
            for p in processos_param:
                if p.tempo_restante > 0 and p.chegada > tempo_atual:
                    min_proxima_chegada = min(min_proxima_chegada, p.chegada)
                    found_pending_arrival = True
            
            if found_pending_arrival:
                tempo_atual = min_proxima_chegada
            else:
                break 
            continue

        processos_candidatos.sort(key=lambda p: (-p.prioridade, p.chegada))
        
        cmpg = processos_candidatos[0] # candidato_mais_prioritario_geral
        
        if not cmpg.primeira_execucao_concedida:
            processo_a_executar = cmpg
            special_first_run_block_applies = False

            if cmpg.duracao == 1 and cmpg.usa_recurso:
                # Check if it *would be* blocked if this wasn't a guaranteed run
                if processo_detentor_recurso and \
                   processo_detentor_recurso != cmpg and \
                   processo_detentor_recurso.tempo_restante > 0:
                    # It would be blocked. Mark it for special handling.
                    cmpg.foi_bloqueado_na_primeira_exec_garantida = True
                    special_first_run_block_applies = True
                    # Also log this "attempt" as per previous logic, even if it runs
                    cmpg.registrar_tentativa_bloqueada(tempo_atual)


            # Execute its guaranteed first run
            processo_a_executar.adicionar_processamento(
                tempo_atual, 
                tempo_atual + 1, 
                is_handling_special_first_run_block=special_first_run_block_applies
            )
            processo_a_executar.primeira_execucao_concedida = True
            
            # Resource acquisition logic for the first run
            if processo_a_executar.usa_recurso:
                # If it uses a resource, it attempts to become the holder.
                # If another process was holding it, this implies the resource was yielded or
                # this is the higher priority process taking over (if rules allowed).
                # For the guaranteed first run, if it uses a resource, it gets it if free.
                # If special_first_run_block_applies was true, it means it *would* have been blocked,
                # but the guarantee lets it run. It still "holds" the resource conceptually for this 1 tick.
                if not processo_detentor_recurso or \
                   processo_detentor_recurso.tempo_restante == 0 or \
                   processo_detentor_recurso == processo_a_executar: # It can take/reaffirm resource
                    processo_detentor_recurso = processo_a_executar
            
            tempo_atual += 1
            if processo_detentor_recurso and processo_detentor_recurso.tempo_restante == 0:
                processo_detentor_recurso = None
            continue # Re-evaluate for the next time slice

        # Normal logic (after first guaranteed run)
        processo_a_executar = cmpg 

        if cmpg.usa_recurso:
            # If CMPG was previously marked as D=1, R=true, and blocked on its first guaranteed run,
            # it means its tempo_restante is still 1. It now needs the resource legitimately.
            is_special_case_retrying = cmpg.duracao == 1 and \
                                       cmpg.usa_recurso and \
                                       cmpg.foi_bloqueado_na_primeira_exec_garantida and \
                                       cmpg.tempo_restante == 1


            if processo_detentor_recurso and \
               processo_detentor_recurso != cmpg and \
               processo_detentor_recurso.tempo_restante > 0:
                
                # This is a genuine block or attempt after the first guaranteed run
                # (or for processes with D > 1 on their first attempt if they need a resource)
                if not is_special_case_retrying: # Don't double-log if it's the D=1 special retry
                    cmpg.registrar_tentativa_bloqueada(tempo_atual)
                
                processos_elegiveis_para_rodar_neste_turno = []
                if processo_detentor_recurso in processos_candidatos:
                    processos_elegiveis_para_rodar_neste_turno.append(processo_detentor_recurso)

                for p_cand in processos_candidatos:
                    if not p_cand.usa_recurso and \
                       p_cand.prioridade > processo_detentor_recurso.prioridade and \
                       p_cand != cmpg:
                        processos_elegiveis_para_rodar_neste_turno.append(p_cand)
                
                if processos_elegiveis_para_rodar_neste_turno:
                    processos_elegiveis_para_rodar_neste_turno.sort(key=lambda p: (-p.prioridade, p.chegada))
                    processo_a_executar = processos_elegiveis_para_rodar_neste_turno[0]
                # else: CMPG remains 'processo_a_executar' but is blocked.
                # The 'adicionar_processamento' call below will handle it.
                # If CMPG is blocked and no B or C can run, CMPG (as processo_a_executar)
                # will effectively "not run" if its 'adicionar_processamento' results in 0 time.
                # However, if it's the special D=1 case retrying, it *should* run now if resource is free.

            # If CMPG is the special D=1 case retrying, and the resource is now free or held by itself
            elif is_special_case_retrying and \
                 (not processo_detentor_recurso or processo_detentor_recurso == cmpg or processo_detentor_recurso.tempo_restante == 0):
                processo_a_executar = cmpg # It can now run its "second" part
                # It will acquire the resource below

        # Update resource holder based on who is actually executing
        if processo_a_executar.usa_recurso:
            if not processo_detentor_recurso or \
               processo_detentor_recurso.tempo_restante == 0 or \
               processo_detentor_recurso == processo_a_executar:
                processo_detentor_recurso = processo_a_executar
        
        # Execute the chosen process
        # If CMPG was blocked, and processo_a_executar is still CMPG,
        # it means no other process (B or C) was chosen.
        # In this state, CMPG should not execute if it's genuinely blocked.
        # The 'registrar_tentativa_bloqueada' handles the logging.
        # The 'adicionar_processamento' should effectively do nothing if it can't run.
        
        # Check if the process chosen to run is actually blocked by someone else
        is_chosen_process_blocked = False
        if processo_a_executar.usa_recurso and \
           processo_detentor_recurso and \
           processo_detentor_recurso != processo_a_executar and \
           processo_detentor_recurso.tempo_restante > 0:
            is_chosen_process_blocked = True

        if not is_chosen_process_blocked:
            processo_a_executar.adicionar_processamento(
                tempo_atual, 
                tempo_atual + 1, 
                is_handling_special_first_run_block=False # Not the guaranteed first run context here
            )
            tempo_atual += 1
        else:
            # The chosen process is blocked (e.g. A is chosen but C still holds resource and B didn't run)
            # In this case, only advance time. The block was already registered.
            tempo_atual += 1


        if processo_detentor_recurso and processo_detentor_recurso.tempo_restante == 0:
            processo_detentor_recurso = None

    total_espera_final = sum(p.get_espera() for p in processos_param)
    total_turnaround_final = sum(p.get_turnaround() for p in processos_param)
    num_processos = len(processos_param)

    media_espera = total_espera_final / num_processos if num_processos > 0 else 0
    media_turnaround = total_turnaround_final / num_processos if num_processos > 0 else 0
    
    return media_espera, media_turnaround