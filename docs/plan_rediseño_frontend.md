# Rediseño de Interfaz "Marketinera" y Dark Mode para VENG

## Descripción del Objetivo
El objetivo es transformar el frontend actual (Streamlit) en una versión visualmente atractiva, orientada al marketing ("marketinera"), con un diseño premium en modo oscuro e incorporando el branding de la empresa VENG. Esto incluye el uso de los colores institucionales y una presentación más elegante estilo plataforma SaaS.

## Cambios Propuestos

### `frontend_ui/.streamlit/config.toml`
Crear este archivo para definir el tema global de Streamlit:
- `primaryColor="#2c83c3"` (Azul VENG)
- `backgroundColor="#0A1118"` (Azul noche premium)
- `secondaryBackgroundColor="#111B27"` (Para paneles y cards)
- `textColor="#F0F4F8"` (Blanco suave para mejor lectura)
- `font="sans serif"`

### `frontend_ui/app.py`
- **Inyección de CSS**: Agregar código CSS personalizado (`st.markdown`) para estilizar la aplicación, dándole bordes redondeados, sombras sutiles (glow) a los botones, y un layout más moderno.
- **Layout de Cabecera**: Reemplazar la barra de título simple por una estructura en columnas que muestre el logo de VENG alineado a la izquierda y el título a la derecha o debajo con una tipografía premium.
- **Micro-copy**: Mejorar los textos para que suenen más corporativos/marketineros (ej: "Sube la transcripción de tu reunión y deja que nuestra IA haga el trabajo pesado").
- **Carga de Logo**: Implementar lectura condicional del archivo `logo_veng.png` para asegurar que el app no falle si el archivo aún no fue guardado.
