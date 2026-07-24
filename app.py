import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="LAB AÉREO | Curso 1", page_icon="🔊", layout="wide")
ROOT = Path(__file__).parent
FREQS = np.array([100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150])

st.markdown("""
<style>
:root{--navy:#07172b;--blue:#0967d2;--cyan:#17c3e6;--ink:#14243a;--muted:#60718a;--line:#dce6f2;--soft:#f3f8fd;--green:#0f9d78;--orange:#ef8b2c}
.stApp{background:#f5f8fc;color:var(--ink)} .block-container{padding-top:1.2rem;max-width:1280px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#06172b,#0a2b4d);color:white}
[data-testid="stSidebar"] *{color:white}.hero{background:linear-gradient(125deg,#07172b,#075da9 70%,#11a8cc);
color:white;border-radius:24px;padding:2rem 2.2rem;margin:.4rem 0 1.2rem;box-shadow:0 18px 42px #14395a25}
.hero h1{font-size:2.35rem;margin:.2rem 0}.hero p{max-width:850px;font-size:1.05rem}.tag{font-size:.73rem;font-weight:900;letter-spacing:.13em;color:#8ee9ff}
.card,.lesson,.answer{background:white;border:1px solid var(--line);border-radius:17px;padding:1.1rem 1.25rem;
box-shadow:0 6px 18px #17324d0b;margin:.55rem 0}.lesson{border-left:5px solid var(--blue)}
.formula{background:#07172b;color:white;border-radius:14px;padding:1rem 1.2rem;margin:.6rem 0;text-align:center;font-size:1.15rem}
.good{background:#eaf9f4;border-left:5px solid var(--green);padding:1rem;border-radius:12px}.warn{background:#fff5e8;border-left:5px solid var(--orange);padding:1rem;border-radius:12px}
.step{display:inline-flex;width:34px;height:34px;border-radius:50%;background:var(--blue);color:white;align-items:center;justify-content:center;font-weight:900}
.stage-title{font-size:1.7rem;font-weight:900;color:#092342;margin:.3rem 0}.muted{color:var(--muted)}
div[data-testid="stMetric"]{background:white;border:1px solid var(--line);padding:.7rem 1rem;border-radius:14px}
.scene{display:grid;grid-template-columns:1fr 80px 1fr;min-height:230px;border:1px solid #bcd0e4;border-radius:18px;overflow:hidden;background:white}
.room{display:flex;align-items:center;justify-content:center;font-size:3rem;position:relative;background:linear-gradient(#edf7ff,#fff)}
.wall{background:#25374a;display:flex;align-items:center;justify-content:center;color:white;font-size:.72rem;writing-mode:vertical-rl;font-weight:800}
.small{font-size:.85rem}.route{font-size:.8rem;padding:.25rem 0;color:#d7ecff}
</style>
""", unsafe_allow_html=True)

STAGES = [
("Etapa 0","Introducción y ruta del curso"),
("Etapa 1","Control del ruido: fuente, trayectoria y receptor"),
("Etapa 2","Aislamiento y absorción acústica"),
("Etapa 3","Aplicación: absorción, reverberación e inteligibilidad"),
("Etapa 4","Aislamiento y análisis costo-beneficio"),
("Etapa 5","Aplicación conceptual técnico-económica"),
("Etapa 6","Fundamentos físicos del aislamiento acústico"),
("Etapa 7","Aplicación práctica del aislamiento acústico"),
("Etapa 8","Índices de aislamiento acústico"),
("Etapa 9","Aplicación práctica de los índices"),
("Etapa 10","Evaluación final del Curso 1"),
]

def header(kicker,title,desc):
    st.markdown(f'<div class="hero"><span class="tag">{kicker}</span><h1>{title}</h1><p>{desc}</p></div>',unsafe_allow_html=True)

def lesson(title, text):
    st.markdown(f'<div class="lesson"><b>{title}</b><br><span class="muted">{text}</span></div>',unsafe_allow_html=True)

def check(key,q,options,correct,explanation):
    choice=st.radio(q,options,index=None,key=key)
    if st.button("Comprobar",key=f"b_{key}"):
        if choice==correct: st.success(f"Correcto. {explanation}")
        elif choice is None: st.warning("Selecciona una respuesta.")
        else: st.error(f"No es correcto. {explanation}")

