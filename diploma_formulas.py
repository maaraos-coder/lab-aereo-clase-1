"""Formulario acumulativo del Diplomado en Acústica en la Edificación."""

FORMULA_CATALOG = [
    {
        "course": "Aislamiento acústico al ruido aéreo",
        "labs": [
            {
                "number": 1,
                "subtitle": "Fundamentos, recintos, transmisión y evaluación económica",
                "topics": [
                    ("Recintos y absorción", [
                        ("Absorción equivalente", "A = Σ(α<sub>i</sub>·S<sub>i</sub>)",
                         [("A", "absorción acústica equivalente", "m² sabin"),
                          ("α<sub>i</sub>", "coeficiente de absorción de la superficie i", "adimensional"),
                          ("S<sub>i</sub>", "área de la superficie i", "m²")],
                         "Suma el aporte absorbente de las superficies de un recinto."),
                        ("Tiempo de reverberación de Sabine", "T<sub>60</sub> = 0,161·V/A",
                         [("T<sub>60</sub>", "tiempo para un decaimiento de 60 dB", "s"),
                          ("V", "volumen del recinto", "m³"),
                          ("A", "absorción acústica equivalente", "m² sabin")],
                         "Estimación para un campo suficientemente difuso."),
                    ]),
                    ("Transmisión y elementos compuestos", [
                        ("Coeficiente de transmisión", "τ = 10<sup>−R/10</sup>",
                         [("τ", "potencia transmitida dividida por la incidente", "adimensional"),
                          ("R", "índice de reducción sonora por banda", "dB")],
                         "Convierte decibeles de aislamiento en una fracción energética."),
                        ("Cerramiento compuesto",
                         "τ<sub>t</sub> = Σ(S<sub>i</sub>·τ<sub>i</sub>)/ΣS<sub>i</sub><br>R<sub>t</sub> = −10·log<sub>10</sub>(τ<sub>t</sub>)",
                         [("τ<sub>t</sub>", "coeficiente de transmisión total", "adimensional"),
                          ("S<sub>i</sub>", "área de cada componente", "m²"),
                          ("τ<sub>i</sub>", "coeficiente de transmisión de cada componente", "adimensional"),
                          ("R<sub>t</sub>", "índice de reducción sonora compuesto", "dB")],
                         "Combina muro, puerta, ventana u otros componentes; los dB no se promedian."),
                    ]),
                    ("Placas y sistemas dobles", [
                        ("Ley de masa", "R ≈ 20·log<sub>10</sub>(m′·f) − 47",
                         [("R", "índice de reducción sonora aproximado", "dB"),
                          ("m′", "masa superficial de la placa", "kg/m²"),
                          ("f", "frecuencia", "Hz")],
                         "Aproximación ideal fuera de resonancias, coincidencia, fugas y flancos."),
                        ("Rigidez flexional", "D = E·h<sup>3</sup>/[12·(1−ν<sup>2</sup>)]",
                         [("D", "rigidez flexional por unidad de ancho", "N·m"),
                          ("E", "módulo de Young", "Pa"), ("h", "espesor", "m"),
                          ("ν", "coeficiente de Poisson", "adimensional")],
                         "Paso previo para estimar la frecuencia crítica de una placa homogénea."),
                        ("Frecuencia crítica", "f<sub>c</sub> = c<sup>2</sup>/(2π)·√(m′/D)",
                         [("f<sub>c</sub>", "frecuencia crítica o de coincidencia", "Hz"),
                          ("c", "velocidad del sonido en el aire", "m/s"),
                          ("m′", "masa superficial", "kg/m²"), ("D", "rigidez flexional", "N·m")],
                         "Ubica la zona donde la coincidencia puede disminuir el aislamiento."),
                    ]),
                    ("Evaluación económica", [
                        ("Flujo neto anual", "F<sub>neto</sub> = B<sub>bruto</sub> − C<sub>recurrente</sub>",
                         [("F<sub>neto</sub>", "flujo neto anual", "$/año"),
                          ("B<sub>bruto</sub>", "beneficio bruto anual", "$/año"),
                          ("C<sub>recurrente</sub>", "costos recurrentes anuales", "$/año")],
                         "Determina el flujo anual disponible para recuperar la inversión."),
                        ("Payback", "Payback = I<sub>0</sub>/F<sub>neto</sub>",
                         [("I<sub>0</sub>", "inversión inicial", "$"),
                          ("F<sub>neto</sub>", "flujo neto anual", "$/año"),
                          ("Payback", "periodo de recuperación", "años")],
                         "Solo es interpretable cuando el flujo neto es positivo."),
                        ("Retorno sobre la inversión", "ROI = (B<sub>total</sub>−C<sub>total</sub>)/C<sub>total</sub>·100",
                         [("B<sub>total</sub>", "beneficios acumulados del periodo", "$"),
                          ("C<sub>total</sub>", "costos totales del mismo periodo", "$"),
                          ("ROI", "retorno sobre los costos", "%")],
                         "Compara beneficios y costos dentro del mismo horizonte temporal."),
                    ]),
                ],
            },
            {
                "number": 2,
                "subtitle": "CES–MINVU, tesis, ISO 12354 y casos profesionales",
                "topics": [
                    ("Descriptores", [
                        ("Adaptaciones espectrales", "R<sub>w</sub> + C &nbsp;·&nbsp; R<sub>w</sub> + C<sub>tr</sub>",
                         [("R<sub>w</sub>", "índice ponderado de reducción sonora de laboratorio", "dB"),
                          ("C", "adaptación para espectros medios y altos", "dB"),
                          ("C<sub>tr</sub>", "adaptación para tránsito y contenido grave", "dB")],
                         "El término se selecciona según el espectro de la fuente."),
                        ("Diferencia de nivel estandarizada",
                         "D<sub>nT</sub> = L<sub>1</sub>−L<sub>2</sub>+10·log<sub>10</sub>(T/T<sub>0</sub>)",
                         [("D<sub>nT</sub>", "diferencia de nivel estandarizada", "dB"),
                          ("L<sub>1</sub>", "nivel medio en el recinto emisor", "dB"),
                          ("L<sub>2</sub>", "nivel medio en el recinto receptor", "dB"),
                          ("T", "tiempo de reverberación medido en el receptor", "s"),
                          ("T<sub>0</sub>", "tiempo de reverberación de referencia", "s")],
                         "Caracteriza la separación entre recintos corrigiendo la reverberación del receptor."),
                        ("Descriptor adaptado", "D<sub>nT,A</sub> = D<sub>nT,w</sub> + C",
                         [("D<sub>nT,A</sub>", "diferencia estandarizada ponderada y adaptada", "dB"),
                          ("D<sub>nT,w</sub>", "valor único ponderado de DnT", "dB"),
                          ("C", "término de adaptación espectral", "dB")],
                         "Se usa con el término espectral exigido por el criterio del caso."),
                    ]),
                    ("Predicción simplificada", [
                        ("Paso de elemento a edificio",
                         "D<sub>nT,A</sub> ≈ R<sub>comp,A</sub> + 10·log<sub>10</sub>(0,32·V/S) − L<sub>obra</sub>",
                         [("R<sub>comp,A</sub>", "reducción adaptada del cerramiento compuesto", "dB"),
                          ("V", "volumen del recinto receptor", "m³"),
                          ("S", "área del elemento separador", "m²"),
                          ("L<sub>obra</sub>", "pérdida estimada de montaje y encuentros", "dB")],
                         "Modelo didáctico del caso; no sustituye un cálculo completo según ISO 12354."),
                    ]),
                ],
            },
        ],
    },
    {
        "course": "Control de ruido de impacto y ruido de instalaciones",
        "labs": [
            {"number": 1, "subtitle": "Ruido de impacto y transmisión estructural", "topics": [
                ("Impacto entre recintos", [
                    ("Nivel de presión de ruido de impactos normalizado",
                     "L′<sub>n</sub> = L<sub>i</sub> + 10·log<sub>10</sub>(A/A<sub>0</sub>)",
                     [("L′<sub>n</sub>", "nivel de impacto normalizado", "dB"),
                      ("L<sub>i</sub>", "nivel medio medido en el receptor", "dB"),
                      ("A", "absorción equivalente del receptor", "m²"),
                      ("A<sub>0</sub>", "absorción de referencia", "m²")],
                     "Normaliza el resultado mediante la absorción equivalente."),
                    ("Nivel de impacto estandarizado",
                     "L′<sub>nT</sub> = L<sub>i</sub> − 10·log<sub>10</sub>(T/T<sub>0</sub>)",
                     [("L′<sub>nT</sub>", "nivel de impacto estandarizado", "dB"),
                      ("L<sub>i</sub>", "nivel medio medido en el receptor", "dB"),
                      ("T", "tiempo de reverberación medido", "s"),
                      ("T<sub>0</sub>", "tiempo de reverberación de referencia", "s")],
                     "En ruido de impacto un valor menor representa mejor desempeño."),
                    ("Mejora de un revestimiento", "ΔL = L<sub>n,0</sub> − L<sub>n</sub>",
                     [("ΔL", "reducción del nivel de impacto", "dB"),
                      ("L<sub>n,0</sub>", "nivel sin revestimiento", "dB"),
                      ("L<sub>n</sub>", "nivel con revestimiento", "dB")],
                     "Compara un piso de referencia antes y después del revestimiento."),
                ])]},
            {"number": 2, "subtitle": "Instalaciones, vibraciones y control", "topics": [
                ("Aislamiento vibratorio", [
                    ("Frecuencia natural", "f<sub>n</sub> = (1/2π)·√(k/m)",
                     [("f<sub>n</sub>", "frecuencia natural del sistema", "Hz"),
                      ("k", "rigidez equivalente del apoyo", "N/m"),
                      ("m", "masa soportada", "kg")],
                     "Permite evaluar la relación entre la excitación y el sistema aislador."),
                    ("Razón de frecuencias", "r = f/f<sub>n</sub>",
                     [("r", "razón de frecuencias", "adimensional"),
                      ("f", "frecuencia de excitación", "Hz"),
                      ("f<sub>n</sub>", "frecuencia natural", "Hz")],
                     "El aislamiento comienza por encima de la zona de resonancia."),
                    ("Transmisibilidad", "T<sub>r</sub> = √[(1+(2ζr)²)/((1−r²)²+(2ζr)²)]",
                     [("T<sub>r</sub>", "transmisibilidad de fuerza", "adimensional"),
                      ("ζ", "razón de amortiguamiento", "adimensional"),
                      ("r", "razón de frecuencias", "adimensional")],
                     "Modelo lineal de un grado de libertad; requiere condiciones compatibles."),
                ])]},
        ],
    },
    {
        "course": "Control de ruido ambiental",
        "labs": [
            {"number": 1, "subtitle": "Magnitudes, propagación y medición", "topics": [
                ("Niveles y propagación", [
                    ("Suma energética de niveles", "L<sub>T</sub> = 10·log<sub>10</sub>[Σ10<sup>L<sub>i</sub>/10</sup>]",
                     [("L<sub>T</sub>", "nivel total", "dB"), ("L<sub>i</sub>", "nivel de cada fuente", "dB")],
                     "Los niveles sonoros no se suman aritméticamente."),
                    ("Nivel equivalente", "L<sub>eq,T</sub> = 10·log<sub>10</sub>[(1/T)·Σ(t<sub>i</sub>·10<sup>L<sub>i</sub>/10</sup>)]",
                     [("L<sub>eq,T</sub>", "nivel continuo equivalente del periodo", "dB"),
                      ("T", "duración total", "s"), ("t<sub>i</sub>", "duración del intervalo i", "s"),
                      ("L<sub>i</sub>", "nivel del intervalo i", "dB")],
                     "Integra exposiciones de distinta duración en un nivel energético equivalente."),
                    ("Divergencia esférica", "L<sub>p,2</sub> = L<sub>p,1</sub> − 20·log<sub>10</sub>(r<sub>2</sub>/r<sub>1</sub>)",
                     [("L<sub>p,1</sub>, L<sub>p,2</sub>", "niveles en las posiciones 1 y 2", "dB"),
                      ("r<sub>1</sub>, r<sub>2</sub>", "distancias a la fuente", "m")],
                     "Aproximación de campo libre para una fuente puntual."),
                ])]},
            {"number": 2, "subtitle": "Evaluación, fondo y medidas de control", "topics": [
                ("Correcciones y criterio", [
                    ("Corrección por ruido de fondo", "L<sub>fuente</sub> = 10·log<sub>10</sub>(10<sup>L<sub>total</sub>/10</sup>−10<sup>L<sub>fondo</sub>/10</sup>)",
                     [("L<sub>fuente</sub>", "nivel atribuido a la fuente", "dB"),
                      ("L<sub>total</sub>", "nivel con la fuente operando", "dB"),
                      ("L<sub>fondo</sub>", "nivel de ruido de fondo", "dB")],
                     "Solo es válida cuando la diferencia permite separar ambas contribuciones con confiabilidad."),
                    ("Atenuación de barrera", "IL = L<sub>sin</sub> − L<sub>con</sub>",
                     [("IL", "pérdida por inserción", "dB"),
                      ("L<sub>sin</sub>", "nivel sin la medida de control", "dB"),
                      ("L<sub>con</sub>", "nivel con la medida de control", "dB")],
                     "Compara estados equivalentes antes y después de instalar la barrera."),
                ])]},
        ],
    },
    {
        "course": "Factores del ruido en el proceso de construcción",
        "labs": [
            {"number": 1, "subtitle": "Fuentes, etapas de obra y predicción", "topics": [
                ("Predicción de obra", [
                    ("Propagación por distancia", "L<sub>p,2</sub> = L<sub>p,1</sub> − 20·log<sub>10</sub>(r<sub>2</sub>/r<sub>1</sub>)",
                     [("L<sub>p,1</sub>, L<sub>p,2</sub>", "niveles a dos distancias", "dB"),
                      ("r<sub>1</sub>, r<sub>2</sub>", "distancias a la fuente", "m")],
                     "Estimación inicial en campo libre para una fuente aproximadamente puntual."),
                    ("Operación parcial", "L<sub>eq</sub> = L<sub>op</sub> + 10·log<sub>10</sub>(t<sub>op</sub>/T)",
                     [("L<sub>eq</sub>", "nivel equivalente del periodo", "dB"),
                      ("L<sub>op</sub>", "nivel durante la operación", "dB"),
                      ("t<sub>op</sub>", "tiempo efectivo de operación", "min o s"),
                      ("T", "periodo total con la misma unidad", "min o s")],
                     "Representa el aporte temporal de una actividad intermitente."),
                ])]},
            {"number": 2, "subtitle": "Plan de manejo y verificación en terreno", "topics": [
                ("Gestión y seguimiento", [
                    ("Reducción verificada", "ΔL = L<sub>antes</sub> − L<sub>después</sub>",
                     [("ΔL", "reducción observada", "dB"),
                      ("L<sub>antes</sub>", "nivel antes de la medida", "dB"),
                      ("L<sub>después</sub>", "nivel después de la medida", "dB")],
                     "Exige condiciones de operación y medición comparables."),
                    ("Cumplimiento", "Margen = L<sub>límite</sub> − L<sub>evaluado</sub>",
                     [("Margen", "holgura respecto del límite", "dB"),
                      ("L<sub>límite</sub>", "límite aplicable", "dB"),
                      ("L<sub>evaluado</sub>", "nivel determinado según el procedimiento", "dB")],
                     "Margen positivo indica valor bajo el límite; no reemplaza la revisión del procedimiento."),
                ])]},
        ],
    },
    {
        "course": "Certificaciones acústicas en la edificación residencial",
        "labs": [
            {"number": 1, "subtitle": "Ensayos, muestreo e incertidumbre", "topics": [
                ("Trazabilidad del ensayo", [
                    ("Diferencia de nivel", "D = L<sub>1</sub> − L<sub>2</sub>",
                     [("D", "diferencia de niveles por banda", "dB"),
                      ("L<sub>1</sub>", "nivel medio en el recinto emisor", "dB"),
                      ("L<sub>2</sub>", "nivel medio en el recinto receptor", "dB")],
                     "Magnitud base; la normalización o estandarización depende del descriptor requerido."),
                    ("Absorción equivalente desde reverberación", "A = 0,161·V/T",
                     [("A", "absorción equivalente del recinto receptor", "m² sabin"),
                      ("V", "volumen del recinto", "m³"), ("T", "tiempo de reverberación", "s")],
                     "Relación de Sabine usada bajo sus condiciones de aplicación."),
                    ("Incertidumbre expandida", "U = k·u<sub>c</sub>",
                     [("U", "incertidumbre expandida", "unidad de la magnitud"),
                      ("k", "factor de cobertura", "adimensional"),
                      ("u<sub>c</sub>", "incertidumbre estándar combinada", "unidad de la magnitud")],
                     "La regla de decisión debe declarar cómo se considera la incertidumbre."),
                ])]},
            {"number": 2, "subtitle": "Clasificación, conformidad e informe final", "topics": [
                ("Indicadores y conformidad", [
                    ("Descriptor de fachada adaptado", "D<sub>2m,nT,Atr</sub> = D<sub>2m,nT,w</sub> + C<sub>tr</sub>",
                     [("D<sub>2m,nT,Atr</sub>", "diferencia de nivel de fachada estandarizada y adaptada", "dB"),
                      ("D<sub>2m,nT,w</sub>", "valor ponderado de fachada", "dB"),
                      ("C<sub>tr</sub>", "adaptación espectral para tránsito", "dB")],
                     "Se usa cuando la fuente exterior se representa mediante el espectro de tránsito."),
                    ("Margen de conformidad", "M = X<sub>medido</sub> − X<sub>requisito</sub>",
                     [("M", "margen de conformidad", "dB"),
                      ("X<sub>medido</sub>", "descriptor obtenido", "dB"),
                      ("X<sub>requisito</sub>", "valor mínimo exigido", "dB")],
                     "Esta orientación corresponde a requisitos mínimos; para máximos se invierte la comparación."),
                ])]},
        ],
    },
]


