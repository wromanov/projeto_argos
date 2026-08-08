VALOR_PERSONALIZADO = "__PERSONALIZADO__"


FARMS_CATALOGO = (
    "ESTACIONAMENTO",
    "STVV",
    "ALFANDEGAMENTO",
    "BOLSÃO DE TAXI",
    "TDNA",
    "COANA",
    "FACE X",
    "POC",
)


FARM_CHOICES = (
    ("", "---------"),
    *(
        (valor, valor)
        for valor in FARMS_CATALOGO
    ),
    (
        VALOR_PERSONALIZADO,
        "PERSONALIZADO",
    ),
)
