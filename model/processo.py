class Periodo:
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
    
    def get_duracao(self):
        return self.fim - self.inicio


class Processo:
    def __init__(self, id, chegada, duracao, prioridade, usa_recurso):
        self.id = id
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade
        self.usa_recurso = usa_recurso # Add the new attribute

        self.tempo_restante = duracao
        self.processamentos = []
        self.tentativas_bloqueadas_ts = [] # Lista para registrar timestamps de tentativas bloqueadas
        self.primeira_execucao_concedida = False # Flag para a primeira execução garantida
        self.foi_bloqueado_na_primeira_exec_garantida = False # Específico para D=1, R=true que foi bloqueado na 1a exec
    
    def registrar_tentativa_bloqueada(self, tempo_ts):
        self.tentativas_bloqueadas_ts.append(tempo_ts)

    def adicionar_processamento(self, inicio, fim, is_handling_special_first_run_block=False):
        duracao_processamento_solicitado = fim - inicio
        
        # Calcula o tempo real de processamento com base no tempo restante
        if self.tempo_restante < duracao_processamento_solicitado:
            fim_real = inicio + self.tempo_restante
            tempo_real_processado = self.tempo_restante
        else:
            fim_real = fim
            tempo_real_processado = duracao_processamento_solicitado

        if tempo_real_processado <= 0 and not (self.duracao == 1 and self.usa_recurso and is_handling_special_first_run_block and self.tempo_restante == 1) : # Adicionado para permitir o caso especial mesmo com tempo_restante = 1 que não seria decrementado
             # Se não há tempo a processar (e não é o caso especial), não faz nada ou retorna 0
             # No caso especial, mesmo que tempo_real_processado seja 1 (e seria o normal), não decrementamos.
             if not (self.duracao == 1 and self.usa_recurso and is_handling_special_first_run_block and self.tempo_restante == 1 and tempo_real_processado == 1):
                return 0


        self.processamentos.append(Periodo(inicio, fim_real))
        
        # Lógica de decremento do tempo_restante
        if not (self.duracao == 1 and self.usa_recurso and is_handling_special_first_run_block):
            self.tempo_restante -= tempo_real_processado
        
        # Garante que tempo_restante não seja negativo
        if self.tempo_restante < 0:
            self.tempo_restante = 0
            
        return tempo_real_processado

    def get_espera(self):
        espera = 0
        tempo_atual = self.chegada

        for periodo in self.processamentos:
            espera += periodo.inicio - tempo_atual
            tempo_atual = periodo.fim

        return espera

    def get_turnaround(self):
        if(len(self.processamentos) == 0):
            return 0

        return self.processamentos[-1].fim - self.chegada

    def verificar_estado(self, instante):
        if(len(self.processamentos) == 0):
            return "Desconhecido"
        
        if(instante < self.chegada):
            return "Antes da chegada"
        
        if(instante >= self.processamentos[-1].fim):
            return "Após a chegada"

        for periodo in self.processamentos:
            if periodo.inicio <= instante < periodo.fim:
                return "Execução"
            
        return "Espera"
    
    def __str__(self):
        return f'Processo(id={self.id}])'
    