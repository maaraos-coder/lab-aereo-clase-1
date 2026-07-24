# LAB AÉREO · Curso 1

Aplicación interactiva del Curso 1 del Diplomado en Acústica en la Edificación.

## Ejecución

```bash
pip install -r requirements.txt
streamlit run app.py
```

La clave docente de respaldo local es `docente123`. En producción se recomienda definir:

```toml
[teacher]
password = "una-clave-segura"
```

en `.streamlit/secrets.toml`.
