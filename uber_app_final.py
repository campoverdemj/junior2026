import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- CLASE DEL PDF ---
class UberPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, 'Uber', ln=True)
        self.ln(5)

def generar_pdf(row):
    pdf = UberPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Datos basados en tu plantilla [cite: 1, 2, 4, 5]
    pdf.cell(0, 10, f"Gracias por elegir Uber, {row.get('usuario', 'Mario')}", ln=True)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f"{row.get('fecha_texto', '16 de enero de 2026')}", ln=True)
    pdf.ln(10)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(100, 15, "Total", 0, 0)
    pdf.cell(0, 15, f"{row.get('total', '22.40')} US$", 0, 1, 'R')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 10, "Tarifa del viaje", 0, 0)
    pdf.cell(0, 10, f"{row.get('tarifa', '22.37')} US$", 0, 1, 'R') [cite: 6, 9]
    pdf.cell(100, 10, "Tiempo de espera", 0, 0)
    pdf.cell(0, 10, f"{row.get('espera', '0.03')} US$", 0, 1, 'R') [cite: 8, 10]
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, f"Viajaste con {row.get('conductor', 'VICTOR DAVID')}", ln=True) [cite: 17]
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"{row.get('servicio', 'UberX')} | {row.get('distancia', '53.1 kilómetros')}", ln=True) [cite: 18]
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ ---
st.title("📄 Reportes Individuales Uber")

archivo = st.file_uploader("Cargar CSV", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)
    
    # Selector de viaje
    st.subheader("Selecciona un viaje")
    indice = st.selectbox("ID del viaje", options=df.index)
    
    # DEFINICIÓN CRÍTICA DE LA VARIABLE
    viaje = df.loc[indice]
    
    # Ahora que 'viaje' existe, mostramos métricas 
    col1, col2 = st.columns(2)
    col1.metric("Total", f"{viaje.get('total', '0.00')} US$")
    col2.metric("Fecha", viaje.get('fecha_texto', 'N/A'))
    
    if st.button("Descargar PDF"):
        pdf_bytes = generar_pdf(viaje)
        st.download_button(
            label="Click para Guardar",
            data=pdf_bytes,
            file_name="Reporte_Uber.pdf",
            mime="application/pdf"
        )
else:
    st.info("Sube un archivo para comenzar.")
