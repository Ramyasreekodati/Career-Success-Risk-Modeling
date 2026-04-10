# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the ports (Render will use $PORT for one of them)
EXPOSE 8000
EXPOSE 8501

# Create a robust startup script
RUN echo '#!/bin/bash\n\
# Start the Backend on port 8000\n\
python app/main.py &\n\
\n\
# Start the Frontend on the port provided by Render ($PORT) or default to 8501\n\
streamlit run app/view.py --server.port=${PORT:-8501} --server.address=0.0.0.0\n\
' > run.sh

RUN chmod +x run.sh

# Run the script
CMD ["./run.sh"]