def line_chart(x, series, title, ytitle):
    fig=go.Figure()
    for name,y in series: fig.add_trace(go.Scatter(x=x,y=y,name=name,mode="lines+markers"))
    fig.update_layout(title=title,xaxis_title="Frecuencia (Hz)",yaxis_title=ytitle,height=390,
                      template="plotly_white",margin=dict(l=20,r=20,t=55,b=20))
    fig.update_xaxes(type="log",tickvals=x)
    st.plotly_chart(fig,use_container_width=True)

def stage0():
    header("ETAPA 0 · BIENVENIDA","Aislamiento acústico a ruido aéreo",
           "Una ruta interactiva para comprender el fenómeno, calcular soluciones y decidir con criterio técnico y económico.")
    st.markdown("### ¿Qué aprenderás?")
    cols=st.columns(3)
    cards=[
      ("Comprender","Diferenciar fuente, trayectoria y receptor; absorción y aislamiento."),
      ("Experimentar","Modificar masa, frecuencia, absorción, costos y curvas de aislamiento."),
      ("Decidir","Elegir soluciones suficientes, justificadas y coherentes con la fuente real."),
    ]
    for c,(t,d) in zip(cols,cards):
        c.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
    st.markdown("### Ruta completa")
    for i,(n,t) in enumerate(STAGES[1:],1):
        st.markdown(f'<div class="route"><span class="step">{i}</span>&nbsp;&nbsp;<b>{t}</b></div>',unsafe_allow_html=True)
    st.info("La lógica de cada etapa es: materia → ejemplo → interacción → interpretación → ejercicio → retroalimentación.")

def stage1():
    header("ETAPA 1 · MATERIA + LABORATORIO","Control del ruido: fuente, trayectoria y receptor",
           "Antes de elegir un material hay que localizar dónde nace el ruido, cómo se propaga y a quién afecta.")
    lesson("Modelo de control","Fuente: genera la energía. Trayectoria: medio y vías de propagación. Receptor: persona, actividad o recinto afectado. Una solución robusta puede combinar los tres.")
    source=st.selectbox("Intervención en la fuente",["Sin intervención","Silenciador o encapsulado","Equipo de menor emisión"])
    path=st.selectbox("Intervención en la trayectoria",["Sin intervención","Sellado de fugas","Barrera pesada y estanca"])
    receiver=st.selectbox("Intervención en el receptor",["Sin intervención","Aumentar distancia","Reubicar/proteger receptor"])
    gains={"Sin intervención":0,"Silenciador o encapsulado":8,"Equipo de menor emisión":12,
           "Sellado de fugas":6,"Barrera pesada y estanca":15,"Aumentar distancia":5,"Reubicar/proteger receptor":10}
    total=gains[source]+gains[path]+gains[receiver]
    st.markdown(f'<div class="scene"><div class="room">🔊<small> FUENTE</small></div><div class="wall">TRAYECTORIA</div><div class="room">👂<small> RECEPTOR</small></div></div>',unsafe_allow_html=True)
    a,b,c=st.columns(3);a.metric("Nivel inicial","85 dB");b.metric("Reducción estimada",f"{total} dB");c.metric("Nivel resultante",f"{85-total} dB")
    st.markdown('<div class="warn">Las reducciones se suman aquí con fines didácticos. En un proyecto real deben evaluarse por bandas, vías dominantes y condiciones de montaje.</div>',unsafe_allow_html=True)
    check("e1","Una máquina afecta una oficina contigua. ¿Dónde actúa el muro separador?",["Fuente","Trayectoria","Receptor"],"Trayectoria","El muro se interpone en el camino de propagación.")

