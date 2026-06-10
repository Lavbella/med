
import streamlit as st
import requests
import base64
from PIL import Image
import io
import pydicom
import numpy as np
from dotenv import load_dotenv
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama-med:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:4b")

def convert_dicom_to_png(dicom_file):
    try:
        # Ler o ficheiro DICOM
        ds = pydicom.dcmread(dicom_file, force=True)
        
        # 2. Corrigir a falta de TransferSyntaxUID (O erro atual)
        if not ds.file_meta.get("TransferSyntaxUID"):
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

        # Se o ficheiro não tiver metadados de transferência, 
        # precisamos de definir um padrão para o pydicom não se perder
        if not hasattr(ds, 'file_meta'):
            ds.file_meta = pydicom.dataset.Dataset()
            ds.is_little_endian = True
            ds.is_implicit_VR = True

        # Extrair os pixéis (lidando com diferentes profundidades de bits)
        img_array = ds.pixel_array.astype(float)

        # Normalização Simples (0 a 255)
        # Subtraímos o mínimo e dividimos pelo alcance para evitar valores negativos
        img_min = np.min(img_array)
        img_max = np.max(img_array)
        
        if img_max > img_min:
            rescaled_image = (img_array - img_min) / (img_max - img_min) * 255
        else:
            rescaled_image = img_array * 0
            
        # O ERRO ESTAVA AQUI: Usar np.uint8
        final_image = Image.fromarray(rescaled_image.astype(np.uint8))
        
        return final_image
    
    except Exception as e:
        # Log detalhado para o terminal do VS Code
        print(f"Erro técnico no DICOM: {e}")
        return None
    
# 1. Configuração da Interface
st.set_page_config(page_title="MedGemma (Gemma 3) Assistant", layout="wide")
st.title("🩺 Assistente Médico Local - Gemma 3:4b")
st.markdown("---")

# 2. Definições do Modelo e Hardware (em cima)
# OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
# MODEL_NAME = "gemma3:4b"

# 3. Sidebar com informações de Hardware
st.sidebar.header("Estado do Sistema")
st.sidebar.info(f"🖥️ CPU: i5-6200U (4 Cores)\n🧠 RAM: 8GB + 12GB SWAP\n🤖 Modelo: {MODEL_NAME}")

# 4 No file_uploader, adiciona o tipo 'dcm'
uploaded_file = st.file_uploader("Carregue o exame (PNG, JPG ou DICOM)", type=['png', 'jpg', 'jpeg', 'dcm'])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    if uploaded_file.name.endswith('.dcm'):
        image = convert_dicom_to_png(uploaded_file)
        st.sidebar.success("DICOM convertido para PNG com sucesso!")
    else:
        image = Image.open(uploaded_file)
    # ... segue o resto do teu código igual ...


    # # Abrir imagem e redimensionar para 448x448 (Otimização para o teu i5)
    # image = Image.open(uploaded_file)

    # Converter para RGB caso seja RGBA ou DICOM convertido
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
# 2. Converter para Bytes para o Streamlit (Evita o erro de resize interno)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    # 3. Mostrar no Streamlit usando BYTES (Mais seguro para o Python 3.12)
    col1, col2 = st.columns(2)

    with col1:
        # Passamos img_bytes em vez do objeto Image
        st.image(img_bytes, caption=f"Cérebro: {image.size[0]}x{image.size[1]}", width=400)
    
    # 4. Preparar Base64 para o Gemma 3 (O código do modelo mantém-se)
    img_str = base64.b64encode(img_bytes).decode()

    with col2:
        st.subheader("Análise Clínica")
        user_prompt = st.text_area(
            "O que deseja analisar?", 
            "Analyze this medical image in detail. Describe clinical findings and potential abnormalities.",
            height=100
        )

# 1. Criar uma área expansível na barra lateral para o Protocolo (System Prompt)
with st.sidebar:
    st.header("Configurações Médicas")
    system_instruction = st.text_area(
        "Protocolo de Sistema (System Prompt):",
        value=(
            "You are a specialized neuroradiology assistant. "
            "Analyze brain CT/MRI scans following this protocol:\n"
            "1. SYMMETRY: Evaluate midline shift and hemispheric symmetry.\n"
            "2. VENTRICLES: Check for dilation, compression, or effacement.\n"
            "3. TISSUE: Identify abnormal densities (hemorrhage/edema) or lesions.\n"
            "4. CONCLUSION: Provide a technical clinical summary.\n"
            "Be factual, concise, and use professional medical terminology."
        ),
        height=250
    ) 

if st.button("🚀 Analisar com Gemma 3"):
    with st.spinner("O i5-6200U está a processar... (Verás o texto a aparecer aos poucos)"):
        try:
            # 2. Payload corrigido para o formato Gemma 3 (Chat)
            payload = {
                "model": MODEL_NAME,
                "prompt": user_prompt,
                "system": system_instruction,  # Usa o que escreveste na barra lateral,
                "images": [img_str],  # No generate, a imagem fica na raiz do JSON
                "stream": True,
                "options": {
                    "num_thread": 2,
                    "num_ctx": 1024,
                    "temperature": 0.1
                }
            }
            
            # Fazemos o pedido com stream=True
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=None)
            
            if response.status_code == 200:
                placeholder = st.empty() # Espaço para o texto dinâmico
                full_response = ""
                
                for line in response.iter_lines():
                    if line:
                        import json
                        chunk = json.loads(line.decode('utf-8'))
                        token = chunk.get("response", "")
                        if token:
                            full_response += token
                            placeholder.markdown(full_response + "▌") # Efeito de escrita
                        if chunk.get("done"):
                            break
                        
                placeholder.markdown(full_response) # Texto final limpo
            else:
                st.error(f"Erro no Ollama: {response.text}")
                
        except Exception as e:
            st.error(f"Ocorreu um erro: {str(e)}")