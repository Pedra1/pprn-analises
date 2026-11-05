"""
Configurações Globais, Constantes e Parâmetros Oficiais do Concurso PPRN.
"""

DISCIPLINAS_CONFIG = [
    ("Língua Portuguesa", 15),
    ("História do RN", 5),
    ("Ética no Serviço Público", 5),
    ("Direito Constitucional", 10),
    ("Direito Administrativo", 10),
    ("Direitos Humanos", 10),
    ("Execução Penal", 30),
    ("Legislação Específica", 40),
    ("Direito Penal e Processo Penal", 20),
]

DISCIPLINAS = [d[0] for d in DISCIPLINAS_CONFIG]
PONTOS_MAXIMOS = {d[0]: d[1] for d in DISCIPLINAS_CONFIG}
NOTA_MAXIMA_PROVA = sum(PONTOS_MAXIMOS.values())  # 145 pontos

# Totais gerais estáticos pré-computados (0ms de CPU por reload)
TOTAL_CANDIDATOS = 18945
TOTAL_AMPLA_PURA = 11977
TOTAL_ETNICO = 6309
TOTAL_PCD = 659
TOTAL_NEGRO_PARDO = 6243
TOTAL_INDIGENA = 58
TOTAL_QUILOMBOLA = 29

# Totais Definitivos Pós-Recursos (Publicação Oficial de 04/11/2026)
TOTAL_ETNICO_APTOS = 3586
TOTAL_ETNICO_INAPTOS = 2723
PCT_ETNICO_APTOS = 56.84
PCT_ETNICO_INAPTOS = 43.16

TOTAL_PCD_APTOS = 534
TOTAL_PCD_INAPTOS = 125
PCT_PCD_APTOS = 81.03
PCT_PCD_INAPTOS = 18.97

# Convocação Oficial do TAF (04/11/2026)
TOTAL_CONVOCADOS_TAF_OFICIAL = 1884
TOTAL_CONVOCADOS_AMPLA_OFICIAL = 1074
TOTAL_CONVOCADOS_ETNICO_OFICIAL = 276
TOTAL_CONVOCADOS_PCD_OFICIAL = 534

# Linhas de Corte Oficiais
CORTE_TAF_AMPLA = 119
CORTE_TAF_ETNICO = 114
CORTE_TAF_PCD = 73

# Métricas de Acurácia Oficial do Modelo
ACURACIA_GLOBAL_OFICIAL = 99.07
TOTAL_ACERTOS_OFICIAL = 18769
RECURSOS_ETNICO_PROVIDOS = 322
RECURSOS_PCD_PROVIDOS = 61

TOTAL_CONVOCADOS_TAF_PRELIMINAR = 1850

MAIOR_NOTA = 138
MENOR_NOTA = 73
MEDIA_NOTA = 89.2
MEDIANA_NOTA = 88.0

TOTAL_CANDIDATOS_FMT = "18.945"
TOTAL_AMPLA_FMT = "11.977"
TOTAL_ETNICO_FMT = "6.309"
TOTAL_PCD_FMT = "659"

MEDIAS_DISCIPLINAS = {
    'Língua Portuguesa': 5.55,
    'História do RN': 3.62,
    'Ética no Serviço Público': 3.36,
    'Direito Constitucional': 7.15,
    'Direito Administrativo': 6.99,
    'Direitos Humanos': 7.74,
    'Execução Penal': 17.94,
    'Legislação Específica': 32.79,
    'Direito Penal e Processo Penal': 10.01
}
