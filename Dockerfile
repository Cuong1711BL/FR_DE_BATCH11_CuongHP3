FROM apache/airflow:2.10.3

USER root

# Add the scripts directory to PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/scripts"
ENV AIRFLOW__LOGGING__LOGGING_LEVEL=INFO

# Switch back to airflow user
USER airflow

# Ensure the /opt/airflow/logs directory exists and set permissions
RUN mkdir -p /opt/airflow/logs && \
    chown -R airflow:root /opt/airflow/logs && \
    chmod -R 775 /opt/airflow/logs

USER root

# Install required system packages for Selenium and ChromeDriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    chromium-driver \
    python3-dev \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh

# Make the script executable
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Switch back to airflow user
USER airflow

# Copy requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER root

# Copy project files
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts
COPY plugins /opt/airflow/plugins
COPY datasets /opt/airflow/datasets

# Ensure datasets directory exists and has appropriate permissions
RUN mkdir -p /opt/airflow/datasets && \
    chmod -R 775 /opt/airflow/datasets


