# Partire da un'immagine Python
FROM python:3.8

# Aggiornare l'elenco dei pacchetti e installare unrar
RUN echo 'deb http://deb.debian.org/debian/ bullseye main contrib non-free' > /etc/apt/sources.list && \
    apt-get update && apt-get install -y unrar

# Impostare la directory di lavoro
WORKDIR /app

# Copiare i file del progetto nella directory di lavoro
COPY . /app

# Installare le dipendenze Python
RUN pip install -r requirements.txt

# Comando da eseguire quando il container viene avviato
CMD ["python", "app.py"]
