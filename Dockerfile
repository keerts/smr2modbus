FROM python:3.12-slim

LABEL org.opencontainers.image.title="smr2modbus"
LABEL org.opencontainers.image.description="Bridge SMR v5 telegrams from telnet to Modbus TCP input registers"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY smr2modbus ./smr2modbus

EXPOSE 502 8080

ENTRYPOINT ["python", "-m", "smr2modbus"]