def stage2():
    header("ETAPA 2 · MATERIA + COMPARADOR","Aislamiento no es absorción",
           "Ambos conceptos controlan sonido, pero modifican fenómenos distintos.")
    lesson("Aislamiento acústico","Reduce la energía que atraviesa un elemento entre recintos. Se mejora con masa, estanqueidad, desacoplamiento y control de vías indirectas.")
    lesson("Absorción acústica","Reduce reflexiones dentro del mismo recinto. Se expresa mediante α entre 0 y 1 y modifica reverberación e inteligibilidad.")
    iso=st.slider("Mejora de aislamiento del muro (dB)",0,20,0)
    alpha=st.slider("Coeficiente de absorción del tratamiento, α",0.0,1.0,.10,.05)
    area=st.slider("Superficie tratada (m²)",0,80,0)
    V=150; Abase=25; A=Abase+alpha*area; rt=.161*V/A
    a,b=st.columns(2)
    a.metric("Nivel transmitido",f"{45-iso:.0f} dB",delta=f"{-iso} dB")
    b.metric("T₆₀ del receptor",f"{rt:.2f} s",delta=f"{rt-.161*V/Abase:+.2f} s")
    st.markdown('<div class="good">El tratamiento absorbente modifica T₆₀, pero no aumenta automáticamente el aislamiento del muro. La mejora del muro reduce transmisión, pero no corrige por sí sola el eco.</div>',unsafe_allow_html=True)
    check("e2","Pegar espuma liviana al muro medianero cuando se escucha al vecino actúa principalmente sobre:",["La absorción del recinto","La masa del muro","La transmisión flanqueante"],"La absorción del recinto","La espuma puede reducir reflexiones, pero suele aportar muy poco aislamiento.")

