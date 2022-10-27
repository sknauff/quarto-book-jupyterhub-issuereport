FROM jupyter/datascience-notebook:2022-10-26

COPY ./download_quarto.py . 
RUN python download_quarto.py && rm download_quarto.py

USER root

RUN apt update \
    && apt full-upgrade -y \
    && apt install -yq --no-install-recommends \
            # Quarto
            /tmp/quarto.deb \
            # 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # clean up downloaded quarto.deb
    && rm /tmp/quarto.deb

USER $NB_UID

RUN mamba install -c conda-forge -y \
        # jupyter-server-proxy: needed for VSCodium, Pluto and others.
        jupyter-server-proxy