# python 3.9 (base)
FROM python:3.9-slim

# working directory
WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y\
    gcc \
    postgresql-client \ 
    && rm -rf /var/lib/apt/lists/*


# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the app
COPY . .

# expose port 5000
EXPOSE 5000

# run the app
CMD ["python", "app.py"]



