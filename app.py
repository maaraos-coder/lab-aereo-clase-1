import hashlib
import math
import random
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="LAB AÉREO | Curso 1",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
LOGO_UC = ROOT / "assets" / "logo_uc.png"
LOGO_DECON = ROOT / "assets" / "logo_decon_uc.png"
FREQS = np.array([100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150])
REF_RW = np.array([-19, -16, -13, -10, -7, -4, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8])


st.markdown(
    """
    <style>
    :root{--navy:#071a31;--blue:#0875d1;--cyan:#18bddd;--ink:#14243a;
    --muted:#64748b;--line:#dbe5ef;--soft:#f4f8fc;--green:#118566;--orange:#e98324}
    .stApp{background:#f6f8fb;color:var(--ink)}
    .block-container{max-width:1420px;padding-top:1.3rem}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#06172b,#0b3156)}
    [data-testid="stSidebar"] *{color:#eef7ff}
    [data-testid="stSidebar"] .stProgress > div > div{background:#22c8e8}
    h1,h2,h3{letter-spacing:-.025em;color:var(--ink)}
    .hero{padding:2rem;border-radius:24px;background:linear-gradient(125deg,#071a31,#0a4777);
    box-shadow:0 18px 45px #0b315622;color:white;margin-bottom:1rem}
    .hero h1{color:white;margin:.35rem 0}.hero p{color:#d8eafb;max-width:900px}
    .eyebrow{font-size:.75rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#18bddd}
    .card{background:white;border:1px solid var(--line);border-radius:18px;padding:1.2rem;
    box-shadow:0 7px 22px #193b5e0d;margin:.55rem 0}
    .concept{background:#eaf6ff;border-left:5px solid var(--blue);border-radius:13px;padding:1rem;margin:.7rem 0}
    .warning{background:#fff5e8;border-left:5px solid var(--orange);border-radius:13px;padding:1rem;margin:.7rem 0}
    .formula{background:#071a31;color:white;border-radius:14px;padding:1rem;text-align:center;font-size:1.25rem}
    .badge{display:inline-block;background:#0d4069;color:#bceeff;border:1px solid #2d698f;
    border-radius:99px;padding:.3rem .75rem;font-weight:700;font-size:.75rem}
    .stage{display:grid;grid-template-columns:45px 1fr;gap:.8rem;align-items:start}
    .stage-number{display:grid;place-items:center;width:40px;height:40px;border-radius:12px;
    background:#e7f3ff;color:#0875d1;font-weight:900}
    .result{background:linear-gradient(125deg,#071a31,#0d4069);color:white;border-radius:18px;padding:1.2rem}
    .result b{font-size:1.7rem;color:#69e5ff}.result small{color:#bad1e4}
    div[data-testid="stMetric"]{background:white;border:1px solid var(--line);border-radius:15px;padding:1rem}
    button[kind="primary"]{background:#0875d1!important;border-radius:10px!important}
    .footer{text-align:center;color:#718096;border-top:1px solid var(--line);padding:1rem;margin-top:2rem}
    </style>
    """,
    unsafe_allow_html=True,
)


STAGES = [
    ("Inicio", "Presentación y ruta del curso"),
    ("Etapa 1", "Sonido, frecuencia y longitud de onda"),
    ("Etapa 2", "Decibeles y suma energética"),
    ("Etapa 3", "Espectros y bandas de frecuencia"),
    ("Etapa 4", "Absorción y reverberación"),
    ("Etapa 5", "Aislamiento versus absorción"),
    ("Etapa 6", "Fundamentos físicos de transmisión"),
    ("Etapa 7", "Aplicación práctica de transmisión"),
    ("Etapa 8", "Índices Rw, STC y otros"),
    ("Etapa 9", "Aplicación práctica de índices"),
    ("Etapa 10", "Evaluación final del Curso 1"),
]


