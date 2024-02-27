FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME World

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--reload"]