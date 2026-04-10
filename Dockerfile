# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Create a script to run both services
RUN echo '#!/bin/bash\npython app/main.py & streamlit run app/view.py --server.port 8501 --server.address 0.0.0.0' > run.sh
RUN chmod +x run.sh

# Run the script
CMD ["./run.sh"]
