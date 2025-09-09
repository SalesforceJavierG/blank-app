import streamlit as st
import pandas as pd
import docx
from io import BytesIO

st.set_page_config(page_title="Gestor de Recetas", layout="wide")

st.title("Gestor Interno de Recetas")

# --- Sidebar ---
st.sidebar.header("Instrucciones")
st.sidebar.markdown(
    """
    - Sube un archivo de recetas en Word o TXT.  
    - (Opcional) Sube un Excel de ingredientes.  
    - Genera la plantilla de salida y descárgala.  
    """
)

# --- Step 1: Upload recipes ---
st.header("1. Subir archivo de recetas")
recipe_file = st.file_uploader("Selecciona un archivo de recetas", type=["docx", "txt"])

text = ""
if recipe_file:
    file_details = {
        "Nombre": recipe_file.name,
        "Tipo": recipe_file.type,
        "Tamaño (KB)": round(len(recipe_file.getvalue()) / 1024, 2),
    }
    st.success("Archivo de recetas cargado correctamente.")
    st.json(file_details)

    # Preview del contenido
    if recipe_file.name.endswith(".txt"):
        text = recipe_file.getvalue().decode("utf-8", errors="ignore")
    elif recipe_file.name.endswith(".docx"):
        doc = docx.Document(recipe_file)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

    if text:
        st.subheader("Vista previa del archivo de recetas")
        st.text_area("Contenido detectado", text[:2000], height=250)
    else:
        st.warning("No se pudo leer el contenido del archivo.")

# --- Step 2: Optional ingredients Excel ---
st.header("2. (Opcional) Subir Excel de ingredientes")
ingredients_file = st.file_uploader("Selecciona un archivo de ingredientes", type=["xlsx"])

if ingredients_file:
    st.success("Archivo de ingredientes cargado.")
    df_ing = pd.read_excel(ingredients_file)
    st.subheader("Vista previa del Excel de ingredientes")
    st.dataframe(df_ing.head())
else:
    st.info("En producción, este Excel estará precargado en el repositorio.")

# --- Step 3: Generate template ---
if recipe_file:
    st.header("3. Generar plantilla de salida")
    st.markdown("Haz clic para generar un archivo Excel con la plantilla de rentabilidad.")

    if st.button("Generar plantilla"):
        # DataFrame ficticio de ejemplo
        data = {
            "Receta": ["Pasta Carbonara", "Ensalada César", "Paella"],
            "Costo (€)": [3.50, 2.20, 5.80],
            "Precio Venta (€)": [9.00, 6.50, 14.00],
            "Margen (%)": [61, 66, 59],
        }
        df_out = pd.DataFrame(data)

        st.success("Plantilla generada con éxito.")
        st.subheader("Vista previa de la plantilla")
        st.dataframe(df_out)

        # Guardar en Excel para descarga
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_out.to_excel(writer, index=False, sheet_name="Recetas")
        excel_data = output.getvalue()

        st.download_button(
            label="Descargar plantilla",
            data=excel_data,
            file_name="plantilla_rentabilidad.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