def stage3():
    header("ETAPA 3 · APLICACIÓN PRÁCTICA","Absorción, reverberación e inteligibilidad",
           "Diseña el acondicionamiento de un aula y observa cómo cambia el tiempo de reverberación.")
    st.markdown('<div class="formula">A = Σ(Sᵢ·αᵢ) &nbsp;&nbsp; | &nbsp;&nbsp; T₆₀ = 0,161·V/A</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    V=c1.number_input("Volumen (m³)",50,1000,220)
    base=c2.number_input("Absorción inicial (m² sabin)",5.,200.,28.)
    area=c3.number_input("Área nueva (m²)",0.,300.,55.)
    alpha=st.select_slider("α del material en 500 Hz",options=[0.05,.10,.20,.35,.50,.65,.80,.95],value=.80)
    A=base+area*alpha; T=.161*V/A; T0=.161*V/base
    a,b,c=st.columns(3);a.metric("A nueva",f"{A:.1f} m² sabin");b.metric("T₆₀ inicial",f"{T0:.2f} s");c.metric("T₆₀ final",f"{T:.2f} s",delta=f"{T-T0:+.2f} s")
    if T<=.8: st.success("Condición didáctica favorable para habla: decaimiento rápido y mejor claridad.")
    elif T<=1.2: st.warning("Condición intermedia. Puede requerir más absorción según volumen y uso.")
    else: st.error("Reverberación alta para una actividad centrada en la palabra.")
    check("e3","Si el volumen se mantiene y se duplica A, ¿qué ocurre con T₆₀?",["Se duplica","Se reduce aproximadamente a la mitad","No cambia"],"Se reduce aproximadamente a la mitad","Sabine muestra una relación inversa entre T₆₀ y A.")

def economic_inputs(prefix="eco"):
    names=["Solución A","Solución B","Solución C"]
    data=[]
    defaults=[(32,1200000,180000,8,900000),(40,1900000,220000,12,1150000),(47,3200000,260000,15,1250000)]
    for i,n in enumerate(names):
        with st.expander(n,expanded=i<2):
            d=defaults[i]
            r=st.number_input("Aislamiento esperado (dB)",20,70,d[0],key=f"{prefix}r{i}")
            inv=st.number_input("Inversión inicial ($)",0,20000000,d[1],step=100000,key=f"{prefix}i{i}")
            maint=st.number_input("Mantenimiento anual ($)",0,3000000,d[2],step=50000,key=f"{prefix}m{i}")
            life=st.number_input("Vida útil (años)",1,30,d[3],key=f"{prefix}l{i}")
            ben=st.number_input("Beneficio anual estimado ($)",0,10000000,d[4],step=50000,key=f"{prefix}b{i}")
        total=inv+maint*life; benefit=ben*life; roi=(benefit-total)/total*100 if total else 0
        payback=inv/(ben-maint) if ben>maint else math.inf
        data.append([n,r,inv,total,benefit,roi,payback])
    return pd.DataFrame(data,columns=["Solución","Aislamiento","Inversión","Costo ciclo","Beneficio acumulado","ROI","Payback"])

def stage4():
    header("ETAPA 4 · MATERIA + MODELO","Aislamiento acústico y costo-beneficio",
           "La mejor solución no es la de mayor número ni la más barata: es la que cumple la meta con un costo justificable.")
    lesson("Orden correcto de decisión","1) definir meta y espectro; 2) descartar lo que no cumple; 3) comparar costo del ciclo, vida útil, riesgo, ROI y recuperación; 4) revisar margen de seguridad.")
    st.markdown('<div class="formula">ROI = (beneficio acumulado − costo total) / costo total × 100</div>',unsafe_allow_html=True)
    st.markdown('<div class="formula">Payback = inversión inicial / (beneficio anual − mantenimiento anual)</div>',unsafe_allow_html=True)
    meta=st.slider("Meta de diseño (dB)",25,55,38)
    cost=st.slider("Costo de la solución ($)",500000,5000000,1800000,100000)
    benefit=st.slider("Beneficio anual ($)",100000,2000000,650000,50000)
    maint=st.slider("Mantenimiento anual ($)",0,500000,100000,25000)
    horizon=st.slider("Horizonte (años)",1,20,10)
    total=cost+maint*horizon; accum=benefit*horizon; roi=(accum-total)/total*100
    pay=cost/(benefit-maint) if benefit>maint else math.inf
    a,b,c=st.columns(3);a.metric("Costo del ciclo",f"${total:,.0f}");b.metric("ROI",f"{roi:.1f}%");c.metric("Recuperación",f"{pay:.1f} años" if math.isfinite(pay) else "No recupera")
    st.caption(f"La meta acústica seleccionada es {meta} dB. El cálculo económico solo tiene sentido si la solución la cumple.")

def stage5():
    header("ETAPA 5 · APLICACIÓN CONCEPTUAL","Decisión técnico-económica",
           "Compara alternativas, filtra por suficiencia acústica y encuentra el mejor compromiso.")
    target=st.slider("Objetivo acústico mínimo (dB)",25,55,38,key="target5")
    df=economic_inputs("s5")
    df["Cumple"]=df["Aislamiento"]>=target
    st.dataframe(df.style.format({"Inversión":"${:,.0f}","Costo ciclo":"${:,.0f}","Beneficio acumulado":"${:,.0f}","ROI":"{:.1f}%","Payback":"{:.1f} años"}),use_container_width=True,hide_index=True)
    feasible=df[df.Cumple]
    if feasible.empty: st.error("Ninguna alternativa cumple. No corresponde recomendar por precio o ROI.")
    else:
        best=feasible.loc[feasible["Costo ciclo"].idxmin()]
        st.success(f'Entre las alternativas suficientes, {best["Solución"]} tiene el menor costo del ciclo. La decisión final debe revisar además bandas críticas, montaje y riesgo.')
    check("e5","Una alternativa tiene excelente ROI, pero no alcanza la meta acústica. ¿Qué corresponde?",["Elegirla por su ROI","Descartarla o rediseñarla antes de comparar economía","Promediar ROI y dB"],"Descartarla o rediseñarla antes de comparar economía","La suficiencia técnica precede a la optimización económica.")

def mass_r(m,f): return 20*np.log10(np.maximum(m*f,1))-47

def stage6():
    header("ETAPA 6 · MATERIA + SIMULADORES","Fundamentos físicos del aislamiento acústico",
           "Masa, frecuencia, transmisión, coincidencia, sistemas dobles, estanqueidad y elementos débiles.")
    tabs=st.tabs(["Transmisión y R","Ley de masa","Coincidencia","Sistemas dobles","Elementos compuestos"])
    with tabs[0]:
        st.markdown('<div class="formula">τ = Wₜ/Wᵢ &nbsp;&nbsp; | &nbsp;&nbsp; R = 10 log₁₀(1/τ)</div>',unsafe_allow_html=True)
        R=st.slider("R (dB)",10,70,40,key="r6"); t=10**(-R/10)
        st.metric("Fracción de energía transmitida",f"{t:.8f} ({t*100:.6f} %)")
    with tabs[1]:
        m=st.slider("Masa superficial m′ (kg/m²)",5,150,25)
        curve=mass_r(m,FREQS); curve2=mass_r(2*m,FREQS)
        line_chart(FREQS,[("m′",curve),("2·m′",curve2)],"Ley de masa ideal","R (dB)")
        st.info("Duplicar masa o frecuencia aumenta aproximadamente 6 dB en la región ideal de ley de masa.")
    with tabs[2]:
        fc=st.slider("Frecuencia crítica estimada (Hz)",100,3150,800)
        ideal=mass_r(25,FREQS); dip=ideal-12*np.exp(-.5*(np.log(FREQS/fc)/.24)**2)
        line_chart(FREQS,[("Ley de masa ideal",ideal),("Con coincidencia",dip)],"Efecto didáctico de coincidencia","R (dB)")
        st.warning("Cerca de fᶜ el panel radia con mayor eficiencia y puede aparecer una caída de aislamiento.")
    with tabs[3]:
        gap=st.slider("Cámara (mm)",20,300,80); absorb=st.checkbox("Absorbente en cámara",True)
        gain=8+min(gap/30,8)+(5 if absorb else 0)
        st.metric("Mejora didáctica sobre hoja simple",f"{gain:.1f} dB")
        st.caption("El desempeño real depende de masas, rigidez de uniones, frecuencia masa–aire–masa y puentes estructurales.")
    with tabs[4]:
        wall=st.slider("R del muro (dB)",30,70,55); door=st.slider("R de puerta/ventana (dB)",15,50,28)
        share=st.slider("Porcentaje de área débil",1,40,15)/100
        tau=(1-share)*10**(-wall/10)+share*10**(-door/10); comp=-10*np.log10(tau)
        st.metric("R compuesto",f"{comp:.1f} dB")
        st.info("Los dB no se promedian: se combinan coeficientes de transmisión ponderados por superficie.")

def stage7():
    header("ETAPA 7 · APLICACIÓN PRÁCTICA","Diseño de aislamiento acústico",
           "Resuelve un caso completo por bandas, identifica el componente dominante y verifica la meta.")
    source=st.slider("Nivel de la fuente (dB)",70,110,92)
    target=st.slider("Nivel máximo admisible en receptor (dB)",25,60,40)
    m=st.slider("Masa superficial del cerramiento (kg/m²)",10,120,40,key="m7")
    fc=st.select_slider("Frecuencia crítica (Hz)",options=list(FREQS),value=800,key="fc7")
    weak=st.slider("R del elemento débil (dB)",18,50,32,key="weak7")
    share=st.slider("Área del elemento débil (%)",1,30,10,key="share7")/100
    wall=mass_r(m,FREQS)-10*np.exp(-.5*(np.log(FREQS/fc)/.28)**2)
    comp=-10*np.log10((1-share)*10**(-wall/10)+share*10**(-weak/10))
    received=source-comp
    line_chart(FREQS,[("R muro",wall),("R compuesto",comp),("Nivel receptor",received)],"Diagnóstico espectral","dB")
    worst=int(np.argmax(received)); ok=np.all(received<=target)
    a,b,c=st.columns(3);a.metric("Banda crítica",f"{FREQS[worst]} Hz");b.metric("Máximo receptor",f"{received[worst]:.1f} dB");c.metric("Meta","Cumple" if ok else "No cumple")
    st.markdown('<div class="warn">Prioriza el elemento o la banda que domina la transmisión. Reforzar una zona que ya aísla bien puede elevar el costo sin mejorar el resultado global.</div>',unsafe_allow_html=True)

REF=np.array([33,36,39,42,45,48,51,52,53,54,55,56,56,56,56,56])
def rw_from_curve(curve):
    best=None
    for shift in range(-30,31):
        ref=REF+shift; dev=np.maximum(ref-curve,0)
        if dev.sum()<=32: best=(int(ref[7]),ref,dev)
    return best

def stage8():
    header("ETAPA 8 · MATERIA + INTERPRETACIÓN","Índices de aislamiento acústico",
           "Los números únicos permiten comparar, pero deben corresponder al método, lugar y espectro del problema.")
    data=[
      ("R(f)","Reducción por banda","Laboratorio/curva"),
      ("Rᵥ","Reducción ponderada","Laboratorio ISO"),
      ("R′ᵥ","Reducción aparente","Terreno, incluye vías laterales"),
      ("DₙT,w","Diferencia estandarizada","Entre recintos, corregida por T"),
      ("D₂m,nT,w","Diferencia de fachada","Exterior a 2 m"),
      ("STC / ASTC","Clasificación ASTM","Laboratorio / terreno"),
      ("OITC","Exterior–interior","Transporte y bajas frecuencias"),
      ("CAC","Paso por cielo/plenum","Cielos suspendidos"),
    ]
    st.dataframe(pd.DataFrame(data,columns=["Indicador","Representa","Contexto"]),hide_index=True,use_container_width=True)
    st.markdown('<div class="formula">Rᵥ(C;Cₜᵣ) = 52(−2;−7) dB → Rᵥ+C = 50 dB | Rᵥ+Cₜᵣ = 45 dB</div>',unsafe_allow_html=True)
    source=st.selectbox("Fuente a evaluar",["Voz / actividades domésticas","Tránsito, buses o bajos","Fachada bajo criterio ASTM","Fuente tonal industrial"])
    recommendation={"Voz / actividades domésticas":"Revisar Rᵥ y Rᵥ+C.","Tránsito, buses o bajos":"Priorizar Rᵥ+Cₜᵣ y la curva grave.",
    "Fachada bajo criterio ASTM":"Revisar OITC además de STC.","Fuente tonal industrial":"La curva completa en la banda tonal es indispensable."}[source]
    st.info(recommendation)
    check("e8","Un tabique tiene Rᵥ=55 dB en laboratorio y R′ᵥ=47 dB en obra. ¿El laboratorio estaba necesariamente equivocado?",["Sí","No; montaje y vías laterales pueden explicar la diferencia"],"No; montaje y vías laterales pueden explicar la diferencia","R′ incorpora el comportamiento aparente de la construcción instalada.")

def stage9():
    header("ETAPA 9 · APLICACIÓN PRÁCTICA","Cálculo e interpretación de índices",
           "Desplaza la curva ISO, interpreta C y Cₜᵣ y selecciona la solución adecuada.")
    base=np.array([27,30,33,36,39,43,47,50,53,55,57,59,61,62,63,64],dtype=float)
    low=st.slider("Modificación en bajas frecuencias (100–315 Hz)",-12,12,0)
    mid=st.slider("Modificación en frecuencias medias (400–1250 Hz)",-8,8,0)
    curve=base.copy();curve[:6]+=low;curve[6:12]+=mid
    rw,ref,dev=rw_from_curve(curve)
    line_chart(FREQS,[("R medida",curve),("Referencia ajustada",ref)],"Cálculo gráfico de Rᵥ","dB")
    a,b,c=st.columns(3);a.metric("Rᵥ",f"{rw} dB");b.metric("Σ desviaciones",f"{dev.sum():.1f} dB");c.metric("Bandas desfavorables",int(np.sum(dev>0)))
    st.caption("Rᵥ es el valor de la curva de referencia desplazada en 500 Hz; no es el promedio ni necesariamente R(500).")
    st.markdown("### Comparador de selección")
    compare=pd.DataFrame({"Indicador":["Rᵥ","C","Cₜᵣ","Rᵥ+C","Rᵥ+Cₜᵣ"],"Partición A":[50,-1,-8,49,42],"Partición B":[50,-3,-4,47,46]})
    st.dataframe(compare,hide_index=True,use_container_width=True)
    use=st.radio("¿Para qué fuente eliges?",["Oficinas con voz","Fachada con tránsito"],horizontal=True)
    st.success("Partición A: mejor adaptación a voz." if use=="Oficinas con voz" else "Partición B: mejor resultado frente a tránsito y contenido grave.")

QUESTIONS=[
("La trayectoria incluye principalmente:",["La partición y sus fugas","Solo el oído","Solo la fuente"],0),
("La absorción reduce principalmente:",["La reverberación interior","La masa del muro","El ruido emitido"],0),
("A = Σ(S·α) representa:",["Absorción equivalente","Masa superficial","Costo del ciclo"],0),
("Sabine relaciona:",["V, A y T₆₀","R, STC y OITC","Costo, ROI y vida útil"],0),
("Si A aumenta con V constante, T₆₀:",["Disminuye","Aumenta","No cambia"],0),
("Antes de comparar ROI se debe:",["Verificar suficiencia acústica","Elegir lo más barato","Promediar dB"],0),
("ROI compara:",["Beneficio neto con costo total","R con frecuencia","Área con volumen"],0),
("Payback expresa:",["Tiempo de recuperación","Vida útil acústica","Frecuencia crítica"],0),
("El punto de equilibrio es:",["Donde el beneficio adicional deja de justificar el costo","El mayor R posible","El menor precio siempre"],0),
("Una solución que no cumple la meta:",["Se descarta o rediseña","Gana si tiene buen ROI","Se aprueba por vida útil"],0),
("τ es:",["Energía transmitida/incidente","R promedio","Absorción total"],0),
("R se expresa en:",["dB","sabin","segundos"],0),
("Duplicar masa en ley de masa aporta cerca de:",["6 dB","1 dB","20 dB"],0),
("La coincidencia puede producir:",["Una caída de R","Aislamiento infinito","Mayor absorción Sabine"],0),
("La lana en una cámara ayuda a:",["Amortiguar resonancias","Crear puentes rígidos","Eliminar sellos"],0),
("Una rendija puede:",["Dominar la transmisión","Mejorar R","Aumentar masa"],0),
("Los R de elementos compuestos se combinan mediante:",["τ ponderado por área","Promedio aritmético","Suma directa"],0),
("Transmisión flanqueante significa:",["Vía indirecta alrededor del separador","Reflexión interior","Medición a 2 m"],0),
("R(f) es:",["Resultado por banda","Un único índice","Costo por dB"],0),
("Rᵥ corresponde principalmente a:",["Laboratorio ISO","Terreno ASTM","Absorción"],0),
("R′ᵥ incorpora:",["Comportamiento aparente en obra","Solo el material aislado","ROI"],0),
("DₙT,w corrige mediante:",["Tiempo de reverberación","Costo de montaje","Masa"],0),
("D₂m,nT,w se usa en:",["Fachadas","Cielos plenums","ROI"],0),
("OITC es especialmente útil para:",["Ruido exterior de transporte","Eco interior","Impactos exclusivamente"],0),
("Cₜᵣ se asocia a:",["Tránsito y contenido grave","Solo agudos","Reverberación"],0),
("STC y Rᵥ:",["No tienen conversión fija universal","Siempre difieren en 2","Son idénticos"],0),
("CAC evalúa:",["Paso por cielos y plenums","Fachada a 2 m","Tiempo de recuperación"],0),
("Para una fuente tonal debe priorizarse:",["Curva por bandas","Solo el índice mayor","Solo el costo"],0),
("Rᵥ es:",["Valor de referencia ajustada en 500 Hz","Promedio de R","R medido siempre en 500 Hz"],0),
]

def stage10():
    header("ETAPA 10 · EVALUACIÓN FINAL","Evaluación práctica final del Curso 1",
           "30 preguntas: 29 teórico-aplicadas y un caso integrador con costo-beneficio.")
    if "exam_answers" not in st.session_state: st.session_state.exam_answers={}
    tab1,tab2=st.tabs(["Preguntas 1 a 29","Pregunta 30 · Caso práctico"])
    with tab1:
        qn=st.selectbox("Pregunta",range(29),format_func=lambda i:f"Pregunta {i+1}")
        q,opts,correct=QUESTIONS[qn]
        ans=st.radio(q,opts,index=None,key=f"q{qn}")
        if st.button("Guardar respuesta",key=f"save{qn}"):
            if ans is None: st.warning("Selecciona una alternativa.")
            else: st.session_state.exam_answers[qn]=opts.index(ans);st.success("Respuesta guardada.")
        st.progress(len(st.session_state.exam_answers)/29)
    with tab2:
        st.markdown("### Dormitorio junto a sala de máquinas")
        st.write("La fuente domina en 125, 250 y 500 Hz. Compara:")
        df=pd.DataFrame({
          "Indicador":["Rᵥ","Cₜᵣ","Rᵥ+Cₜᵣ","R en 125 Hz","R en 250 Hz","R en 500 Hz","Costo instalado","Vida útil"],
          "Solución A":["52 dB","−9 dB","43 dB","27 dB","34 dB","47 dB","$1.800.000","20 años"],
          "Solución B":["49 dB","−4 dB","45 dB","34 dB","39 dB","45 dB","$2.100.000","25 años"]})
        st.dataframe(df,hide_index=True,use_container_width=True)
        c1,c2=st.columns(2);V=c1.number_input("V (m³)",1.,500.,50.);A=c2.number_input("A (m² sabin)",1.,200.,20.)
        calc=st.number_input("Calcula T₆₀ (s)",0.,10.,0.,.01)
        diff=st.number_input("Diferencia de costo ($)",0,5000000,0,step=50000)
        pct=st.number_input("Incremento porcentual de B respecto de A (%)",0.,200.,0.,.1)
        bands=st.multiselect("Bandas críticas",[125,250,500,1000])
        choice=st.radio("Recomendación",["Solución A","Solución B"],index=None)
        justification=st.text_area("Justificación técnico-económica")
        if st.button("Finalizar y corregir evaluación",type="primary"):
            theory=sum(st.session_state.exam_answers.get(i)==QUESTIONS[i][2] for i in range(29))
            practical=0
            practical+=3 if abs(calc-.4025)<=.03 else 0
            practical+=2 if set(bands)=={125,250,500} else 0
            practical+=3 if choice=="Solución B" else 0
            practical+=2 if abs(diff-300000)<=10000 else 0
            practical+=2 if abs(pct-16.7)<=.5 else 0
            words=justification.lower()
            practical+=4 if all(k in words for k in ["costo","125"]) else 2 if justification.strip() else 0
            practical+=4 if any(k in words for k in ["vida útil","cumple","objetivo","grave","250"]) else 0
            total=theory/29*80+practical
            st.session_state.exam_result=(theory,practical,total)
    if "exam_result" in st.session_state:
        theory,practical,total=st.session_state.exam_result
        st.markdown(f'<div class="good"><b>Resultado: {total:.1f}/100</b><br>Teoría: {theory}/29 aciertos, ponderados a 80 puntos. Caso práctico: {practical}/20 puntos.<br>{"APROBADO" if total>=60 else "REQUIERE REFORZAMIENTO"}</div>',unsafe_allow_html=True)
        st.info("Respuesta esperada: T₆₀≈0,40 s; diferencia $300.000; incremento 16,7%; bandas 125, 250 y 500 Hz; Solución B por mejor respuesta grave, mejor Rᵥ+Cₜᵣ y mayor vida útil. Si ambas cumplieran holgadamente la meta, A podría ser suficiente.")

def login():
    uc=ROOT/"assets/logos/logo_uc.png";decon=ROOT/"assets/logos/logo_decon_uc.png"
    a,b=st.columns([1,1])
    if uc.exists(): a.image(str(uc),width=110)
    if decon.exists(): b.image(str(decon),width=180)
    header("DIPLOMADO EN ACÚSTICA EN LA EDIFICACIÓN","LAB AÉREO · Curso 1","Ingresa como alumno o docente para acceder a la plataforma.")
    role=st.radio("Perfil",["Alumno","Docente"],horizontal=True)
    name=st.text_input("Nombre completo")
    if role=="Alumno":
        rut=st.text_input("RUT o identificación");email=st.text_input("Correo")
        valid=name.strip() and rut.strip() and "@" in email
    else:
        password=st.text_input("Clave docente",type="password")
        try:
            teacher_password=str(st.secrets["teacher"]["password"])
        except (KeyError, FileNotFoundError):
            teacher_password="docente123"
        valid=name.strip() and password==teacher_password
    if st.button("Ingresar",type="primary",use_container_width=True):
        if valid: st.session_state.update(access=True,role=role,name=name);st.rerun()
        else: st.error("Completa correctamente los datos de acceso.")

if not st.session_state.get("access"):
    login();st.stop()

with st.sidebar:
    uc=ROOT/"assets/logos/logo_uc.png";decon=ROOT/"assets/logos/logo_decon_uc.png"
    if uc.exists(): st.image(str(uc),width=75)
    if decon.exists(): st.image(str(decon),width=130)
    st.markdown("## ◉ LAB AÉREO")
    st.caption("DIPLOMADO EN ACÚSTICA EN LA EDIFICACIÓN")
    st.markdown(f"**{st.session_state.name}**  \n{st.session_state.role}")
    labels=[f"{n} · {t}" for n,t in STAGES]
    selected=st.radio("Ruta de aprendizaje",labels,label_visibility="collapsed")
    if st.button("Cerrar sesión",use_container_width=True):
        st.session_state.clear();st.rerun()
    st.caption("Docente: Marco Araos Barría")

idx=labels.index(selected)
[stage0,stage1,stage2,stage3,stage4,stage5,stage6,stage7,stage8,stage9,stage10][idx]()
