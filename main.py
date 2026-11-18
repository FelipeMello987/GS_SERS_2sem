PARAMETROS = {
    "fator_emissao_kg_kwh": 0.0385,
    "tarifa_kwh": 0.85,
    "hsp": 4.5,
    "eficiencia_sistema": 0.80,
    "custo_kwp": 4500.0,
    "disponibilidade_kwh": 100.0,
    "meta_solar": 0.70,
    "reducao_eficiencia": 0.15,
    "custo_eficiencia": 8000.0,
    "dias_mes": 30,
}


class energy_analysis_engine:
    def __init__(self, publico_alvo, consumo_mensal_kwh, tarifa_kwh, fator_emissao_rede, hsp):
        if consumo_mensal_kwh <= 0 or tarifa_kwh <= 0 or fator_emissao_rede <= 0 or hsp <= 0:
            raise ValueError("consumo, tarifa, fator de emissao e hsp devem ser maiores que zero")
        self.publico_alvo = publico_alvo
        self.consumo = consumo_mensal_kwh
        self.tarifa = tarifa_kwh
        self.fator = fator_emissao_rede
        self.hsp = hsp

    def custo_rede(self, kwh_rede):
        cobrado = max(kwh_rede, PARAMETROS["disponibilidade_kwh"])
        return cobrado * self.tarifa

    def montar(self, nome, consumo_rede, capex, extra=None):
        custo = self.custo_rede(consumo_rede)
        co2 = consumo_rede * self.fator
        dados = {
            "nome": nome,
            "consumo_rede_kwh": round(consumo_rede, 2),
            "custo_mensal_rs": round(custo, 2),
            "co2_mensal_kg": round(co2, 2),
            "capex_rs": round(capex, 2),
        }
        if extra:
            dados.update(extra)
        return dados

    def alternativa_convencional(self):
        return self.montar("Alternativa 1 - rede convencional", self.consumo, 0.0)

    def alternativa_eficiencia(self):
        consumo_novo = self.consumo * (1 - PARAMETROS["reducao_eficiencia"])
        return self.montar(
            "Alternativa 2 - eficiencia energetica (LED + equipamentos eficientes)",
            consumo_novo,
            PARAMETROS["custo_eficiencia"],
        )

    def alternativa_solar(self):
        fator_dia = self.hsp * PARAMETROS["dias_mes"] * PARAMETROS["eficiencia_sistema"]
        kwp = self.consumo * PARAMETROS["meta_solar"] / fator_dia
        geracao = kwp * fator_dia
        return self.montar(
            "Alternativa 3 - solar fotovoltaica (renovavel)",
            self.consumo - geracao,
            kwp * PARAMETROS["custo_kwp"],
            {"potencia_kwp": round(kwp, 2), "geracao_mensal_kwh": round(geracao, 2)},
        )

    def analisar(self):
        base = self.alternativa_convencional()
        lista = [base, self.alternativa_eficiencia(), self.alternativa_solar()]
        for alt in lista:
            alt["economia_mensal_rs"] = round(base["custo_mensal_rs"] - alt["custo_mensal_rs"], 2)
            alt["reducao_co2_kg"] = round(base["co2_mensal_kg"] - alt["co2_mensal_kg"], 2)
            if alt["economia_mensal_rs"] > 0:
                alt["payback_meses"] = round(alt["capex_rs"] / alt["economia_mensal_rs"], 1)
            else:
                alt["payback_meses"] = None
        return lista


