import streamlit as st
import requests
import json
import os
from docx import Document

# Configuración de página
st.set_page_config(page_title="Generador de Minutas VENG", page_icon="✨", layout="wide")

# ESTILOS CSS PREMIUM (Marketinera Dark)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

    /* Aplicar fuente Inter a todo Streamlit */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Ocultar elementos por defecto de Streamlit para un look más limpio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Contenedor principal y fondo general */
    .stApp {
        background-color: #041424;
        background-image: radial-gradient(circle at 50% 0%, #0a2a4a 0%, #041424 60%);
    }

    /* Estilización del título principal */
    h1 {
        color: #ffffff;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    
    /* Subtítulo premium */
    .subtitle {
        color: #8ab4f8;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    /* Efectos Glassmorphism - usamos clases genéricas para interceptar contenedores */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
    }

    /* Botones principales con efecto Glow */
    .stButton > button {
        background: linear-gradient(135deg, #2c83c3 0%, #1a5c8e 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(44, 131, 195, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(44, 131, 195, 0.6);
        background: linear-gradient(135deg, #3aa0eb 0%, #2071af 100%);
        color: white;
        border: none;
    }

    /* File uploader estilizado (Dropzone ampliado) */
    .css-1n76uvr, .st-emotion-cache-1erjvxc {
        border-radius: 16px;
        border: 2px dashed rgba(44, 131, 195, 0.5);
        background-color: rgba(10, 34, 56, 0.4);
        padding: 3rem 1rem !important;
        transition: all 0.3s ease;
    }
    .css-1n76uvr:hover, .st-emotion-cache-1erjvxc:hover {
        border-color: #3aa0eb;
        background-color: rgba(10, 34, 56, 0.8);
        box-shadow: 0 0 15px rgba(58, 160, 235, 0.2);
    }
    
    /* Animación Fade In Up para resultados */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Aplicar animación al contenedor de descarga y tabs */
    .stTabs, div[data-testid="stVerticalBlock"] > div:last-child {
        animation: fadeInUp 0.5s ease-out;
    }

    /* Cajas de alerta estilizadas */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #2c83c3;
    }
    
    /* Paneles de vista previa */
    .stMarkdown pre {
        background-color: #020a12 !important;
        border-radius: 8px;
        border: 1px solid #1a365d;
    }
</style>
""", unsafe_allow_html=True)

# CABECERA PREMIUM VENG
col_logo, col_text = st.columns([1, 4])

with col_logo:
    logo_path = "logo_veng.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        # Placeholder si no subió el logo aún
        st.markdown(
            "<div style='background-color:#0a2238; border-radius:8px; padding:20px; text-align:center; border: 1px dashed #2c83c3; color:#2c83c3;'>"
            "🚀<br><small>Falta logo_veng.png</small></div>", 
            unsafe_allow_html=True
        )

with col_text:
    st.markdown("<h1>Generador de Minutas Automático</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Generación automatizada de minutas a partir de tus archivos de reunión.<br>Subí tu transcripción y obtené un resumen estructurado al instante.</p>", unsafe_allow_html=True)

st.markdown("---")

def extract_text(file):
    """Extrae el contenido de texto dependiendo de la extensión e implementa optimización de tokens."""
    import re
    
    if file.name.endswith(".docx"):
        doc = Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        texto = "\n".join(full_text)
    else: # asume .txt
        texto = file.getvalue().decode("utf-8")
        
    # --- OPTIMIZACIÓN EXTREMA DE TOKENS IA ---
    # 1. Eliminar marcas de tiempo como [00:15:20] o 00:15:20 que saturan transcripciones largas
    texto = re.sub(r'\[?\b\d{1,2}:\d{2}(?::\d{2})?\b\]?', '', texto)
    # 2. Reconstrucción semántica (Unir subtítulos rotos)
    # Si una línea termina sin puntuación natural, se asume que la oración sigue y le borra el salto de línea.
    texto = re.sub(r'([^.,?!:;>\]\-])\n+', r'\1 ', texto)
    # 3. Eliminar tabulaciones y espacios múltiples innecesarios
    texto = re.sub(r'[ \t]+', ' ', texto)
    # 4. Eliminar saltos de línea excesivos (más de 2 vacíos se reducen a 2)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    
    return texto.strip()

# Inicializar estados si no existen
if 'minuta_texto' not in st.session_state:
    st.session_state['minuta_texto'] = ""
if 'minuta_json' not in st.session_state:
    st.session_state['minuta_json'] = ""

# Selector de archivos
uploaded_file = st.file_uploader("Buscá tu archivo en tu equipo:", type=["txt", "docx"])

if uploaded_file:
    # Pre-procesamiento local
    with st.status("Procesando archivo localmente...", expanded=False) as status:
        try:
            text_content = extract_text(uploaded_file)
            status.update(label=f"✅ Archivo listo: {uploaded_file.name}", state="complete")
        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}")
            text_content = None

    if text_content:
        st.markdown("### ⚙️ Opciones de Procesamiento", unsafe_allow_html=True)
        modo_procesamiento = st.radio(
            "Elige el motor de Inteligencia Artificial según la longitud de tu archivo:",
            options=["🟢 Rápido (Reuniones Cortas - hasta ~15 pág)", "🟡 Extenso (Chunking Anti-Límites - más de 15 pág)"],
            index=0,
            help="El modo Extenso divide reuniones gigantes en partes para no romper los límites de tokens de la IA, pero puede demorar un par de minutos."
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Espacio para los botones
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generar minutas con IA", use_container_width=True):
                with st.spinner("La IA está analizando tu reunión... (el modo Extenso puede demorar unos minutos)"):
                    try:
                        # Determinamos la ruta de n8n correcta según tu selección
                        url_webhook = "http://n8n:5678/webhook/minutas"
                        tiempo_espera = 120 # 2 minutos por defecto
                        
                        if "Extenso" in modo_procesamiento:
                            url_webhook = "http://n8n:5678/webhook/minutas-chunking"
                            tiempo_espera = 600 # 10 minutos para archivos grandes

                        # Enviamos el texto directamente a n8n
                        payload = {"meeting_text": text_content}
                        
                        response = requests.post(
                            url_webhook,
                            json=payload,
                            timeout=tiempo_espera
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Normalizar respuesta (n8n a veces manda una lista)
                            if isinstance(data, list) and len(data) > 0:
                                data = data[0]
                            
                            if isinstance(data, dict):
                                # CASO 1: Tenemos las claves esperadas (minuta, json)
                                if 'minuta' in data and 'json' in data:
                                    st.session_state['minuta_texto'] = data.get('minuta', '')
                                    st.session_state['minuta_json'] = json.dumps(data.get('json', {}), indent=4, ensure_ascii=False)
                                
                                # CASO 2: La respuesta ES el json estructurado directamente (como en la captura del usuario)
                                elif 'tipo_reunion' in data or 'participantes' in data:
                                    # Intentamos mostrar algo como minuta
                                    st.session_state['minuta_texto'] = f"Minuta generada con éxito.\nParticipantes: {', '.join(data.get('participantes', []))}"
                                    st.session_state['minuta_json'] = json.dumps(data, indent=4, ensure_ascii=False)
                                
                                # CASO 3: Respuesta genérica
                                else:
                                    st.session_state['minuta_texto'] = data.get('text') or data.get('minutas_texto') or str(data)
                                    st.session_state['minuta_json'] = json.dumps(data, indent=4, ensure_ascii=False)
                                
                                # Verificación final antes de mostrar
                                if st.session_state['minuta_texto']:
                                    st.success("¡Minutas generadas!")
                                else:
                                    st.warning("La IA generó una respuesta pero no pudimos extraer el texto de la minuta.")
                            else:
                                st.error("La respuesta de la IA no tiene el formato esperado (se esperaba un Diccionario).")
                        else:
                            st.error(f"Error en el servidor de IA (n8n): {response.status_code} - {response.text}")
                    except requests.exceptions.Timeout:
                        st.error("⚠️ **Tiempo de espera superado (Timeout)**: El servidor n8n demoró más de 120 segundos en responder. El archivo podría estar procesándose en segundo plano en n8n.")
                    except json.JSONDecodeError:
                        st.error("⚠️ **Respuesta no válida**: El servidor n8n devolvió un formato incorrecto (no es JSON válido).")
                        with st.expander("Ver respuesta cruda enviada por n8n (para depurar)"):
                            st.text(response.text)
                    except Exception as e:
                        st.error(f"Error de conexión: {type(e).__name__} - {str(e)}")

        # Mostrar resultado y permitir descarga si existe contenido
        if st.session_state.get('minuta_texto'):
            st.markdown("---")
            st.markdown("### ✨ Resultados del Análisis")
            
            # Usar Tabs para ocultar la complejidad
            tab1, tab2 = st.tabs(["📄 Vista Previa de la Minuta", "💻 Estructura de Datos (JSON)"])
            
            with tab1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.write(st.session_state['minuta_texto'])
                st.markdown("</div>", unsafe_allow_html=True)
                
            with tab2:
                st.markdown("Revisa el JSON directo que generó la IA:")
                try:
                    js = json.loads(st.session_state['minuta_json'])
                    st.json(js)
                except Exception:
                    st.code(st.session_state['minuta_json'], language="json")
            
            # Botón de descarga destacado en su propio contenedor
            st.markdown("<br>", unsafe_allow_html=True)
            _, col_btn, _ = st.columns([1, 2, 1])
            with col_btn:
                st.download_button(
                    label="📥 Descargar Documento Oficial (.json)",
                    data=st.session_state['minuta_json'],
                    file_name=f"minuta_{uploaded_file.name.split('.')[0]}.json",
                    mime="application/json",
                    use_container_width=True
                )
else:
    # Limpiamos el estado si se quita el archivo
    st.session_state['minuta_texto'] = ""
    st.session_state['minuta_json'] = ""