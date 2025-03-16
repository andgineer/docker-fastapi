FROM andgineer/lean-python

COPY requirements.txt requirements.txt

RUN uv pip install -r requirements.txt

# python is set in ENTRYPOINT in the base image so no need to set it before `-m`
CMD ["-m", "uvicorn", "singularity:app", "--host", "0.0.0.0"]