QUESTIONS = [
    ("Fundamentos", "Una onda de 250 Hz se propaga a 343 m/s. ¿Cuál es su longitud de onda aproximada?", ["0,73 m", "1,37 m", "2,50 m", "343 m"], 1, "λ=c/f=343/250≈1,37 m."),
    ("Fundamentos", "Si aumenta la frecuencia y la velocidad permanece constante, la longitud de onda:", ["Aumenta", "Disminuye", "No cambia", "Se anula"], 1, "La longitud de onda es inversamente proporcional a la frecuencia."),
    ("Fundamentos", "¿Qué describe mejor la frecuencia?", ["Energía total", "Oscilaciones por segundo", "Tiempo de reverberación", "Área absorbente"], 1, "La frecuencia se expresa en hertz: ciclos por segundo."),
    ("Decibeles", "Dos fuentes independientes de 60 dB producen juntas aproximadamente:", ["60 dB", "63 dB", "120 dB", "66 dB"], 1, "Dos niveles iguales suman 3 dB."),
    ("Decibeles", "¿Qué operación debe usarse para sumar niveles sonoros?", ["Promedio aritmético", "Suma logarítmica energética", "Resta directa", "Multiplicación"], 1, "Los decibeles no se suman aritméticamente."),
    ("Decibeles", "Una reducción de 10 dB en el nivel corresponde a una intensidad:", ["Diez veces menor", "Dos veces menor", "Cien veces menor", "Igual"], 0, "Diez decibeles equivalen a un factor 10 en intensidad."),
    ("Decibeles", "Si L1=85 dB y una partición aporta R=35 dB en un modelo simplificado, L2 es:", ["50 dB", "60 dB", "120 dB", "35 dB"], 0, "L2=L1−R=50 dB."),
    ("Espectros", "Una banda de octava tiene como relación entre límites superior e inferior:", ["2", "10", "√2", "3"], 0, "Una octava duplica la frecuencia."),
    ("Espectros", "¿Para qué sirve analizar el espectro por bandas?", ["Para ocultar tonos", "Para identificar frecuencias dominantes", "Para convertir absorción en aislamiento", "Para sumar superficies"], 1, "El espectro muestra dónde se concentra la energía."),
    ("Espectros", "Una máquina presenta un tono dominante en 125 Hz. ¿Qué debe revisarse primero?", ["Solo Rw", "La curva en 125 Hz", "Solo STC", "El color del muro"], 1, "Una fuente tonal exige revisar la banda crítica."),
    ("Reverberación", "En la ecuación de Sabine, al aumentar la absorción equivalente A, T60:", ["Aumenta", "Disminuye", "No cambia", "Se duplica siempre"], 1, "T60=0,161V/A."),
    ("Reverberación", "Para V=100 m³ y A=20 m² sabin, T60 es aproximadamente:", ["0,08 s", "0,81 s", "3,22 s", "5,00 s"], 1, "0,161×100/20=0,805 s."),
    ("Reverberación", "Instalar material absorbente dentro de un recinto modifica principalmente:", ["La reverberación interior", "La masa del muro", "La frecuencia de la fuente", "El STC automáticamente"], 0, "La absorción reduce reflexiones y reverberación."),
    ("Transmisión", "¿Qué magnitud relaciona energía transmitida e incidente?", ["α", "τ", "T60", "C"], 1, "τ es el coeficiente de transmisión."),
    ("Transmisión", "Para R=40 dB, τ vale aproximadamente:", ["10⁻²", "10⁻³", "10⁻⁴", "40"], 2, "τ=10^(−R/10)=10⁻⁴."),
    ("Transmisión", "Si R aumenta 10 dB, la energía transmitida:", ["Se reduce a la mitad", "Se reduce a una décima", "No cambia", "Se duplica"], 1, "Un aumento de 10 dB en R divide τ por 10."),
    ("Transmisión", "En un cerramiento compuesto, el elemento que suele dominar es:", ["El de mayor superficie siempre", "El de menor aislamiento", "El más caro", "El más absorbente"], 1, "Una puerta o rendija débil puede dominar la transmisión."),
    ("Ley de masa", "Al duplicar la masa superficial de una hoja simple ideal, R aumenta aproximadamente:", ["3 dB", "6 dB", "10 dB", "20 dB"], 1, "20log10(2)≈6 dB."),
    ("Ley de masa", "La masa superficial se calcula como:", ["ρ/t", "ρ·t", "t/ρ", "ρ+t"], 1, "m′=densidad por espesor."),
    ("Ley de masa", "La ley de masa ideal no representa adecuadamente:", ["El efecto general de masa", "Resonancias y coincidencia", "La frecuencia", "El logaritmo"], 1, "Los sistemas reales presentan resonancias, coincidencia y uniones."),
    ("Ley de masa", "El valle de coincidencia puede causar:", ["Una mejora infinita", "Una disminución local del aislamiento", "Absorción igual a uno", "Frecuencia cero"], 1, "En torno a la frecuencia crítica puede caer R."),
    ("Curvas", "Dos tabiques tienen igual Rw. Esto significa que:", ["Sus curvas son idénticas", "Siempre sirven para lo mismo", "Pueden responder distinto por frecuencia", "Tienen igual costo"], 2, "El índice único puede ocultar diferencias espectrales."),
    ("Curvas", "Para ruido grave de maquinaria conviene priorizar:", ["La curva completa en bajas frecuencias", "Solo el promedio", "Solo 4 kHz", "La absorción del piso"], 0, "La decisión debe corresponder al espectro real."),
    ("Curvas", "Un error aritmético menor con procedimiento correcto debería:", ["Anular todo", "Recibir puntaje parcial", "Aprobar automáticamente", "Ignorarse siempre"], 1, "La evaluación práctica considera procedimiento e interpretación."),
    ("Índices", "Rw se obtiene mediante:", ["Promedio simple", "Desplazamiento de una curva de referencia", "La suma de espesores", "El tiempo de reverberación"], 1, "ISO 717-1 usa una curva de referencia y desviaciones desfavorables."),
    ("Índices", "En Rw(C;Ctr)=52(−2;−7), Rw+Ctr es:", ["59 dB", "54 dB", "50 dB", "45 dB"], 3, "52−7=45 dB."),
    ("Índices", "¿Qué índice describe un elemento ensayado en laboratorio bajo ISO?", ["Rw", "R'w", "DnT,w", "ASTC"], 0, "Rw caracteriza el elemento bajo condiciones de laboratorio."),
    ("Índices", "¿Cuál es la afirmación correcta?", ["STC=Rw+2 siempre", "Rw y STC son métodos diferentes", "OITC es absorción", "Ctr aumenta siempre Rw"], 1, "No existe conversión fija y universal entre Rw y STC."),
    ("Índices", "Para una fachada expuesta a tránsito, es especialmente relevante:", ["Rw+C", "D2m,nT,w+Ctr u OITC", "αw", "CAC interior únicamente"], 1, "Ctr y OITC consideran mejor el contenido grave del transporte."),
]


