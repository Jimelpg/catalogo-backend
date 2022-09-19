#Clonar el proyecto
git clone <URL del repositorio>

#Crear virtualenviroment para el proyecto
python -m venv venv

#activar el venv
Windows
venv\Scripts\activate

Mac
source venv/bin/activate

#descargar las dependecias
pip install -r requirements.txt

#correr el proyecto
python app.py
