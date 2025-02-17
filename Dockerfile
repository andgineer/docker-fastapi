FROM andgineer/lean-python

COPY requirements.txt requirements.txt

RUN uv pip install -r requirements.txt

ENTRYPOINT [ "python" ]
