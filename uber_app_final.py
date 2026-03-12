import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# --- LÓGICA DEL REPORTE PDF ---
class UberPDF(FPDF):
    def header(self):
        # Dibujamos un logo de texto simple (estilo Uber) [cite: 1]
        self.set_font('Arial', 'B', 24)
        self.set_text_color(0, 0, 0)
        self.cell(0, 15, 'Uber', ln=True)
        self.ln(5)

def generar_pdf(row):
    pdf = UberPDF()
    pdf.add_page()
    
    # Encabezado: Saludo y Fecha [cite: 1, 2]
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Gracias por elegir Uber, {row.get('usuario', 'Usuario')}", ln=True)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f"{row.get('fecha_texto', 'Fecha no disponible')}", ln=True)
    pdf.ln(10)

    # Bloque de Total [cite: 4, 5]
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(100, 15, "Total", 0, 0)
    pdf.cell(0, 15, f"{row.get('total', '0.00')} US$", 0, 1, 'R')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    # Desglose (Tarifa y Espera) [cite: 6, 8, 10]
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 10, "Tarifa del viaje", 0, 0)
    pdf.cell(0, 10, f"{row.get('tarifa', '0.00')} US$", 0, 1, 'R')
    pdf.cell(100, 10, "Tiempo de espera", 0, 0)
    pdf.cell(0, 10, f"{row.get('espera', '0.00')} US$", 0, 1, 'R')
    
    # Información del Conductor y Servicio [cite: 17, 18]
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, f"Viajaste con {row.get('conductor', 'N/A')}", ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"{row.get('servicio', 'UberX')} | {row.get('distancia', '0 km')} | {row.get('duracion', '0 min')}", ln=True)
    
    # Ruta (Origen y Destino) [cite: 19, 20]
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, f"Inicio: {row.get('hora_inicio', '--:--')} | {row.get('origen', 'Dirección de origen')}")
    pdf.ln(2)
    pdf.multi_cell(0, 5, f"Fin: {row.get('hora_fin', '--:--')} | {row.get('destino', 'Dirección de destino')}")
    
    # Output como bytes para Streamlit
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Uber Report Studio", layout="centered")

st.title("📄 Generador de Reportes Uber")
st.write("Sube tu historial para generar recibos individuales basados en tu formato.")

# Diccionario de mapeo (Traduce columnas automáticas a las de tu plantilla)
MAPEO_COLUMNAS = {
    'Fare Amount': 'total',
    'Begin Trip Time': 'fecha_texto',
    'Driver Name': 'conductor',
    'Drop-off Address': 'destino',
    'Begin Trip Address': 'origen'
}

archivo = st.file_uploader("Cargar archivo CSV", type="csv")

if archivo:
    df = pd.read_csv(archivo)
    df = df.rename(columns=MAPEO_COLUMNAS)
    st.success("Archivo cargado con éxito.")
    
    # Selector de viaje
    seleccion = st.selectbox(
        "¿Qué viaje quieres reportar?",
        options=df.index,
        format_func=lambda x: f"Viaje {df.iloc[x].get('fecha_texto', 'Sin Fecha')} - {df.iloc[x].get('total', '0.00')} US$"
    )
    
    # AQUÍ SE DEFINE LA VARIABLE 'viaje'
    viaje = df.loc[seleccion]
    
    # Vista previa (Métricas)
    col1, col2 = st.columns(2)
    with col1:
        # Usamos .get() para evitar NameError si la columna falta
        st.metric("Total", f"{viaje.get('total', '0.00')} US$") [cite: 4, 5]
    with col2:
        st.metric("Distancia", viaje.get('distancia', 'N/A')) [cite: 18]

    # Botón de Generación
    if st.button("Generar PDF Individual"):
        pdf_data = generar_pdf(viaje)
        st.download_button(
            label="📥 Descargar Reporte PDF",
            data=pdf_data,
            file_name=f"Uber_Reporte_{viaje.get('fecha_texto', 'viaje')}.pdf",
            mime="application/pdf"
        )
