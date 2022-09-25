
FROM python:3.9
WORKDIR /app
COPY ./ /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 3232
CMD ["python3", "server.py"]
