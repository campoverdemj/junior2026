import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- CONFIGURACIÓN DE LA CLASE PDF (Estilo Uber) ---
class UberPDF(FPDF):
    def header(self):
        # Fuente Helvetica/Arial negrita para el logo
        self.set_font('Arial', 'B', 24)
        self.set_text_color(0, 0, 0)
        self.cell(0, 15, 'Uber', ln=True)
        self.ln(5)

def generar_pdf(row):
    # Inicializar PDF
    pdf = UberPDF()
    pdf.add_page()
    
    # Encabezado: Saludo y Fecha 
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Gracias por elegir Uber, {row.get('usuario', 'Usuario')}", ln=True) [cite: 1]
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f"{row.get('fecha_texto', 'Fecha no disponible')}", ln=True) [cite: 2]
    pdf.ln(10)

    # Bloque de Total Destacado [cite: 4, 5]
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(100, 15, "Total", 0, 0) [cite: 4]
    pdf.cell(0, 15, f"{row.get('total', '0.00')} US$", 0, 1, 'R') [cite: 5]
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    # Desglose Financiero [cite: 6, 8, 10]
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 10, "Tarifa del viaje", 0, 0) [cite: 6]
    pdf.cell(0, 10, f"{row.get('tarifa', '0.00')} US$", 0, 1, 'R') [cite: 6, 9]
    pdf.cell(100, 10, "Tiempo de espera", 0, 0) [cite: 8]
    pdf.cell(0, 10, f"{row.get('espera', '0.00')} US$", 0, 1, 'R') [cite: 10]
    
    # Detalles del Conductor y Vehículo 
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, f"Viajaste con {row.get('conductor', 'N/A')}", ln=True) [cite: 17]
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"{row.get('servicio', 'UberX')} | {row.get('distancia', '0 km')} | {row.get('duracion', '0 min')}", ln=True) [cite: 18]
    
    # Ruta Completa 
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, f"Inicio: {row.get('hora_inicio', '--:--')} | {row.get('origen', 'Origen')}") [cite: 19]
    pdf.ln(2)
    pdf.multi_cell(0, 5, f"Fin: {row.get('hora_fin', '--:--')} | {row.get('destino', 'Destino')}") [cite: 20]
    
    # Retorno de bytes (Corrección fpdf2)
    return pdf.output()

# --- INTERFAZ DE USUARIO EN STREAMLIT ---
st.set_page_config(page_title="Uber Report Studio", layout="wide")
st.title("🚗 Panel de Reportes Uber")
st.markdown("Transforma tus datos de viaje en recibos individuales profesionales.")

# Mapeo de columnas para compatibilidad
MAPEO_COLUMNAS = {
    'Fare Amount': 'total',
    'Begin Trip Time': 'fecha_texto',
    'Driver Name': 'conductor',
    'Drop-off Address': 'destino',
    'Begin Trip Address': 'origen'
}

archivo = st.file_uploader("Sube tu archivo CSV", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)
    df = df.rename(columns=MAPEO_COLUMNAS)
    
    # 1. Tabla de Previsualización
    st.subheader("📋 Vista Previa de los Datos")
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # 2. Selección de Viaje y Métricas
    col_sel, col_met = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Selección")
        indice = st.selectbox("Elija el índice del viaje", options=df.index)
        viaje = df.loc[indice]
    
    with col_met:
        st.subheader("Resumen Seleccionado")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total", f"{viaje.get('total', '0.00')} US$") [cite: 5]
        m2.metric("Distancia", viaje.get('distancia', 'N/A')) [cite: 18]
        m3.metric("Conductor", viaje.get('conductor', 'N/A')) [cite: 17]

    # 3. Botón de Generación y Descarga
    st.divider()
    if st.button("✨ Generar Reporte PDF"):
        try:
            pdf_bytes = generar_pdf(viaje)
            
            st.download_button(
                label="📥 Descargar Reporte PDF",
                data=pdf_bytes,
                file_name=f"Reporte_Uber_{viaje.get('fecha_texto', 'viaje')}.pdf",
                mime="application/pdf"
            )
            st.success("¡PDF generado con éxito!")
        except Exception as e:
            st.error(f"Hubo un error técnico: {e}")

else:
    st.info("👋 Por favor, sube tu archivo CSV para comenzar.")
