import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# --- CONFIGURACIÓN DE LA CLASE PDF (IDÉNTICO A LA PLANTILLA) ---
class UberPDF(FPDF):
    def header(self):
        # Título Uber en negrita grande
        self.set_font('helvetica', 'B', 26)
        self.set_text_color(0, 0, 0)
        self.cell(0, 15, 'Uber', ln=True)
        self.ln(2)

def generar_pdf(row):
    pdf = UberPDF()
    pdf.add_page()
    
    # 1. Saludo y Fecha
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Gracias por elegir Uber, {row.get('usuario', 'Usuario')}", ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"{row.get('fecha_texto', 'Fecha no disponible')}", ln=True)
    pdf.cell(0, 6, "Esperamos que hayas disfrutado tu viaje de esta tarde.", ln=True)
    pdf.ln(10)

    # 2. Bloque de Total (Línea destacada)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(140, 12, "Total", 0, 0)
    pdf.cell(0, 12, f"{row.get('total', '0.00')} US$", 0, 1, 'R')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Línea negra
    pdf.ln(4)

    # 3. Desglose detallado
    pdf.set_font('helvetica', '', 11)
    # Tarifa
    pdf.cell(140, 7, "Tarifa del viaje", 0, 0)
    pdf.cell(0, 7, f"{row.get('tarifa', '0.00')} US$", 0, 1, 'R')
    # Subtotal
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(140, 7, "Subtotal", 0, 0)
    pdf.cell(0, 7, f"{row.get('tarifa', '0.00')} US$", 0, 1, 'R')
    # Espera
    pdf.set_font('helvetica', '', 11)
    pdf.cell(140, 7, "Tiempo de espera", 0, 0)
    pdf.cell(0, 7, f"{row.get('espera', '0.00')} US$", 0, 1, 'R')
    
    pdf.ln(12)

    # 4. Información del Conductor y Vehículo
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 7, f"Viajaste con {row.get('conductor', 'N/A')}", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    detalles = f"{row.get('servicio', 'UberX')}  {row.get('distancia', '0 km')} | {row.get('duracion', '0 min')}"
    pdf.cell(0, 7, detalles, ln=True)
    pdf.ln(8)

    # 5. Ruta con formato de la plantilla
    pdf.set_text_color(0, 0, 0)
    # Inicio
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(15, 6, f"{row.get('hora_inicio', '--:--')} | ", 0, 0)
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, f"{row.get('origen', 'Origen')}")
    pdf.ln(2)
    # Fin
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(15, 6, f"{row.get('hora_fin', '--:--')} | ", 0, 0)
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, f"{row.get('destino', 'Destino')}")

    return bytes(pdf.output())

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Uber Report Studio", layout="wide")

st.title("🚗 Generador de Reportes Individuales Uber")
st.write("Sube tu archivo CSV para visualizar los viajes y generar el PDF con el formato oficial.")

archivo_subido = st.file_uploader("Cargar archivo CSV", type="csv")

if archivo_subido is not None:
    # Leer el archivo
    df = pd.read_csv(archivo_subido)
    
    # --- VISTA PREVIA DE LA TABLA (Requerimiento del usuario) ---
    st.subheader("📋 Vista previa de la tabla de datos")
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # --- SELECCIÓN Y GENERACIÓN ---
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        st.subheader("Seleccionar viaje")
        viaje_idx = st.selectbox(
            "Selecciona el ID del viaje para el reporte:",
            options=df.index,
            format_func=lambda x: f"Viaje {df.iloc[x].get('fecha_texto', x)} - {df.iloc[x].get('total')} US$"
        )
        viaje_data = df.loc[viaje_idx]
        
    with col_der:
        st.subheader("Acciones")
        if st.button("🚀 Preparar PDF"):
            try:
                pdf_output = generar_pdf(viaje_data)
                st.download_button(
                    label="📥 Descargar Reporte PDF",
                    data=pdf_output,
                    file_name=f"Uber_{viaje_data.get('fecha_texto', 'reporte')}.pdf",
                    mime="application/pdf"
                )
                st.success("¡PDF generado! Haz clic en el botón de arriba para descargar.")
            except Exception as e:
                st.error(f"Error al generar el PDF: {e}")

else:
    st.info("Esperando archivo CSV. Asegúrate de que las columnas coincidan con el formato requerido.")
