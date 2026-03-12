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
    
    # Datos del encabezado 
    pdf.cell(0, 10, f"Gracias por elegir Uber, {row.get('usuario', 'Mario')}", ln=True)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f"{row.get('fecha_texto', '16 de enero de 2026')}", ln=True)
    pdf.ln(10)
    
    # Bloque de Total 
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(100, 15, "Total", 0, 0)
    pdf.cell(0, 15, f"{row.get('total', '22.40')} US$", 0, 1, 'R')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    # Desglose Financiero [cite: 6, 8, 10]
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 10, "Tarifa del viaje", 0, 0)
    pdf.cell(0, 10, f"{row.get('tarifa', '22.37')} US$", 0, 1, 'R')
    pdf.cell(100, 10, "Tiempo de espera", 0, 0)
    pdf.cell(0, 10, f"{row.get('espera', '0.03')} US$", 0, 1, 'R')
    
    # Detalles del Servicio [cite: 17, 18]
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, f"Viajaste con {row.get('conductor', 'VICTOR DAVID')}", ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"{row.get('servicio', 'UberX')} | {row.get('distancia', '53.1 kilómetros')} | {row.get('duracion', '1 hora 5 min')}", ln=True)
    
    # Ruta 
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, f"Inicio: {row.get('hora_inicio', '09:44')} | {row.get('origen', 'Guayaquil')}")
    pdf.ln(2)
    pdf.multi_cell(0, 5, f"Fin: {row.get('hora_fin', '10:49')} | {row.get('destino', 'Virgen de Fátima')}")
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="Uber Report Tool", layout="wide")
st.title("🚗 Panel de Reportes Uber")

archivo = st.file_uploader("Sube tu historial de viajes (CSV)", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)
    
    # 1. Tabla de Previsualización General
    st.subheader("📋 Vista Previa de Datos Cargados")
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # 2. Selección y Métricas Individuales
    col_sel, col_met = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Selección")
        indice = st.selectbox("Elija el ID del viaje", options=df.index)
        viaje_seleccionado = df.loc[indice]
    
    with col_met:
        st.subheader("Resumen del Viaje")
        m1, m2, m3 = st.columns(3)
        # Se extraen datos reales del CSV basado en tu formato [cite: 4, 5, 18]
        m1.metric("Total", f"{viaje_seleccionado.get('total', '0.00')} US$")
        m2.metric("Distancia", viaje_seleccionado.get('distancia', '0 km'))
        m3.metric("Servicio", viaje_seleccionado.get('servicio', 'UberX'))

    # 3. Generación de Reporte
    st.divider()
    if st.button("✨ Generar Reporte PDF Individual"):
        try:
            pdf_bytes = generar_pdf(viaje_seleccionado)
            nombre_archivo = f"Reporte_Uber_{viaje_seleccionado.get('fecha_texto', 'viaje')}.pdf"
            
            st.download_button(
                label="📥 Descargar Reporte PDF",
                data=pdf_bytes,
                file_name=nombre_archivo,
                mime="application/pdf"
            )
            st.success("¡El reporte está listo para descargar!")
        except Exception as e:
            st.error(f"Error al generar el PDF: {e}")
else:
    st.info("👋 Bienvenido. Por favor sube tu archivo CSV para comenzar a generar reportes.")
