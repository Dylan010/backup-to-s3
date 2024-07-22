# Usar la imagen base de Ubuntu
FROM ubuntu:latest

# Establecer las variables de entorno no interactivo
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar el sistema e instalar dependencias
RUN apt-get update && \
    apt-get install -y python3 python3-pip cron zip && \
    apt-get clean

# Instalar boto3
RUN pip3 install boto3

# Copiar el script y el directorio de backup al contenedor
COPY backup_to_s3.py /usr/local/bin/backup_to_s3.py
COPY backup /backup

# Agregar el cron job
RUN (crontab -l ; echo "0 2 * * * /usr/bin/python3 /usr/local/bin/backup_to_s3.py >> /var/log/backup.log 2>&1") | crontab

# Copiar el crontab al directorio correcto y dar permisos de ejecución
COPY mycron /etc/cron.d/backup_cron
RUN chmod 0644 /etc/cron.d/backup_cron && \
    crontab /etc/cron.d/backup_cron

# Crear el archivo de log
RUN touch /var/log/backup.log

# Ejecutar el cron y el servicio en primer plano
CMD cron && tail -f /var/log/backup.log
