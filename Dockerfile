# Use an official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]