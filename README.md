# LAB AÉREO — Clase 1

Laboratorio Interactivo de Aislamiento a Ruido Aéreo para el Diplomado en Acústica en la Edificación.

## Ejecutar

### Windows (forma sencilla)

Haz doble clic en `INICIAR_APP.bat`. La primera ejecución instala automáticamente los componentes necesarios y luego abre la aplicación en el navegador.

### Terminal

```bash
pip install -r requirements.txt
streamlit run app.py
```

La aplicación incluye:

- acceso inicial independiente para alumnos y docentes;
- una clase interactiva completa de 4 horas (240 minutos);
- tres aplicaciones conceptuales basadas en los ejercicios del PowerPoint;
- dibujos, ecuaciones rasterizadas y animaciones didácticas visibles tanto
  para alumnos como para el docente;
- 20 actividades formativas, dos intentos y 50 puntos;
- seis laboratorios interactivos de profundización;
- decisión técnico-económica con costo por dB, ROI y payback;
- evaluación final independiente de 40 puntos;
- vista docente e informe PDF del intento final.

Al subir el proyecto a GitHub, incluye la carpeta `assets/course_visuals`
completa. La aplicación la necesita para mostrar las ilustraciones y ecuaciones.

## Configurar el acceso docente en Streamlit Cloud

En **Manage app → Settings → Secrets**, agrega:

```toml
[teacher]
email = "maaraos@gmail.com"
password = "TU_CLAVE_DOCENTE_SEGURA"
```

El correo y la clave no deben escribirse en `app.py` ni subirse a GitHub.

Los cálculos son didácticos y no sustituyen una predicción normalizada, un ensayo de laboratorio ni una medición en terreno.
