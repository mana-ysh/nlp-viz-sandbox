FROM ubuntu:16.04

COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential language-pack-ja python3 python3-pip python3-setuptools curl tmux sudo git wget unzip
    # apt-get install -y mecab libmecab-dev

RUN python3 -m pip install pip --upgrade

# install external libs 
RUN git clone https://github.com/mana-ysh/mapnlp && cd mapnlp && python3 setup.py install
# RUN pip install SudachiPy && pip install https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/sudachi/SudachiDict_core-20190718.tar.gz
RUN git clone https://github.com/WorksApplications/SudachiPy -b v0.1 && cd SudachiPy && pip install -e .
RUN cd SudachiPy/resources && wget https://github.com/WorksApplications/Sudachi/releases/download/v0.1.0/sudachi-0.1.0-dictionary-core.zip && \
    unzip sudachi-0.1.0-dictionary-core.zip && mv system_core.dic system.dic

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python3", "src/application.py"]