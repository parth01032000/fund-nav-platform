FROM python:3.11-slim
WORKDIR /app
COPY nav_calculator.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3", "nav_calculator.py"]
