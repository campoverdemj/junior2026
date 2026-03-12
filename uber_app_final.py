import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# --- CLASE PDF CONFIGURADA PARA CALCAR LA PLANTILLA ---
class UberPDF(FPDF):
    def header(self):
        # Logo tipo texto Uber
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(0, 0, 0)
        self.cell(0, 20, 'Uber', ln=True)
        self.ln(2)

def generar_pdf(row):
    pdf = UberPDF()
    pdf.add_page()
    
    # 1. Saludo y Fecha (Igual a la plantilla)
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Gracias por elegir Uber, {row.get('usuario', 'Mario')}", ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"{row.get('fecha_texto', '16 de enero de 2026')}", ln=True)
    pdf.cell(0, 6, "Esperamos que hayas disfrutado tu viaje de esta tarde.", ln=True)
    pdf.ln(10)

    # 2. Bloque de Total (Fila destacada)
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(140, 15, "Total", 0, 0)
    pdf.cell(0, 15, f"{row.get('total', '22.40')} US$", 0, 1, 'R')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Línea negra fina
    pdf.ln(5)

    # 3. Desglose (Tarifa y Espera)
    pdf.set_font('helvetica', '', 11)
    # Tarifa
    pdf.cell(140, 8, "Tarifa del viaje", 0, 0)
    pdf.cell(0, 8, f"{row.get('tarifa', '22.37')} US$", 0, 1, 'R')
    # Subtotal
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(140, 8, "Subtotal", 0, 0)
    pdf.cell(0, 8, f"{row.get('tarifa', '22.37')} US$", 0, 1, 'R')
    # Espera
    pdf.set_font('helvetica', '', 11)
    pdf.cell(140, 8, "Tiempo de espera", 0, 0)
    pdf.cell(0, 8, f"{row.get('espera', '0.03')} US$", 0, 1, 'R')
    pdf.ln(15)

    # 4. Detalles del Conductor y Vehículo
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, f"Viajaste con {row.get('conductor', 'VICTOR DAVID')}", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    detalles_auto = f"{row.get('servicio', 'UberX')}  {row.get('distancia', '53.1 kilómetros')} | {row.get('duracion', '1 hora 5 min')}"
    pdf.cell(0, 8, detalles_auto, ln=True)
    pdf.ln(10)

    # 5. Ruta (Puntos de inicio y fin con hora)
    pdf.set_text_color(0, 0, 0)
    # Inicio
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(15, 6, f"{row.get('hora_inicio', '09:44')} | ", 0, 0)
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, f"{row.get('origen', 'Dirección de origen')}")
    pdf.ln(2)
    # Fin
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(15, 6, f"{row.get('hora_fin', '10:49')} | ", 0, 0)
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, f"{row.get('destino', 'Dirección de destino')}")

    # Retorno de bytes compatible con Streamlit
    return bytes(pdf.output())

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Uber Receipt Generator", layout="wide")
st.title("🚗 Generador de Recibos Uber")

archivo = st.file_uploader("Sube tu archivo CSV", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)
    st.subheader("Selecciona el viaje para calcar la plantilla")
    
    indice = st.selectbox("ID del Viaje", options=df.index)
    viaje = df.loc[indice]
    
    # Vista previa rápida
    st.info(f"Seleccionado: Viaje de {viaje.get('usuario')} - {viaje.get('total')} US$")

    if st.button("✨ Generar PDF Exacto"):
        try:
            pdf_data = generar_pdf(viaje)
            st.download_button(
                label="📥 Descargar PDF",
                data=pdf_data,
                file_name=f"Recibo_Uber_{indice}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.write("Por favor, carga el archivo CSV para continuar.")
