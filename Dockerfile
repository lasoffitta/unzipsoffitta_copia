# Usa un'immagine di base di Python
FROM python:3.8

# Aggiorna i repository e installa le dipendenze necessarie
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    cmake \
    libnss3 \
    libnss3-dev \
    libcairo2-dev \
    libjpeg-dev \
    libgif-dev \
    cmake \
    libblkid-dev \
    e2fslibs-dev \
    libboost-all-dev \
    libaudit-dev \
    libopenjp2-7-dev \
    g++  # Aggiunto il pacchetto g++

# Scarica e estrai Poppler
RUN wget https://poppler.freedesktop.org/poppler-21.09.0.tar.xz \
    && tar -xvf poppler-21.09.0.tar.xz \
    && cd poppler-21.09.0 \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Release \
             -DCMAKE_INSTALL_PREFIX=/usr \
             -DTESTDATADIR=$PWD/testfiles \
             -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
             .. \
    && make \
    && make install

# Copia il file poppler.py nella directory di lavoro nel container
WORKDIR /app
COPY poppler.py /app/poppler.py

# Installare le dipendenze Python
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Pulisce eventuali file temporanei non necessari
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Aggiungi la cartella utils al percorso (PATH)
ENV PATH="/poppler-21.09.0/build/utils:${PATH}"

# Comando da eseguire quando il container viene avviato
CMD ["python", "poppler.py"]
