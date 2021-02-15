FROM python:3.9
WORKDIR /bgl-assignment
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "./main.py"]