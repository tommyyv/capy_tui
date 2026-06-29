FROM python:3.14.6

WORKDIR /capy_tui

COPY requirements.txt .

RUN python --version

RUN pip --version

RUN pip install -vvv --no-cache-dir -r requirements.txt

COPY . .

CMD ["textual", "run", "main.py"]