class citizen_assist_energy_integration:
    def __init__(self, engine):
        self.engine = engine
        self.alternativas = engine.analisar()

    def comparativo(self):
        linhas = [f"Publico: {self.engine.publico_alvo}", f"Consumo de referencia: {self.engine.consumo:.0f} kWh/mes", ""]
        for alt in self.alternativas:
            linhas.append(alt["nome"])
            linhas.append(f"  consumo da rede: {alt['consumo_rede_kwh']:.2f} kWh | custo: R$ {alt['custo_mensal_rs']:.2f}/mes | CO2: {alt['co2_mensal_kg']:.2f} kg/mes")
            if "potencia_kwp" in alt:
                linhas.append(f"  sistema: {alt['potencia_kwp']} kWp gerando {alt['geracao_mensal_kwh']:.2f} kWh/mes")
        return "\n".join(linhas)

    def economia(self):
        linhas = ["Economia e retorno do investimento (valores estimados):"]
        for alt in self.alternativas[1:]:
            payback = alt["payback_meses"]
            texto_payback = f"{payback} meses (~{payback / 12:.1f} anos)" if payback else "nao ha retorno"
            linhas.append(f"- {alt['nome']}")
            linhas.append(f"  investimento: R$ {alt['capex_rs']:.2f} | economia: R$ {alt['economia_mensal_rs']:.2f}/mes | retorno: {texto_payback}")
        return "\n".join(linhas)

    def impacto(self):
        linhas = ["Impacto ambiental (CO2 evitado):"]
        for alt in self.alternativas[1:]:
            linhas.append(f"- {alt['nome']}: {alt['reducao_co2_kg']:.2f} kg/mes ({alt['reducao_co2_kg'] * 12:.2f} kg/ano)")
        return "\n".join(linhas)

    def recomendacao(self):
        validas = [a for a in self.alternativas[1:] if a["payback_meses"]]
        if not validas:
            return "Recomendacao: com esse consumo, nenhuma alternativa se paga. Mantenha a rede e evite desperdicios."
        melhor = min(validas, key=lambda a: a["payback_meses"])
        solar = self.alternativas[2]
        texto = f"Recomendacao: menor tempo de retorno -> {melhor['nome']}."
        if melhor is not solar and solar["payback_meses"]:
            texto += f"\nA solar evita mais CO2 ({solar['reducao_co2_kg']:.2f} kg/mes) e economiza mais por mes (R$ {solar['economia_mensal_rs']:.2f})."
        texto += "\nO ideal e combinar: primeiro eficiencia, depois solar."
        return texto

    def limitacoes(self):
        return "\n".join([
            "Limitacoes e premissas:",
            "- Valores sao estimativas, nao garantias de economia.",
            f"- Irradiacao (HSP) de {self.engine.hsp} h/dia e eficiencia de {PARAMETROS['eficiencia_sistema'] * 100:.0f}% variam com clima, sombra, inclinacao e perdas do inversor.",
            f"- Custo minimo de disponibilidade considerado: {PARAMETROS['disponibilidade_kwh']:.0f} kWh/mes.",
            "- Nao inclui regras de compensacao da Lei 14.300/2022, bandeiras tarifarias, impostos sobre a energia injetada, manutencao e degradacao dos paineis.",
            "- Custos de instalacao e de eficiencia sao estimados; peca orcamentos e vistoria tecnica.",
            "",
            "Referencias:",
            "- ANEEL: tarifas de energia por distribuidora (www.aneel.gov.br).",
            "- MCTI: fator medio de emissao do SIN, 2023 = 38,5 kg CO2/MWh (www.gov.br/mcti).",
            "- CRESESB/CEPEL: Atlas Brasileiro de Energia Solar e SunData (HSP).",
            "- EPE: Anuario Estatistico de Energia Eletrica (www.epe.gov.br).",
            "- Lei 14.300/2022: marco legal da geracao distribuida.",
        ])

    def resposta_completa(self):
        partes = [self.comparativo(), self.economia(), self.impacto(), self.recomendacao(), self.limitacoes()]
        return "\n\n".join(partes)


def ler_numero(texto, padrao, minimo, maximo):
    while True:
        entrada = input(f"{texto} [{padrao}]: ").strip().replace(",", ".")
        if entrada == "":
            return padrao
        try:
            valor = float(entrada)
        except ValueError:
            print("Digite um numero valido.")
            continue
        if minimo < valor <= maximo:
            return valor
        print(f"O valor deve ser maior que {minimo} e no maximo {maximo}.")


def menu(assistente):
    opcoes = {
        "1": assistente.resposta_completa,
        "2": assistente.comparativo,
        "3": assistente.economia,
        "4": assistente.impacto,
        "5": assistente.recomendacao,
        "6": assistente.limitacoes,
    }
    while True:
        print("\n--- Citizen Assist AI | Energia e Sustentabilidade ---")
        print("1 - Analise completa")
        print("2 - Comparativo das alternativas")
        print("3 - Quanto posso economizar? (custo e retorno)")
        print("4 - Quanto CO2 evito?")
        print("5 - Qual alternativa recomendada?")
        print("6 - Limitacoes e referencias")
        print("0 - Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "0":
            break
        if escolha in opcoes:
            print()
            print(opcoes[escolha]())
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    print("Modulo de energia - condominios residenciais e pequenos comercios urbanos")
    print("Pressione Enter para usar o valor padrao entre colchetes.\n")
    consumo = ler_numero("Consumo mensal (kWh)", 1200.0, 0, 100000)
    tarifa = ler_numero("Tarifa (R$/kWh)", PARAMETROS["tarifa_kwh"], 0, 10)
    hsp = ler_numero("Horas de sol pleno por dia (HSP)", PARAMETROS["hsp"], 0, 8)
    motor = energy_analysis_engine(
        "condominios residenciais e pequenos comercios urbanos",
        consumo,
        tarifa,
        PARAMETROS["fator_emissao_kg_kwh"],
        hsp,
    )
    menu(citizen_assist_energy_integration(motor))