def _cards(formulae):
    html = ""
    for name, equation, variables, use in formulae:
        rows = "".join(
            f"<tr><th>{symbol}</th><td>{meaning}</td><td>{unit}</td></tr>"
            for symbol, meaning, unit in variables
        )
        html += (
            f"<article><h4>{name}</h4><div class='eq'>{equation}</div>"
            "<table><thead><tr><th>Símbolo</th><th>Corresponde a</th><th>Unidad</th></tr></thead>"
            f"<tbody>{rows}</tbody></table><p class='use'><b>Uso:</b> {use}</p></article>"
        )
    return html


def build_formulary_html(visible_labs):
    """Build the complete teacher view or the progressively released student view."""
    body = ""
    visible_count = 0
    for course_index, course in enumerate(FORMULA_CATALOG, 1):
        labs_html = ""
        for lab in course["labs"]:
            key = (course_index, lab["number"])
            if key not in visible_labs:
                continue
            visible_count += 1
            topics = "".join(
                f"<div class='topic'><h3>{topic}</h3>{_cards(formulae)}</div>"
                for topic, formulae in lab["topics"]
            )
            labs_html += (
                f"<details class='lab' open><summary>Laboratorio {lab['number']} · "
                f"{lab['subtitle']}</summary>{topics}</details>"
            )
        if labs_html:
            body += (
                f"<section class='course'><h2>Curso {course_index} · {course['course']}</h2>"
                f"{labs_html}</section>"
            )
    if not body:
        body = "<div class='empty'>Aún no hay fórmulas publicadas para este perfil.</div>"
    return f"""<!doctype html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Formulario del Diplomado</title><style>
    *{{box-sizing:border-box}}body{{font-family:Arial,sans-serif;background:#f3f7fb;color:#102b49;margin:0;padding:18px}}
    header{{position:sticky;top:0;z-index:5;background:linear-gradient(135deg,#07172b,#0878bd);color:#fff;
    border-radius:14px;padding:16px 18px;box-shadow:0 8px 22px #07172b33}}
    header b{{font-size:21px}}header span{{display:block;color:#d9f5ff;font-size:12px;margin-top:5px}}
    .course{{margin-top:18px}}h2{{font-size:18px;color:#073f6b;margin:0 0 9px}}
    details.lab{{background:#fff;border:1px solid #cfe1ef;border-radius:13px;margin:9px 0;overflow:hidden}}
    summary{{cursor:pointer;background:#e8f5fd;color:#084f83;font-weight:800;padding:13px 15px}}
    .topic{{padding:4px 13px 11px}}.topic h3{{font-size:14px;color:#08724e;border-bottom:2px solid #d8eee4;padding-bottom:6px}}
    article{{border:1px solid #d8e6f3;border-left:5px solid #0a75bd;border-radius:11px;padding:11px 13px;margin:10px 0}}
    h4{{font-size:14px;margin:0 0 7px;color:#0a4f86}}.eq{{font-size:20px;font-weight:800;line-height:1.55;margin:7px 0 10px}}
    table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{padding:6px 7px;border-top:1px solid #e1eaf2;text-align:left;vertical-align:top}}
    thead th{{color:#53657a;font-size:11px;text-transform:uppercase}}tbody th{{color:#083f6b;white-space:nowrap}}
    .use{{font-size:12px;color:#53657a;margin:9px 0 0}}.empty{{background:#fff4d9;border-radius:12px;padding:16px;margin-top:16px}}
    </style></head><body><header><b>📐 Formulario del Diplomado</b>
    <span>Compendio acumulativo · {visible_count} laboratorio(s) disponible(s)</span></header>{body}</body></html>"""
