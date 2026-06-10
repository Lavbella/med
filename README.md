# Privacy First: Local AI for Medical Imaging Reporting

### Exploring the potential of Gemma 3 in offline clinical environments.

---

## 🌍 Language / Idioma
* [Português (#-português)](#-português)
* [English (#-english)](#-english)

---

## 🇵🇹 Português

Este projeto explora o potencial do modelo de inteligência artificial **Gemma 3** executado localmente para a geração de relatórios clínicos a partir de imagens médicas. Desenhado especificamente para ambientes hospitalares e clínicos offline, o ecossistema prioriza a privacidade dos dados do paciente (*Privacy First*), processando ficheiros médicos sensíveis sem qualquer comunicação com servidores externos.

### Estrutura do Projeto & Stack Python
O projeto está estruturado em Python e utiliza o ecossistema de imagens médicas e interface gráfica:
* **Interface Web (`app.py`)**: Interface interativa em **Streamlit** que permite carregar imagens médicas, visualizar metadados e gerar os relatórios.
* **Processamento Médico & Imagens**: 
  * `pydicom`: Essencial para a leitura e manipulação de ficheiros e metadados no formato padrão da medicina (DICOM).
  * `pylibjpeg` & `pylibjpeg-libjpeg`: Pacotes críticos do sistema para descompressão e conversão de dados pixelados DICOM comprimidos.
  * `Pillow` & `numpy`: Manipulação matemática e renderização visual das matrizes de imagem.
* **Integração com a IA**: `requests` (para comunicação local com a API do Ollama/Gemma 3) e `python-dotenv`.
* **Contentorização (`Dockerfile` & `docker-compose.yml`)**: Configuração para orquestrar o ambiente completo e isolado.

### Pré-requisitos
Antes de iniciar, certifique-se de que tem instalado na máquina de desenvolvimento/clínica:
1. [Git](https://git-scm.com)
2. [Docker e Docker Compose](https://docker.com) (Recomendado)
3. [Python 3.12](https://python.org) (Caso pretenda correr localmente sem Docker)
4. [Ollama](https://ollama.com) com o modelo Gemma 3 descarregado (se optar por execução local).

---

## Como Executar o Projeto

### 1. Clonar (Pull) o Repositório
Abra o seu terminal na diretoria onde quer guardar o projeto e execute:
```bash
git clone https://github.com/Lavbella/med.git
cd med
```
*(Nota: Substitua o URL acima se o repositório deste projeto específico de imagiologia for diferente).*

### 2. Opção A: Ambiente Python Local (Via requirements.txt)
Se preferir testar o projeto localmente na sua máquina:

```bash
# 1. Criar o ambiente virtual
python -m venv venv

# 2. Ativar o ambiente virtual
# No Windows (PowerShell):
.\venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# 3. Instalar dependências (incluindo descodificadores LibJPEG médicos)
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Opção B: Execução com Docker (Recomendado)
O Docker Compose lê as configurações do `Dockerfile` e do `docker-compose.yaml` para subir a aplicação Streamlit e isolar todos os descodificadores binários do formato DICOM, garantindo a recriação limpa das imagens de sistema:

```bash
# Parar e limpar ambientes ou volumes antigos da memória
docker compose down -v

# Construir a imagem com todas as dependências e iniciar o contentor
docker compose up -d --build
```

### 4. Como Correr e Aceder
* **Se optou pelo Ambiente Local:**
  ```bash
  streamlit run app.py
  ```
* **Se optou pelo Docker:** O contentor já inicia o serviço automaticamente em segundo plano.

**Aceder à Interface:**
Abra o seu navegador e aceda à plataforma de análise e relatórios:
* **URL:** [http://localhost:8501](http://localhost:8501)

---

## 🇬🇧 English

This project explores the potential of the **Gemma 3** language model running fully locally to generate clinical reports from medical images. Purpose-built for offline clinical and hospital environments, this ecosystem prioritizes patient data privacy (*Privacy First*), processing sensitive medical files without any outbound connection to external servers.

### Project Structure & Python Stack
The project is built with Python, gathering specific medical imaging processing frameworks:
* **Web UI (`app.py`)**: An interactive **Streamlit** dashboard used to upload medical images, inspect metadata, and trigger report generation.
* **Medical Imaging & Processing**:
  * `pydicom`: Essential for reading and manipulating medical standard DICOM files and patient metadata.
  * `pylibjpeg` & `pylibjpeg-libjpeg`: Critical packages used for decompressing and converting compressed DICOM pixel payloads.
  * `Pillow` & `numpy`: Image array mathematics and visual rendering.
* **AI Integration**: `requests` (for local REST communication with the Ollama/Gemma 3 API) and `python-dotenv`.
* **Containerization (`Dockerfile` & `docker-compose.yml`)**: Infrastructure setup to orchestrate the isolated local medical environment.

### Prerequisites
Before starting, ensure you have the following installed on your target machine:
1. [Git](https://git-scm.com)
2. [Docker & Docker Compose](https://docker.com) (Recommended)
3. [Python 3.12 ](https://python.org) (Only if running locally without Docker)
4. [Ollama](https://ollama.com) with the Gemma 3 model downloaded (if using the local execution path).

---

## How to Run the Project

### 1. Clone (Pull) the Repository
Open your terminal inside the chosen directory and deploy the code:
```bash
git clone https://github.com/Lavbella/med.git
cd med
```
*(Note: Update the URL above if this medical reporting project resides in a separate repository).*

### 2. Option A: Local Python Environment (Via requirements.txt)
To run or develop the project directly on your host operating system:

```bash
# 1. Create the virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install all medical components and dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

<h3>3. Option B: Dockerized Deployment (Recommended)</h3>
Docker Compose will leverage your `Dockerfile` and `docker-compose.yaml` configuration to spin up the Streamlit interface and encapsulate the specialized DICOM system decoders, forcing a clean recreation of host images:

```bash
# Stop previous setups and wipe cached docker volumes
docker compose down -v

# Rebuild the application image and run the components in detached mode
docker compose up -d --build
```

### 4. Running the Application
* **If using the Local Environment:**
  ```bash
  streamlit run app.py
  ```
* **If using Docker Deployment:** The container will start the Streamlit orchestration automatically in the background.

**Accessing the Application Interface:**
Launch your web browser and navigate to the local clinical portal:
* **URL:** [http://localhost:8501](http://localhost:8501)

---

## License / Licença
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
