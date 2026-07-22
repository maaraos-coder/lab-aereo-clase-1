import math
import random

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="LAB AÉREO | Clase 1", page_icon="🔊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--navy:#07172b;--blue:#0967d2;--cyan:#17c3e6;--ink:#14243a;--muted:#60718a;--line:#dce6f2;--soft:#f3f8fd;--green:#0f9d78;--orange:#ef8b2c}
html,body,[class*="css"]{font-family:Inter,sans-serif}.stApp{background:#f7f9fc;color:var(--ink)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#07172b,#0b2948);border-right:0}
[data-testid="stSidebar"] *{color:#e9f4ff}.block-container{padding-top:1.5rem;max-width:1400px}
h1,h2,h3{color:var(--ink);letter-spacing:-.03em}.eyebrow{font-size:.74rem;font-weight:800;letter-spacing:.13em;color:#0875d1;text-transform:uppercase}
.hero{padding:2rem 2.2rem;border-radius:24px;background:linear-gradient(125deg,#07172b 0%,#0a3b66 65%,#0875d1 100%);color:white;box-shadow:0 18px 50px #123b6822;margin-bottom:1.2rem}
.hero h1{color:white;margin:.3rem 0;font-size:2.35rem}.hero p{color:#d7e9f8;max-width:850px;margin:0}.tag{display:inline-block;background:#17c3e622;color:#77e8ff;border:1px solid #42cce755;border-radius:20px;padding:.3rem .7rem;font-size:.75rem;font-weight:700}
.card{background:white;border:1px solid var(--line);border-radius:18px;padding:1.25rem;height:100%;box-shadow:0 7px 25px #173b6810}.card h3{margin-top:.25rem}.number{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:10px;background:#e8f4ff;color:#0967d2;font-weight:800}
.concept{background:linear-gradient(135deg,#edf7ff,#f8fbff);border:1px solid #cfe5f6;border-left:5px solid #0b78d1;border-radius:14px;padding:1rem 1.2rem;margin:.8rem 0}
.result{background:#07172b;border-radius:16px;padding:1.1rem 1.3rem;color:#eef8ff}.result b{font-size:1.6rem;color:#67e5ff}.result small{color:#adc5d9}
.good{background:#e9f8f3;border:1px solid #afe2d2;color:#12644f;border-radius:13px;padding:.9rem 1rem}.warn{background:#fff5e8;border:1px solid #ffd5a6;color:#794411;border-radius:13px;padding:.9rem 1rem}
.room{min-height:230px;border-radius:18px;border:8px solid #d6e0e9;background:linear-gradient(180deg,#e8f6ff 0 72%,#d5c4a7 72%);position:relative;padding:1rem;text-align:center;overflow:hidden}.sound{font-size:2.5rem;margin-top:45px}.wall{height:230px;border-radius:14px;display:grid;place-items:center;background:repeating-linear-gradient(90deg,#8fa3b8 0,#8fa3b8 10px,#aebdca 10px,#aebdca 20px);color:white;font-weight:800}
.footer{color:#718198;font-size:.75rem;text-align:center;border-top:1px solid #dbe5ef;margin-top:2rem;padding:1rem}
div[data-testid="stMetric"]{background:white;border:1px solid var(--line);border-radius:15px;padding:1rem}button[kind="primary"]{background:#0875d1!important;border-radius:11px!important}
</style>
""", unsafe_allow_html=True)

MATERIALS = {
    "Yeso-cartón": 800, "Madera contrachapada": 600, "Vidrio": 2500,
    "Ladrillo": 1800, "Hormigón": 2400, "Acero": 7850,
}
ABS = {
    "Hormigón pintado": .03, "Vidrio": .05, "Yeso-cartón": .10,
    "Madera": .15, "Alfombra": .35, "Cortina pesada": .55,
    "Panel de lana mineral": .85, "Cielo acústico": .75,
}
FREQS = np.array([125, 250, 500, 1000, 2000, 4000])

if "score" not in st.session_state: st.session_state.score = 0
if "answered" not in st.session_state: st.session_state.answered = set()

def r_mass(mass, freq):
    return max(0.0, 20 * math.log10(max(mass * freq, 1e-9)) - 47)

def tau(r): return 10 ** (-r / 10)

def compound(parts):
    area = sum(a for _, a, _ in parts)
    tg = sum(a * tau(r) for _, a, r in parts) / area
    return -10 * math.log10(tg), tg

def plot_line(x, ys, names, ytitle, title=""):
    fig = go.Figure()
    colors = ["#0875d1", "#17c3e6", "#ef8b2c", "#0f9d78"]
    for y, name, color in zip(ys, names, colors):
        fig.add_trace(go.Scatter(x=x, y=y, name=name, mode="lines+markers", line=dict(width=3, color=color)))
    fig.update_layout(title=title, height=370, margin=dict(l=20,r=20,t=45,b=20), paper_bgcolor="white", plot_bgcolor="white", yaxis_title=ytitle, xaxis_title="Frecuencia (Hz)", legend=dict(orientation="h",y=1.12), hovermode="x unified")
    fig.update_xaxes(type="log", tickvals=list(x), gridcolor="#edf1f6")
    fig.update_yaxes(gridcolor="#edf1f6")
    return fig

def module_head(kicker, title, text):
    st.markdown(f'<div class="eyebrow">{kicker}</div><h1>{title}</h1><p style="color:#60718a;max-width:900px">{text}</p>', unsafe_allow_html=True)

def quiz(key, question, options, correct, explanation):
    st.markdown(f"#### {question}")
    choice = st.radio("Selecciona una respuesta", options, key=f"q_{key}", label_visibility="collapsed")
    if st.button("Comprobar", key=f"b_{key}"):
        if choice == correct:
            if key not in st.session_state.answered:
                st.session_state.score += 10; st.session_state.answered.add(key)
            st.success(f"Correcto. {explanation}")
        else: st.error(f"Aún no. {explanation}")

with st.sidebar:
    st.markdown("## ◉ LAB AÉREO")
    st.caption("DIPLOMADO EN ACÚSTICA · CLASE 1")
    st.markdown("---")
    pages = ["Inicio", "1 · Aislamiento vs. absorción", "2 · Transmisión sonora", "3 · Ley de masa", "4 · Absorción del recinto", "5 · Elementos compuestos", "6 · Decisión técnico-económica", "Desafíos", "Evaluación final"]
    page = st.radio("Ruta de aprendizaje", pages, label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"**Puntaje de práctica**  \
### {st.session_state.score} pts")
    st.progress(min(st.session_state.score / 50, 1.0))
    st.caption("Docente: Marco Araos Barría")

if page == "Inicio":
    st.markdown('<div class="hero"><span class="tag">CLASE 1 · LABORATORIO INTERACTIVO</span><h1>Aislamiento a ruido aéreo</h1><p>Experimenta cómo el sonido atraviesa los elementos constructivos. Aprende a distinguir absorción y aislamiento, interpreta los parámetros clave y toma decisiones acústicas con fundamento.</p></div>', unsafe_allow_html=True)
    st.markdown("### Tu recorrido de aprendizaje")
    cols = st.columns(3)
    items = [
        ("01","Distingue","Aislamiento y absorción acústica no resuelven el mismo problema."),
        ("02","Experimenta","Modifica niveles, masa, frecuencia, superficies y materiales."),
        ("03","Interpreta","Conecta cada resultado numérico con su significado físico."),
        ("04","Combina","Comprueba cómo puertas y ventanas dominan una partición."),
        ("05","Decide","Compara desempeño, costo, beneficio y suficiencia técnica."),
        ("06","Demuestra","Resuelve desafíos antes de avanzar a SONARA."),
    ]
    for i,(n,t,d) in enumerate(items):
        with cols[i%3]: st.markdown(f'<div class="card"><span class="number">{n}</span><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
        if i==2: st.write("")
    st.markdown("### El problema acústico")
    a,b,c = st.columns([1,1,1])
    with a: st.markdown('<div class="card"><div style="font-size:2.4rem">🔊</div><h3>Fuente</h3><p>Reducir emisión, vibración o potencia sonora.</p></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="card"><div style="font-size:2.4rem">▥</div><h3>Trayectoria</h3><p>Interponer, sellar, aumentar masa y desacoplar.</p></div>',unsafe_allow_html=True)
    with c: st.markdown('<div class="card"><div style="font-size:2.4rem">👂</div><h3>Receptor</h3><p>Aumentar distancia, proteger o reubicar al receptor.</p></div>',unsafe_allow_html=True)
    st.info("En esta clase nos concentraremos principalmente en la trayectoria: particiones verticales y horizontales frente al ruido transmitido por vía aérea.")

elif page.startswith("1 ·"):
    module_head("MÓDULO 1 · DISTINGUE", "Aislamiento vs. absorción", "Aplica tratamientos a una sala y observa qué variable modifica realmente cada solución.")
    treatments = {
        "Sin tratamiento": (0,0,"No cambia ni la reverberación ni la transmisión."),
        "Espuma acústica interior": (35,1,"Reduce reflexiones internas, pero casi no agrega masa ni sella la partición."),
        "Cielo absorbente": (45,0,"Mejora la acústica interna del recinto, no el aislamiento del muro separador."),
        "Sellos en puerta y rendijas": (5,12,"Cierra caminos de fuga. Puede mejorar mucho si existían aberturas."),
        "Segunda placa de alta densidad": (2,5,"Aumenta la masa superficial y mejora el aislamiento."),
        "Tabique doble desacoplado": (8,18,"Combina masa, cámara y desacoplamiento para reducir la transmisión."),
    }
    treatment = st.selectbox("Tratamiento a probar", list(treatments))
    base_rt = st.slider("Reverberación inicial, T₆₀ (s)", .4, 3.0, 1.8, .1)
    base_r = st.slider("Aislamiento inicial, R (dB)", 15, 55, 30)
    ar, dr, why = treatments[treatment]
    rt = base_rt * (1-ar/100); rr=base_r+dr
    c1,c2=st.columns([1.2,1])
    with c1:
        x,y=st.columns(2)
        with x: st.markdown(f'<div class="room"><div class="sound">🔊 )))</div><b>RECINTO EMISOR</b><br><small>T₆₀: {rt:.2f} s</small></div>',unsafe_allow_html=True)
        with y: st.markdown(f'<div class="room"><div class="sound">👂</div><b>RECINTO RECEPTOR</b><br><small>R: {rr:.0f} dB</small></div>',unsafe_allow_html=True)
    with c2:
        st.metric("Cambio en reverberación", f"{rt:.2f} s", f"-{ar}%")
        st.metric("Cambio en aislamiento", f"{rr:.0f} dB", f"+{dr} dB")
        st.markdown(f'<div class="concept"><b>¿Por qué?</b><br>{why}</div>',unsafe_allow_html=True)
    st.markdown("### Comprueba")
    quiz("foam", "Se instala espuma en el muro porque se oyen los vecinos. ¿Cuál es el error?", ["La espuma es demasiado delgada", "Se está tratando absorción cuando el problema es aislamiento", "Falta pintar la espuma"], "Se está tratando absorción cuando el problema es aislamiento", "La espuma puede reducir el eco dentro de la sala, pero normalmente aporta muy poco aislamiento entre recintos.")

elif page.startswith("2 ·"):
    module_head("MÓDULO 2 · EXPERIMENTA", "Transmisión sonora", "Relaciona el nivel emisor, el índice de reducción sonora y la fracción de energía que atraviesa la partición.")
    c1,c2=st.columns([.8,1.2])
    with c1:
        l1=st.slider("Nivel en recinto emisor L₁ (dB)",50,110,85)
        r=st.slider("Índice de reducción R (dB)",10,70,40)
        freq=st.select_slider("Frecuencia de observación (Hz)",options=list(FREQS),value=500)
        l2=l1-r; t=tau(r)
        st.markdown(f'<div class="result"><small>NIVEL RECEPTOR SIMPLIFICADO</small><br><b>{l2:.1f} dB</b><br><small>L₂ = L₁ − R</small></div>',unsafe_allow_html=True)
        st.metric("Coeficiente de transmisión τ", f"{t:.2e}")
        st.caption("Relación didáctica simplificada; en mediciones normalizadas intervienen área, absorción y condiciones de campo.")
    with c2:
        fig=go.Figure(go.Sankey(node=dict(label=[f"Incidente\n{l1} dB","Reflejada / disipada",f"Transmitida\n{l2} dB"],color=["#0875d1","#aec3d6","#17c3e6"]),link=dict(source=[0,0],target=[1,2],value=[max(1-t,0),max(t,.00001)],color=["#bfd0dd","#17c3e6"])))
        fig.update_layout(height=330,margin=dict(l=10,r=10,t=20,b=10),paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
        denom=1/t
        st.markdown(f'<div class="concept">Con <b>R = {r} dB</b>, atraviesa cerca de <b>1 parte de cada {denom:,.0f}</b> de la energía sonora incidente.</div>',unsafe_allow_html=True)
    quiz("tau", "Si R aumenta 10 dB, ¿qué ocurre con la energía transmitida?", ["Se reduce a la mitad", "Se reduce a una décima parte", "No cambia"], "Se reduce a una décima parte", "Cada aumento de 10 dB en R reduce τ por un factor 10.")

elif page.startswith("3 ·"):
    module_head("MÓDULO 3 · EXPLORA", "Ley de masa", "Observa cómo la masa superficial y la frecuencia influyen en el aislamiento ideal de un elemento simple.")
    c1,c2=st.columns([.8,1.4])
    with c1:
        mat=st.selectbox("Material",list(MATERIALS)+["Personalizado"])
        density=st.number_input("Densidad (kg/m³)",100,10000,MATERIALS.get(mat,1000),50,disabled=mat!="Personalizado") if mat=="Personalizado" else MATERIALS[mat]
        thick=st.slider("Espesor (mm)",3.0,200.0,12.5,.5)
        mass=density*thick/1000
        st.metric("Masa superficial m′",f"{mass:.1f} kg/m²")
        st.markdown(r"$$R=20\log_{10}(m'f)-47$$")
        st.warning("Modelo ideal didáctico. No representa resonancias, coincidencia, uniones ni transmisión flanqueante.")
    with c2:
        curve=np.array([r_mass(mass,f) for f in FREQS]); doubled=np.array([r_mass(mass*2,f) for f in FREQS])
        st.plotly_chart(plot_line(FREQS,[curve,doubled],["Masa actual","Masa duplicada"],"R estimado (dB)","Efecto de duplicar la masa"),use_container_width=True)
        delta=np.mean(doubled-curve)
        a,b,c=st.columns(3);a.metric("R a 500 Hz",f"{r_mass(mass,500):.1f} dB");b.metric("Al duplicar masa",f"+{delta:.1f} dB");c.metric("R a 1 kHz",f"{r_mass(mass,1000):.1f} dB")
    quiz("mass", "Según la ley de masa ideal, ¿cuánto aumenta R al duplicar la masa superficial?", ["Aproximadamente 3 dB", "Aproximadamente 6 dB", "Aproximadamente 10 dB"], "Aproximadamente 6 dB", "20·log₁₀(2) ≈ 6 dB. En una construcción real puede diferir.")

elif page.startswith("4 ·"):
    module_head("MÓDULO 4 · CONSTRUYE", "Absorción del recinto", "Dimensiona una sala, asigna materiales y calcula su absorción equivalente y tiempo de reverberación estimado.")
    c1,c2=st.columns([.8,1.3])
    with c1:
        L=st.number_input("Largo (m)",2.0,30.0,6.0,.5); W=st.number_input("Ancho (m)",2.0,20.0,5.0,.5); H=st.number_input("Alto (m)",2.0,8.0,2.8,.1)
        floor=st.selectbox("Piso",list(ABS),index=4); ceiling=st.selectbox("Cielo",list(ABS),index=7); walls=st.selectbox("Muros",list(ABS),index=2)
        s_floor=L*W; s_walls=2*(L+W)*H
        parts=[("Piso",s_floor,ABS[floor]),("Cielo",s_floor,ABS[ceiling]),("Muros",s_walls,ABS[walls])]
        A=sum(s*a for _,s,a in parts); V=L*W*H; rt=.161*V/A
    with c2:
        df=pd.DataFrame(parts,columns=["Superficie","Área (m²)","α"]);df["Absorción (sabines)"]=df["Área (m²)"]*df["α"]
        st.dataframe(df.style.format({"Área (m²)":"{:.1f}","α":"{:.2f}","Absorción (sabines)":"{:.1f}"}),use_container_width=True,hide_index=True)
        a,b,c=st.columns(3);a.metric("Volumen",f"{V:.1f} m³");b.metric("Absorción total",f"{A:.1f} sabines");c.metric("T₆₀ Sabine",f"{rt:.2f} s")
        fig=go.Figure(go.Bar(x=df["Superficie"],y=df["Absorción (sabines)"],marker_color=["#0875d1","#17c3e6","#ef8b2c"],text=df["Absorción (sabines)"].round(1),textposition="outside"));fig.update_layout(height=300,margin=dict(l=20,r=20,t=20,b=20),yaxis_title="Sabines",paper_bgcolor="white",plot_bgcolor="white");st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="concept"><b>Interpretación:</b> aumentar A reduce el tiempo de reverberación, pero no implica automáticamente aumentar el aislamiento hacia otro recinto.</div>',unsafe_allow_html=True)

elif page.startswith("5 ·"):
    module_head("MÓDULO 5 · COMBINA", "Elementos compuestos", "Descubre por qué una pequeña superficie débil puede controlar el desempeño de toda una partición.")
    c1,c2=st.columns([.8,1.3])
    with c1:
        total=st.slider("Superficie total (m²)",5.0,50.0,20.0,.5); opening=st.slider("Porcentaje de puerta/ventana",0,50,20)
        rw_wall=st.slider("R del muro (dB)",30,70,55);rw_open=st.slider("R de puerta/ventana (dB)",10,50,28)
        ao=total*opening/100; aw=total-ao
        rg,tg=compound([("Muro",aw,rw_wall),("Abertura",ao,rw_open)]) if ao else (rw_wall,tau(rw_wall))
        st.markdown(f'<div class="result"><small>AISLAMIENTO GLOBAL</small><br><b>{rg:.1f} dB</b><br><small>Pérdida respecto del muro: {rw_wall-rg:.1f} dB</small></div>',unsafe_allow_html=True)
    with c2:
        fig=go.Figure(go.Bar(x=["Muro solo","Abertura sola","Conjunto"],y=[rw_wall,rw_open,rg],marker_color=["#0875d1","#ef8b2c","#17c3e6"],text=[f"{rw_wall} dB",f"{rw_open} dB",f"{rg:.1f} dB"],textposition="outside"));fig.update_layout(height=340,yaxis_title="R (dB)",yaxis_range=[0,max(rw_wall+10,70)],paper_bgcolor="white",plot_bgcolor="white",margin=dict(l=20,r=20,t=30,b=20));st.plotly_chart(fig,use_container_width=True)
        if opening and rw_open<rw_wall: st.markdown(f'<div class="warn"><b>Elemento dominante: puerta/ventana.</b><br>Aunque ocupa {opening}% del área, transmite aproximadamente {ao*tau(rw_open)/(aw*tau(rw_wall)+ao*tau(rw_open))*100:.1f}% de la energía que atraviesa el conjunto.</div>',unsafe_allow_html=True)
    quiz("weak", "¿Qué conviene mejorar primero en un muro R=55 dB con ventana R=28 dB?", ["Agregar más masa al muro", "Mejorar la ventana y sus sellos", "Agregar panel absorbente al cielo"], "Mejorar la ventana y sus sellos", "La transmisión se concentra en el elemento de menor aislamiento y en sus encuentros.")

elif page.startswith("6 ·"):
    module_head("MÓDULO 6 · DECIDE", "Decisión técnico-económica", "Compara alternativas por atenuación, costo por dB, retorno y cumplimiento del objetivo de diseño.")
    target=st.slider("Atenuación mínima requerida (dB)",15,45,30)
    data=pd.DataFrame({"Solución":["Sellado de fugas","Refuerzo de placa","Tabique doble","Sistema premium"],"Atenuación (dB)":[12,25,35,42],"Costo (CLP)":[280000,720000,1200000,2400000],"Beneficio estimado (CLP)":[500000,950000,1700000,2600000]})
    data["Costo por dB"]=data["Costo (CLP)"]/data["Atenuación (dB)"];data["ROI (%)"]=(data["Beneficio estimado (CLP)"]-data["Costo (CLP)"])/data["Costo (CLP)"]*100;data["Cumple"]=np.where(data["Atenuación (dB)"]>=target,"Sí","No")
    edited=st.data_editor(data,column_config={"Costo (CLP)":st.column_config.NumberColumn(format="$%d"),"Beneficio estimado (CLP)":st.column_config.NumberColumn(format="$%d"),"Costo por dB":st.column_config.NumberColumn(format="$%d/dB"),"ROI (%)":st.column_config.NumberColumn(format="%.1f%%")},disabled=["Costo por dB","ROI (%)","Cumple"],hide_index=True,use_container_width=True)
    feasible=edited[edited["Atenuación (dB)"]>=target]
    if len(feasible):
        best=feasible.loc[feasible["Costo (CLP)"].idxmin()]
        st.success(f"Alternativa de menor costo que cumple {target} dB: **{best['Solución']}**, con un costo de ${best['Costo (CLP)']:,.0f} CLP.")
    else: st.warning("Ninguna alternativa cumple el objetivo definido.")
    fig=go.Figure();fig.add_trace(go.Scatter(x=edited["Atenuación (dB)"],y=edited["Costo (CLP)"],mode="markers+text",text=edited["Solución"],textposition="top center",marker=dict(size=18,color=edited["ROI (%)"],colorscale="Teal",showscale=True,colorbar=dict(title="ROI %"))));fig.add_vline(x=target,line_dash="dash",line_color="#ef8b2c",annotation_text="Objetivo");fig.update_layout(height=380,xaxis_title="Atenuación (dB)",yaxis_title="Costo (CLP)",paper_bgcolor="white",plot_bgcolor="white",margin=dict(l=20,r=20,t=30,b=20));st.plotly_chart(fig,use_container_width=True)

elif page == "Desafíos":
    module_head("PRÁCTICA · RETROALIMENTACIÓN", "Desafíos de aplicación", "Resuelve los conceptos centrales de la clase. Cada respuesta correcta suma 10 puntos una sola vez.")
    quiz("d1","Un muro separa recintos con L₁=85 dB y L₂=50 dB. ¿Cuál es R simplificado?",["25 dB","35 dB","45 dB"],"35 dB","R = L₁ − L₂ = 35 dB.")
    quiz("d2","Para R=40 dB, ¿cuál es aproximadamente τ?",["0,01","0,001","0,0001"],"0,0001","τ=10⁻⁴: atraviesa una diezmilésima parte de la energía.")
    quiz("d3","¿Qué aporta lana mineral dentro de la cámara de un tabique doble?",["Solo aumenta la masa","Amortigua resonancias de la cámara","Sella automáticamente las juntas"],"Amortigua resonancias de la cámara","Disipa energía dentro de la cavidad; no reemplaza masa, desacoplamiento ni sellado.")
    quiz("d4","Hay buen aislamiento directo, pero aún se oye ruido. ¿Qué sospechas?",["Transmisión flanqueante","Exceso de absorción","Demasiada masa"],"Transmisión flanqueante","El sonido puede rodear la partición por losas, fachadas, ductos, encuentros o instalaciones.")

else:
    module_head("EVALUACIÓN · CIERRE DE CLASE", "Caso final: sala de reuniones", "Integra los fundamentos antes de pasar a la Clase 2 y usar SONARA en la prueba final conjunta.")
    st.markdown('<div class="card"><b>Situación profesional</b><p>Una sala de reuniones genera 82 dB. En la oficina vecina se requiere no superar 42 dB. La separación tiene 18 m²: un muro de 50 dB y una puerta de 28 dB que ocupa 2 m². Además, la sala presenta exceso de reverberación.</p></div>',unsafe_allow_html=True)
    rg,_=compound([("Muro",16,50),("Puerta",2,28)]); receiver=82-rg; needed=82-42
    st.write("")
    c1,c2,c3=st.columns(3);c1.metric("R requerido",f"{needed:.0f} dB");c2.metric("R global actual",f"{rg:.1f} dB");c3.metric("Nivel receptor estimado",f"{receiver:.1f} dB",f"{receiver-42:.1f} dB sobre meta")
    st.markdown("### Diseña tu intervención")
    isolation=st.selectbox("Medida principal de aislamiento",["Agregar espuma al muro","Mejorar puerta y sellos a R=40 dB","Agregar cortinas interiores"])
    absorption=st.selectbox("Medida para la reverberación",["Paneles absorbentes interiores","Aumentar espesor del muro","Cambiar la puerta por una metálica sin sellos"])
    reasoning=st.text_area("Justifica brevemente por qué cada medida resuelve un fenómeno diferente",placeholder="La primera medida... La segunda medida...")
    if st.button("Evaluar solución",type="primary"):
        points=0; feedback=[]
        if isolation=="Mejorar puerta y sellos a R=40 dB": points+=50;feedback.append("✓ Identificaste correctamente el elemento débil.")
        else: feedback.append("✗ La medida elegida no mejora de forma relevante la ruta de transmisión dominante.")
        if absorption=="Paneles absorbentes interiores": points+=30;feedback.append("✓ Elegiste absorción para controlar la reverberación.")
        else: feedback.append("✗ Para la reverberación se necesita absorción dentro del recinto.")
        if len(reasoning.strip())>=40: points+=20;feedback.append("✓ Incluiste una justificación técnica.")
        else: feedback.append("○ Amplía la justificación distinguiendo transmisión y reflexiones internas.")
        newrg,_=compound([("Muro",16,50),("Puerta",2,40)])
        st.markdown(f'<div class="result"><small>RESULTADO</small><br><b>{points}/100 puntos</b><br><small>{"<br>".join(feedback)}</small></div>',unsafe_allow_html=True)
        if isolation=="Mejorar puerta y sellos a R=40 dB": st.info(f"Con la mejora, el conjunto alcanzaría aproximadamente R={newrg:.1f} dB y el receptor {82-newrg:.1f} dB. La meta queda prácticamente alcanzada; el diseño real debe verificarse con método normalizado.")
        if points>=80: st.balloons();st.success("Preparación lograda. Ya puedes avanzar a la siguiente clase.")

st.markdown('<div class="footer">LAB AÉREO · Diplomado en Acústica en la Edificación · Herramienta didáctica basada en modelos simplificados</div>',unsafe_allow_html=True)