def init_state():
    defaults = {
        "authenticated": False,
        "role": None,
        "name": "",
        "email": "",
        "page": "Inicio",
        "exam_started": False,
        "exam_done": False,
        "exam_index": 0,
        "answers": [],
        "orders": [],
        "practical": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def rerun_to(page):
    st.session_state.page = page
    st.rerun()


def section_head(number, title, subtitle):
    st.markdown(
        f'<div class="eyebrow">ETAPA {number} · CURSO 1</div><h1>{title}</h1>'
        f'<p style="color:#64748b;max-width:950px">{subtitle}</p>',
        unsafe_allow_html=True,
    )


def line_chart(x, curves, names, title, ytitle):
    colors = ["#0875d1", "#e98324", "#118566"]
    fig = go.Figure()
    for values, name, color in zip(curves, names, colors):
        fig.add_trace(go.Scatter(x=x, y=values, mode="lines+markers", name=name, line=dict(width=3, color=color)))
    fig.update_layout(height=390, title=title, xaxis_title="Frecuencia (Hz)", yaxis_title=ytitle,
                      paper_bgcolor="white", plot_bgcolor="white", margin=dict(l=25, r=20, t=55, b=25),
                      legend=dict(orientation="h", y=1.12))
    fig.update_xaxes(type="log", tickvals=list(x), gridcolor="#e9eef4")
    fig.update_yaxes(gridcolor="#e9eef4")
    return fig


def login():
    left, center, right = st.columns([1, 1.35, 1])
    with center:
        a, b = st.columns(2)
        a.image(str(LOGO_UC), use_container_width=True)
        b.image(str(LOGO_DECON), use_container_width=True)
        st.markdown(
            '<div class="hero"><span class="badge">DIPLOMADO EN ACÚSTICA EN LA EDIFICACIÓN</span>'
            '<h1>LAB AÉREO</h1><p>Curso 1 · Fundamentos del aislamiento acústico a ruido aéreo</p></div>',
            unsafe_allow_html=True,
        )
        role = st.radio("Tipo de acceso", ["Alumno", "Docente"], horizontal=True)
        with st.form("login_form"):
            if role == "Alumno":
                name = st.text_input("Nombre completo")
                email = st.text_input("Correo electrónico")
                access = st.form_submit_button("Ingresar como alumno", type="primary", use_container_width=True)
                if access:
                    if len(name.strip()) < 3 or "@" not in email:
                        st.error("Completa tu nombre y un correo válido.")
                    else:
                        st.session_state.update(authenticated=True, role="Alumno", name=name.strip(), email=email.strip())
                        st.rerun()
            else:
                email = st.text_input("Correo docente")
                password = st.text_input("Clave", type="password")
                access = st.form_submit_button("Ingresar como docente", type="primary", use_container_width=True)
                if access:
                    teacher = st.secrets.get("teacher", {})
                    expected_email = teacher.get("email", "maaraos@gmail.com")
                    expected_password = teacher.get("password", "docente123")
                    if email.strip().lower() == expected_email.lower() and password == expected_password:
                        st.session_state.update(authenticated=True, role="Docente", name="Marco Araos Barría", email=email.strip())
                        st.rerun()
                    else:
                        st.error("Credenciales docentes incorrectas.")
        st.caption("La clave de demostración local es docente123. En Streamlit Cloud debe configurarse mediante Secrets.")


def sidebar():
    with st.sidebar:
        c1, c2 = st.columns(2)
        c1.image(str(LOGO_UC), use_container_width=True)
        c2.image(str(LOGO_DECON), use_container_width=True)
        st.markdown("## LAB AÉREO")
        st.caption(f"{st.session_state.role.upper()} · {st.session_state.name}")
        labels = [f"{name} · {title}" if name != "Inicio" else "Inicio" for name, title in STAGES]
        current = next((i for i, item in enumerate(labels) if item.startswith(st.session_state.page)), 0)
        selected = st.radio("Ruta del curso", labels, index=current, label_visibility="collapsed")
        selected_page = "Inicio" if selected == "Inicio" else selected.split(" · ", 1)[0]
        if selected_page != st.session_state.page:
            st.session_state.page = selected_page
            st.rerun()
        stage = 0 if st.session_state.page == "Inicio" else int(st.session_state.page.split()[-1])
        st.progress(stage / 10)
        st.caption(f"Avance de contenidos: {stage}/10 etapas")
        if st.button("Cerrar sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def home():
    st.markdown(
        '<div class="hero"><span class="badge">CURSO 1 · 10 ETAPAS</span>'
        '<h1>Fundamentos del aislamiento acústico a ruido aéreo</h1>'
        '<p>Aprende la física, calcula, interpreta curvas e índices y termina tomando una decisión técnica y económica fundamentada.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Ruta de aprendizaje")
    cols = st.columns(2)
    for i, (name, title) in enumerate(STAGES[1:]):
        with cols[i % 2]:
            st.markdown(
                f'<div class="card stage"><div class="stage-number">{i+1:02}</div>'
                f'<div><b>{title}</b><br><small>{"Evaluación" if i == 9 else "Teoría, visualización y aplicación"}</small></div></div>',
                unsafe_allow_html=True,
            )
    st.info("La secuencia pedagógica alterna comprensión y aplicación. Las Etapas 6–7 trabajan transmisión; las Etapas 8–9, índices globales; la Etapa 10 integra todo.")


def stage1():
    section_head(1, "Sonido, frecuencia y longitud de onda", "Comprende qué se propaga, cómo se describe una onda y por qué su escala espacial cambia con la frecuencia.")
    speed = st.slider("Velocidad del sonido c (m/s)", 330, 350, 343)
    freq = st.select_slider("Frecuencia f (Hz)", options=[63, 125, 250, 500, 1000, 2000, 4000], value=500)
    wavelength = speed / freq
    c1, c2, c3 = st.columns(3)
    c1.metric("Frecuencia", f"{freq} Hz")
    c2.metric("Longitud de onda", f"{wavelength:.3f} m")
    c3.metric("Período", f"{1000/freq:.2f} ms")
    st.markdown('<div class="formula">λ = c / f</div>', unsafe_allow_html=True)
    x = np.linspace(0, max(wavelength * 2, .2), 400)
    y = np.sin(2 * np.pi * x / wavelength)
    fig = go.Figure(go.Scatter(x=x, y=y, line=dict(color="#0875d1", width=4)))
    fig.update_layout(height=300, xaxis_title="Distancia (m)", yaxis_title="Presión relativa", paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="concept"><b>Lectura física:</b> las bajas frecuencias poseen longitudes de onda grandes; por eso son difíciles de bloquear con soluciones livianas o pequeñas discontinuidades.</div>', unsafe_allow_html=True)


def stage2():
    section_head(2, "Decibeles y suma energética", "Trabaja con la escala logarítmica y evita sumar niveles como si fueran cantidades lineales.")
    levels = st.multiselect("Fuentes activas", [45, 50, 55, 60, 65, 70, 75, 80], default=[60, 60])
    total = 10 * math.log10(sum(10 ** (value / 10) for value in levels)) if levels else 0
    st.markdown(f'<div class="result"><small>NIVEL TOTAL</small><br><b>{total:.1f} dB</b><br><small>10 log₁₀ Σ10^(Li/10)</small></div>', unsafe_allow_html=True)
    if levels:
        df = pd.DataFrame({"Fuente": [f"Fuente {i+1}" for i in range(len(levels))], "Nivel (dB)": levels})
        st.bar_chart(df.set_index("Fuente"))
    c1, c2, c3 = st.columns(3)
    c1.info("Dos fuentes iguales → +3 dB")
    c2.info("Diferencia ≥10 dB → domina la mayor")
    c3.info("10 dB → factor 10 en intensidad")


def stage3():
    section_head(3, "Espectros y bandas de frecuencia", "Pasa de un nivel global a una lectura espectral capaz de revelar tonos, bandas dominantes y riesgos ocultos.")
    source = st.selectbox("Fuente", ["Voz", "Tránsito urbano", "Música con bajos", "Maquinaria tonal"])
    spectra = {
        "Voz": [49, 55, 61, 65, 62, 55],
        "Tránsito urbano": [76, 73, 69, 64, 59, 54],
        "Música con bajos": [80, 78, 70, 66, 63, 60],
        "Maquinaria tonal": [63, 81, 68, 62, 58, 54],
    }
    bands = [125, 250, 500, 1000, 2000, 4000]
    values = spectra[source]
    fig = go.Figure(go.Bar(x=[str(x) for x in bands], y=values, marker_color=["#0875d1" if value < max(values) else "#e98324" for value in values]))
    fig.update_layout(height=380, xaxis_title="Frecuencia central (Hz)", yaxis_title="Nivel (dB)", paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    critical = bands[int(np.argmax(values))]
    st.warning(f"Banda dominante: {critical} Hz. Una solución debe comprobarse especialmente en esta zona; un índice global aislado puede ocultarla.")


def stage4():
    section_head(4, "Absorción y reverberación", "Calcula el tiempo de reverberación y distingue el control de reflexiones internas del aislamiento entre recintos.")
    a, b, c = st.columns(3)
    length = a.number_input("Largo (m)", 2.0, 30.0, 6.0, .5)
    width = b.number_input("Ancho (m)", 2.0, 20.0, 5.0, .5)
    height = c.number_input("Alto (m)", 2.0, 8.0, 2.8, .1)
    absorption = st.slider("Absorción equivalente A (m² sabin)", 5.0, 150.0, 30.0, 1.0)
    volume = length * width * height
    rt = .161 * volume / absorption
    m1, m2, m3 = st.columns(3)
    m1.metric("Volumen", f"{volume:.1f} m³")
    m2.metric("Absorción equivalente", f"{absorption:.1f} m² sabin")
    m3.metric("T₆₀ estimado", f"{rt:.2f} s")
    st.markdown('<div class="formula">T₆₀ = 0,161 · V / A</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning"><b>No confundir:</b> reducir T₆₀ mejora la acústica interior, pero no significa automáticamente que el muro aísle más hacia el recinto vecino.</div>', unsafe_allow_html=True)


def stage5():
    section_head(5, "Aislamiento versus absorción", "Selecciona el tratamiento según el problema real: reflexión dentro del recinto o transmisión hacia otro recinto.")
    treatment = st.selectbox("Tratamiento", ["Espuma absorbente", "Cielo acústico", "Sellado de rendijas", "Segunda placa densa", "Tabique doble desacoplado"])
    effects = {
        "Espuma absorbente": (-35, 1, "Reduce reflexiones, pero casi no agrega masa."),
        "Cielo acústico": (-45, 0, "Controla reverberación dentro del recinto."),
        "Sellado de rendijas": (-4, 12, "Cierra fugas que pueden dominar la transmisión."),
        "Segunda placa densa": (-2, 5, "Aumenta masa superficial."),
        "Tabique doble desacoplado": (-8, 18, "Combina hojas, cámara, absorbente y desacoplamiento."),
    }
    rt_change, r_change, why = effects[treatment]
    c1, c2 = st.columns(2)
    c1.metric("Cambio estimado en reverberación", f"{rt_change}%")
    c2.metric("Cambio didáctico en aislamiento", f"+{r_change} dB")
    st.markdown(f'<div class="concept"><b>Interpretación:</b> {why}</div>', unsafe_allow_html=True)
    problem = st.radio("Problema observado", ["Hay demasiado eco dentro de la sala", "Se escucha al vecino a través del muro"])
    expected = "Absorción" if "eco" in problem else "Aislamiento"
    st.success(f"Familia de solución correcta: **{expected}**.")


def stage6():
    section_head(6, "Fundamentos físicos de la transmisión", "Relaciona masa superficial, coeficiente de transmisión, ley de masa, sistemas dobles y frecuencia crítica.")
    material = st.selectbox("Material", ["Yeso-cartón", "Vidrio", "Ladrillo", "Hormigón", "Acero"])
    densities = {"Yeso-cartón": 800, "Vidrio": 2500, "Ladrillo": 1800, "Hormigón": 2400, "Acero": 7850}
    thickness = st.slider("Espesor (mm)", 3.0, 200.0, 12.5, .5)
    mass = densities[material] * thickness / 1000
    curve = np.maximum(0, 20 * np.log10(mass * FREQS) - 47)
    doubled = np.maximum(0, 20 * np.log10(2 * mass * FREQS) - 47)
    c1, c2 = st.columns([.7, 1.3])
    with c1:
        st.metric("Masa superficial m′", f"{mass:.1f} kg/m²")
        st.latex(r"m'=\rho t")
        st.latex(r"R=20\log_{10}(m'f)-47")
        st.latex(r"\tau=10^{-R/10}")
        st.markdown('<div class="warning">La ley de masa es una región idealizada. Un sistema real presenta resonancia, coincidencia, puentes rígidos, juntas y transmisiones laterales.</div>', unsafe_allow_html=True)
    with c2:
        st.plotly_chart(line_chart(FREQS, [curve, doubled], ["Masa actual", "Masa duplicada"], "Ley de masa ideal", "R estimado (dB)"), use_container_width=True)
    st.markdown("### Sistemas de una y dos hojas")
    st.write("Una doble hoja no debe evaluarse como dos placas independientes sumadas en dB. Su respuesta depende de las masas, la profundidad de cámara, el material absorbente y el grado de desacoplamiento.")


def stage7():
    section_head(7, "Aplicación práctica de transmisión", "Calcula, interpreta y toma decisiones técnicas usando los fundamentos de la Etapa 6.")
    tabs = st.tabs(["Masa y ley de masa", "Energía transmitida", "Cerramiento compuesto", "Coincidencia"])
    with tabs[0]:
        density = st.number_input("Densidad (kg/m³)", 100.0, 8000.0, 800.0)
        thickness = st.number_input("Espesor (mm)", 1.0, 300.0, 15.0)
        frequency = st.selectbox("Frecuencia (Hz)", [125, 250, 500, 1000, 2000], index=2)
        mass = density * thickness / 1000
        r = max(0, 20 * math.log10(mass * frequency) - 47)
        st.metric("m′", f"{mass:.1f} kg/m²")
        st.metric("R ideal", f"{r:.1f} dB")
    with tabs[1]:
        r = st.slider("R (dB)", 10, 70, 40, key="tau_r")
        tau = 10 ** (-r / 10)
        st.metric("τ", f"{tau:.2e}")
        st.write(f"Atraviesa aproximadamente una parte de cada **{1/tau:,.0f}** de la energía incidente.")
    with tabs[2]:
        area = st.slider("Área total (m²)", 5.0, 50.0, 20.0)
        opening = st.slider("Área de puerta o ventana (%)", 0, 50, 15)
        wall_r = st.slider("R del muro (dB)", 30, 70, 55)
        opening_r = st.slider("R de la abertura (dB)", 10, 50, 28)
        ao = area * opening / 100
        aw = area - ao
        tau_global = (aw * 10 ** (-wall_r/10) + ao * 10 ** (-opening_r/10)) / area
        global_r = -10 * math.log10(tau_global)
        st.metric("R global del conjunto", f"{global_r:.1f} dB")
        st.warning("La abertura domina" if opening and opening_r < wall_r else "El cerramiento no contiene una abertura débil.")
    with tabs[3]:
        fc = st.slider("Frecuencia crítica estimada (Hz)", 100, 4000, 1600, 100)
        depth = st.slider("Profundidad del valle (dB)", 0, 15, 8)
        base = 28 + 10 * np.log2(FREQS / 100)
        valley = depth * np.exp(-((np.log(FREQS) - np.log(fc)) ** 2) / .12)
        st.plotly_chart(line_chart(FREQS, [base, base-valley], ["Ley de masa", "Respuesta real simplificada"], "Valle de coincidencia", "R (dB)"), use_container_width=True)
    st.info("Criterio de corrección: el procedimiento y la interpretación reciben puntaje parcial aunque exista un error aritmético menor.")


def calc_rw(curve):
    valid = []
    for rw in range(20, 81):
        ref = REF_RW + rw
        deviations = np.maximum(ref - curve, 0)
        if deviations.sum() <= 32:
            valid.append((rw, ref, deviations))
    return valid[-1] if valid else (20, REF_RW + 20, np.maximum(REF_RW + 20 - curve, 0))


def stage8():
    section_head(8, "Índices globales de aislamiento", "Convierte una curva por frecuencias en índices únicos y distingue laboratorio, terreno, recintos y fachadas.")
    base = st.slider("Nivel general de la curva", 35, 65, 48)
    low_penalty = st.slider("Debilidad en bajas frecuencias", 0, 15, 7)
    curve = base + REF_RW + 3 - low_penalty * np.exp(-((np.log(FREQS)-np.log(160))**2)/.7)
    rw, ref, dev = calc_rw(curve)
    c_value = int(round(np.clip(-np.mean(np.maximum((base + REF_RW) - curve, 0)) / 2, -8, 0)))
    ctr = int(round(np.clip(-low_penalty * .75, -15, 0)))
    st.plotly_chart(line_chart(FREQS, [curve, ref], ["Curva R(f)", "Referencia desplazada"], "Determinación didáctica de Rw", "R (dB)"), use_container_width=True)
    a, b, c, d = st.columns(4)
    a.metric("Rw", f"{rw} dB")
    b.metric("C", f"{c_value} dB")
    c.metric("Ctr", f"{ctr} dB")
    d.metric("Rw + Ctr", f"{rw+ctr} dB")
    st.caption(f"Suma de desviaciones desfavorables: {dev.sum():.1f} dB. Rw corresponde al valor de la curva de referencia desplazada en 500 Hz, no a un promedio.")
    data = [
        ["Rw", "Elemento", "Laboratorio ISO"],
        ["R'w", "Elemento instalado aparente", "Terreno"],
        ["DnT,w", "Diferencia estandarizada entre recintos", "Terreno"],
        ["D2m,nT,w", "Aislamiento de fachada", "Terreno"],
        ["STC", "Clase de transmisión", "ASTM"],
        ["ASTC", "STC aparente", "Terreno ASTM"],
        ["OITC", "Exterior a interior, énfasis en graves", "Fachadas ASTM"],
        ["CAC", "Transmisión por cielo y plenum", "Cielos suspendidos"],
    ]
    st.dataframe(pd.DataFrame(data, columns=["Índice", "Qué representa", "Contexto"]), hide_index=True, use_container_width=True)
    st.markdown('<div class="warning"><b>No son intercambiables:</b> Rw no es STC; Rw no es DnT,w; STC no es OITC; aislamiento no es absorción.</div>', unsafe_allow_html=True)


def stage9():
    section_head(9, "Aplicación práctica de los índices", "Calcula Rw, interpreta C y Ctr, compara soluciones y selecciona el índice correcto para cada problema.")
    tabs = st.tabs(["Rw interactivo", "C y Ctr", "Comparador", "Laboratorio o terreno", "Ficha técnica"])
    with tabs[0]:
        offset = st.slider("Desplazamiento de la referencia (Rw en 500 Hz)", 30, 60, 45)
        measured = np.array([27, 30, 33, 35, 38, 40, 42, 45, 46, 48, 49, 51, 52, 54, 55, 57])
        reference = REF_RW + offset
        deviations = np.maximum(reference - measured, 0)
        st.plotly_chart(line_chart(FREQS, [measured, reference], ["Medida", "Referencia"], "Desplaza la curva", "R (dB)"), use_container_width=True)
        st.metric("Suma de desviaciones", f"{deviations.sum():.0f} dB")
        st.success("Cumple el límite de 32 dB." if deviations.sum() <= 32 else "Aún no cumple: baja la curva de referencia.")
    with tabs[1]:
        rw = st.number_input("Rw", 20, 80, 52)
        c = st.number_input("C", -15, 0, -2)
        ctr = st.number_input("Ctr", -20, 0, -7)
        x, y = st.columns(2)
        x.metric("Rw + C", f"{rw+c} dB")
        y.metric("Rw + Ctr", f"{rw+ctr} dB")
    with tabs[2]:
        df = pd.DataFrame({
            "Indicador": ["Rw", "C", "Ctr", "Rw+C", "Rw+Ctr"],
            "Partición A": [50, -1, -8, 49, 42],
            "Partición B": [50, -3, -4, 47, 46],
        })
        st.dataframe(df, hide_index=True, use_container_width=True)
        source = st.radio("Fuente de diseño", ["Voz de oficina", "Tránsito con contenido grave"], horizontal=True)
        st.success("Recomendación: Partición A." if source == "Voz de oficina" else "Recomendación: Partición B. Tiene mejor Rw+Ctr.")
    with tabs[3]:
        situations = {
            "Tabique ensayado en laboratorio": "Rw",
            "Elemento instalado con transmisiones laterales": "R'w",
            "Entre recintos corregido por reverberación": "DnT,w",
            "Fachada medida a 2 m": "D2m,nT,w",
            "Fachada frente a transporte bajo ASTM": "OITC",
        }
        situation = st.selectbox("Situación", list(situations))
        st.info(f"Índice correspondiente: **{situations[situation]}**")
    with tabs[4]:
        st.markdown('<div class="card"><b>Tabique de doble estructura</b><br>Rw(C;Ctr)=56(−2;−8) dB<br>STC 57<br>Ensayo de laboratorio</div>', unsafe_allow_html=True)
        st.write("Interpretación: Rw=56 dB; Rw+C=54 dB; Rw+Ctr=48 dB. STC 57 pertenece a otro método y el resultado de laboratorio no garantiza el mismo desempeño en obra.")
        st.warning("Antes de especificar faltan: norma de ensayo, configuración, montantes, absorbente, sellos, dimensiones, laboratorio y número de informe.")


def reset_exam():
    st.session_state.update(exam_started=False, exam_done=False, exam_index=0, answers=[], orders=[], practical=None)


def practical_form():
    st.markdown("### Pregunta 30 · Caso práctico integrador y costo-beneficio")
    st.write("Un dormitorio colinda con una sala de máquinas dominante en 125, 250 y 500 Hz. Compara las alternativas:")
    table = pd.DataFrame({
        "Indicador": ["Rw", "C", "Ctr", "Rw+Ctr", "R 125 Hz", "R 250 Hz", "R 500 Hz", "Costo instalado", "Vida útil", "Instalación"],
        "Solución A": ["52 dB", "−2 dB", "−9 dB", "43 dB", "27 dB", "34 dB", "47 dB", "$1.800.000", "20 años", "Baja"],
        "Solución B": ["49 dB", "−1 dB", "−4 dB", "45 dB", "34 dB", "39 dB", "45 dB", "$2.100.000", "25 años", "Media"],
    })
    st.dataframe(table, hide_index=True, use_container_width=True)
    st.write("Recinto receptor: **V=50 m³** y **A=20 m² sabin**.")
    with st.form("practical_form"):
        rt = st.number_input("1. T₆₀ calculado (s)", 0.0, 5.0, 0.0, .01)
        critical = st.multiselect("2. Bandas críticas", [63, 125, 250, 500, 1000, 2000])
        cost_delta = st.number_input("3. Diferencia absoluta de costo (CLP)", 0, 2_000_000, 0, 50_000)
        cost_percent = st.number_input("4. Aumento porcentual de B respecto de A (%)", 0.0, 100.0, 0.0, .1)
        choice = st.radio("5. Recomendación", ["Solución A", "Solución B"])
        justification = st.text_area("6. Justificación técnica y económica", height=150, placeholder="Relaciona bandas críticas, Rw+Ctr, costo adicional, vida útil, instalación y meta de diseño.")
        submit = st.form_submit_button("Entregar pregunta práctica", type="primary", use_container_width=True)
    if submit:
        points = 0
        details = []
        if abs(rt - .4025) <= .03:
            points += 3; details.append("T60 correcto")
        if {125, 250, 500}.issubset(set(critical)):
            points += 2; details.append("bandas críticas correctas")
        if abs(cost_delta - 300_000) <= 50_000:
            points += 2; details.append("diferencia de costo correcta")
        if abs(cost_percent - 16.7) <= 1.0:
            points += 2; details.append("porcentaje correcto")
        text = justification.lower()
        if choice == "Solución B":
            points += 3
        if any(term in text for term in ["125", "250", "baja frecuencia", "bajas frecuencias"]):
            points += 2
        if any(term in text for term in ["ctr", "45 db", "43 db"]):
            points += 2
        if any(term in text for term in ["costo", "16,7", "16.7", "300"]):
            points += 2
        if any(term in text for term in ["vida útil", "25 años", "cumpl", "objetivo", "meta"]):
            points += 2
        st.session_state.practical = {"points": points, "choice": choice, "details": details, "justification": justification}
        st.session_state.exam_done = True
        st.session_state.exam_started = False
        st.rerun()


def teacher_exam_view():
    st.info("Vista docente: banco completo, alternativas correctas y pauta del caso práctico.")
    q = st.selectbox("Pregunta", range(29), format_func=lambda i: f"{i+1}. {QUESTIONS[i][1]}")
    section, question, options, correct, explanation = QUESTIONS[q]
    st.markdown(f"### {question}")
    for i, option in enumerate(options):
        st.write(("✅ " if i == correct else "○ ") + option)
    st.success(explanation)
    st.markdown("### Pauta pregunta 30")
    st.write("T60≈0,40 s; bandas 125, 250 y 500 Hz; diferencia $300.000; incremento 16,7%; recomendación B si la prioridad es controlar la sala de máquinas. La decisión definitiva debe comprobar el cumplimiento de una meta acústica.")


def stage10():
    section_head(10, "Evaluación final del Curso 1", "30 preguntas: 29 teórico-aplicadas y un caso práctico integrador con análisis costo-beneficio.")
    if st.session_state.role == "Docente" and not st.session_state.exam_started and not st.session_state.exam_done:
        with st.expander("Abrir vista docente de preguntas y pauta"):
            teacher_exam_view()
    if st.session_state.exam_done:
        conceptual = sum(answer == QUESTIONS[i][3] for i, answer in enumerate(st.session_state.answers))
        conceptual_points = conceptual / 29 * 80
        practical_points = (st.session_state.practical or {}).get("points", 0)
        total = conceptual_points + practical_points
        status = "APROBADO" if total >= 60 else "REPROBADO"
        st.markdown(f'<div class="result"><small>RESULTADO FINAL</small><br><b>{total:.1f}/100 · {status}</b><br><small>{conceptual}/29 respuestas correctas · Caso práctico {practical_points}/20</small></div>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        a.metric("Teoría aplicada", f"{conceptual_points:.1f}/80")
        b.metric("Caso práctico", f"{practical_points}/20")
        c.metric("Porcentaje", f"{total:.1f}%")
        sections = list(dict.fromkeys(q[0] for q in QUESTIONS))
        report = []
        for section in sections:
            idxs = [i for i, q in enumerate(QUESTIONS) if q[0] == section]
            hits = sum(st.session_state.answers[i] == QUESTIONS[i][3] for i in idxs)
            report.append([section, hits, len(idxs), 100 * hits / len(idxs)])
        st.dataframe(pd.DataFrame(report, columns=["Contenido", "Correctas", "Total", "Logro (%)"]),
                     hide_index=True, use_container_width=True)
        weakest = min(report, key=lambda row: row[3])
        st.info(f"Concepto prioritario para reforzar: **{weakest[0]}** ({weakest[3]:.0f}% de logro).")
        if st.button("Reiniciar evaluación", use_container_width=True):
            reset_exam(); st.rerun()
        return
    if not st.session_state.exam_started:
        st.markdown(
            '<div class="card"><b>Condiciones</b><br>60 minutos sugeridos · 100 puntos · 60% de aprobación · '
            '80 puntos en preguntas 1–29 · 20 puntos en el caso práctico.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Comenzar evaluación", type="primary", use_container_width=True):
            orders = []
            for _, _, options, _, _ in QUESTIONS:
                order = list(range(len(options))); random.shuffle(order); orders.append(order)
            st.session_state.update(exam_started=True, exam_index=0, answers=[], orders=orders, practical=None)
            st.rerun()
        return
    index = st.session_state.exam_index
    if index < 29:
        section, question, options, correct, explanation = QUESTIONS[index]
        order = st.session_state.orders[index]
        displayed = [options[i] for i in order]
        st.progress((index + 1) / 30)
        st.caption(f"Pregunta {index+1} de 30 · {section}")
        st.markdown(f"### {question}")
        choice = st.radio("Alternativas", range(len(displayed)), format_func=lambda i: displayed[i], index=None, key=f"exam_{index}")
        if st.button("Confirmar respuesta", type="primary", use_container_width=True):
            if choice is None:
                st.warning("Selecciona una alternativa.")
            else:
                st.session_state.answers.append(order[choice])
                st.session_state.exam_index += 1
                st.rerun()
    else:
        st.progress(1.0)
        practical_form()


init_state()
if not st.session_state.authenticated:
    login()
    st.stop()

sidebar()
page = st.session_state.page
if page == "Inicio": home()
elif page == "Etapa 1": stage1()
elif page == "Etapa 2": stage2()
elif page == "Etapa 3": stage3()
elif page == "Etapa 4": stage4()
elif page == "Etapa 5": stage5()
elif page == "Etapa 6": stage6()
elif page == "Etapa 7": stage7()
elif page == "Etapa 8": stage8()
elif page == "Etapa 9": stage9()
elif page == "Etapa 10": stage10()

st.markdown('<div class="footer">LAB AÉREO · Diplomado en Acústica en la Edificación · Docente Marco Araos Barría</div>', unsafe_allow_html=True)
