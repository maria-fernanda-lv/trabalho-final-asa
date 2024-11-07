FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /projeto
COPY . /projeto/
RUN pip install -r requirements.txt 
CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000"] 