import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- CONFIGURACIÓN DE LA CLASE PDF ---
class UberPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'Uber', ln=True)
        self.ln(5)

def generar_pdf(row):
    pdf = UberPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Datos basados en tu plantilla
    pdf.cell(0, 10, f"Gracias por elegir Uber, {row.get('usuario', 'Mario')}", ln=True)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f"{row.get('fecha_texto', '16 de enero de 2026')}", ln=True)
    pdf.ln(10)
    
    # Total
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(100, 15, "Total", 0, 0)
    pdf.cell(0, 15, f"{row.get('total', '0.00')} US$", 0, 1, 'R')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    # Desglose
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 10, "Tarifa del viaje", 0, 0)
    pdf.cell(0, 10, f"{row.get('tarifa', '0.00')} US$", 0, 1, 'R')
    pdf.cell(100, 10, "Tiempo de espera", 0, 0)
    pdf.cell(0, 10, f"{row.get('espera', '0.00')} US$", 0, 1, 'R')
    
    # Detalles
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, f"Viajaste con {row.get('conductor', 'N/A')}", ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"{row.get('servicio', 'UberX')} | {row.get('distancia', '0 km')} | {row.get('duracion', '0 min')}", ln=True)
    
    # Ruta
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, f"Inicio: {row.get('hora_inicio', '--:--')} | {row.get('origen', 'N/A')}")
    pdf.ln(2)
    pdf.multi_cell(0, 5, f"Fin: {row.get('hora_fin', '--:--')} | {row.get('destino', 'N/A')}")
    
    return pdf.output()

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Uber Generator", layout="wide")
st.title("🚗 Generador de Reportes Uber")

archivo = st.file_uploader("Sube tu archivo CSV", type="csv")

if archivo is not None:
    # 1. Cargar datos
    df = pd.read_csv(archivo)
    
    # 2. Mostrar tabla
    st.subheader("📋 Vista Previa de Viajes")
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # 3. Selección y Métricas (Todo dentro del IF)
    col_sel, col_met = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Selección")
        indice = st.selectbox("Elija el índice del viaje", options=df.index)
        # AQUÍ se define la variable 'viaje' que causaba el error
        viaje = df.loc[indice]
    
    with col_met:
        st.subheader("Resumen del Viaje")
        m1, m2, m3 = st.columns(3)
        # Estas líneas ya no darán NameError porque están indentadas correctamente
        m1.metric("Total", f"{viaje.get('total', '0.00')} US$")
        m2.metric("Distancia", viaje.get('distancia', 'N/A'))
        m3.metric("Fecha", viaje.get('fecha_texto', 'N/A'))

    # 4. Botón de descarga
    st.divider()
    if st.button("Generar PDF"):
        pdf_bytes = generar_pdf(viaje)
        st.download_button(
            label="📥 Descargar ahora",
            data=pdf_bytes,
            file_name=f"Uber_{indice}.pdf",
            mime="application/pdf"
        )
else:
    # Si no hay archivo, mostramos este mensaje amigable
    st.info("👋 Por favor, carga un archivo CSV para ver los viajes.")
