================================================================================
CITIZEN ASSIST AI - MODULO DE ENERGIA E SUSTENTABILIDADE
Global Solution 2026.2 - Solucoes em Energias Renovaveis e Sustentaveis
================================================================================

1. INTEGRANTES

- Felipe Mello Ramalho Cagnin - RM 569237
- Gabriel Beu Volpato Correa de Assis - RM 563008

2. CONTEXTO E PUBLICO-ALVO

- Publico: condominios residenciais e pequenos comercios urbanos.
- Necessidade: alto custo mensal de eletricidade (areas comuns, elevadores,
  bombas, refrigeracao, iluminacao) e falta de orientacao simples sobre se vale
  a pena investir em eficiencia ou em energia solar.
- Contribuicao do assistente: transforma o consumo (kWh/mes) em custo, CO2,
  investimento e tempo de retorno, compara as alternativas e responde em
  linguagem simples, sempre com referencias e limitacoes.

3. FUNCIONALIDADES DE ENERGIA

1) energy_analysis_engine: calcula custo, emissoes, potencia solar (kWp),
   geracao, investimento e retorno de 3 alternativas.
2) citizen_assist_energy_integration: monta as respostas do assistente.
3) Menu interativo: o usuario informa consumo, tarifa e HSP e consulta:
   analise completa, comparativo, economia/retorno, CO2 evitado, recomendacao,
   limitacoes e referencias. A resposta muda conforme os dados informados.
4) Validacao de entrada: valores zero, negativos ou texto sao recusados.

4. COMO EXECUTAR

- Requisito: Python 3.8 ou superior. Nao ha dependencias externas.
- Comando: python main.py
- Pressione Enter nas perguntas para usar os valores padrao.
- Teste sugerido: consumo 1200 -> opcao 1. Depois consumo 50 -> opcao 5
  (nenhuma alternativa se paga).

5. DADOS E PREMISSAS

Dados estimados estao identificados como tal. Periodo de referencia comum:
1 mes de 30 dias.

| Parametro                   | Valor            | Origem / justificativa                              |
|-----------------------------|------------------|-----------------------------------------------------|
| Consumo mensal              | 1.200 kWh        | ESTIMADO: area comum de condominio pequeno/medio    |
|                             |                  | ou pequeno comercio (editavel pelo usuario)         |
| Tarifa                      | R$ 0,85/kWh      | ESTIMADO: media com impostos; consultar a           |
|                             |                  | distribuidora local no site da ANEEL                |
| Fator de emissao da rede    | 0,0385 kg/kWh    | MCTI, media do SIN em 2023 (38,5 kg CO2/MWh)        |
| Horas de sol pleno (HSP)    | 4,5 h/dia        | ESTIMADO: ordem de grandeza para a regiao Sudeste;  |
|                             |                  | conferir no SunData (CRESESB)                       |
| Eficiencia do sistema solar | 80%              | ESTIMADO: perdas de inversor, cabos, temperatura    |
| Custo do sistema solar      | R$ 4.500/kWp     | ESTIMADO: valor de mercado, exige orcamento         |
| Meta de abatimento solar    | 70% do consumo   | Premissa de projeto (restante vem da rede)          |
| Custo de disponibilidade    | 100 kWh/mes      | ESTIMADO: minimo faturado (depende do tipo de       |
|                             |                  | ligacao)                                            |
| Reducao por eficiencia      | 15% do consumo   | ESTIMADO: troca por LED e equipamentos eficientes   |
| Custo das acoes de          | R$ 8.000         | ESTIMADO                                            |
| eficiencia                  |                  |                                                     |

6. CALCULOS

Unidades: energia em kWh, potencia em kWp, dinheiro em R$, CO2 em kg.

- Custo mensal = max(kWh da rede; 100) x tarifa
- CO2 mensal = kWh da rede x fator de emissao
- Geracao por kWp = HSP x 30 dias x eficiencia = 4,5 x 30 x 0,80 = 108 kWh/mes
- Potencia solar (kWp) = consumo x 0,70 / 108
- Geracao solar = kWp x 108
- kWh da rede (solar) = consumo - geracao
- Investimento solar = kWp x R$ 4.500
- Economia mensal = custo da alternativa 1 - custo da alternativa
- Retorno (payback) em meses = investimento / economia mensal

Resultado para 1.200 kWh/mes (saida real do programa):

| Item                  | 1 - Rede         | 2 - Eficiencia  | 3 - Solar (renovavel) |
|-----------------------|------------------|-----------------|-----------------------|
| Consumo da rede (kWh) | 1.200,00         | 1.020,00        | 360,00                |
| Custo mensal          | R$ 1.020,00      | R$ 867,00       | R$ 306,00             |
| CO2 mensal            | 46,20 kg         | 39,27 kg        | 13,86 kg              |
| Sistema               | -                | -               | 7,78 kWp / 840 kWh    |
| Investimento          | -                | R$ 8.000,00     | R$ 35.000,00          |
| Economia mensal       | -                | R$ 153,00       | R$ 714,00             |
| CO2 evitado           | -                | 6,93 kg/mes     | 32,34 kg/mes          |
|                       |                  | (83,16 kg/ano)  | (388,08 kg/ano)       |
| Retorno               | -                | 52,3 meses      | 49,0 meses            |
|                       |                  | (~4,4 anos)     | (~4,1 anos)           |

7. JUSTIFICATIVAS DAS RECOMENDACOES

- Custo e viabilidade: a solar tem o maior investimento, mas a maior economia
  mensal e o menor retorno (~4,1 anos). A eficiencia custa menos, porem
  economiza menos. Exige telhado ou area livre sem sombra.
- Impacto ambiental: a solar evita cerca de 388 kg de CO2 por ano; a eficiencia,
  cerca de 83 kg. Como a matriz eletrica brasileira ja e muito limpa, o CO2
  evitado e pequeno em valor absoluto; o ganho principal e financeiro.
- Recomendacao do assistente: priorizar eficiencia (barata e imediata) e depois
  instalar solar. Para consumos muito baixos, o custo de disponibilidade faz
  nenhuma alternativa compensar, e o assistente informa isso.

8. LIMITACOES

- As economias, a geracao e os custos sao estimativas, nao resultados garantidos.
- A geracao depende da irradiacao local, clima, sombra, inclinacao e perdas.
- Nao foram considerados: regras de compensacao da Lei 14.300/2022, bandeiras
  tarifarias, impostos sobre energia injetada, manutencao, troca de inversor e
  degradacao dos paineis.
- O fator de emissao e a media anual de 2023; o valor muda a cada ano.
- Necessaria vistoria tecnica e orcamentos reais antes de qualquer investimento.

9. REFERENCIAS

- ANEEL - Agencia Nacional de Energia Eletrica. Tarifas de distribuicao por
  distribuidora. https://www.aneel.gov.br
- MCTI - Ministerio da Ciencia, Tecnologia e Inovacao. Fator medio de emissao
  de CO2 da geracao de energia eletrica no SIN (2023: 38,5 kg CO2/MWh).
  https://www.gov.br/mcti
- CRESESB/CEPEL. Atlas Brasileiro de Energia Solar e SunData (HSP).
  https://cresesb.cepel.br
- EPE - Empresa de Pesquisa Energetica. Anuario Estatistico de Energia
  Eletrica. https://www.epe.gov.br
- BRASIL. Lei n. 14.300, de 6 de janeiro de 2022 (geracao distribuida).

================================================================================
