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

TOTAL_ETNICO_APTOS = 3264
TOTAL_ETNICO_INAPTOS = 3045
PCT_ETNICO_APTOS = 51.74
PCT_ETNICO_INAPTOS = 48.26

TOTAL_PCD_APTOS = 473
TOTAL_PCD_INAPTOS = 186
PCT_PCD_APTOS = 71.78
PCT_PCD_INAPTOS = 28.22

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
