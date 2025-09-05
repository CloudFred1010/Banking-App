FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source
COPY app/src ./src

# Set PYTHONPATH so src is importable
ENV PYTHONPATH=/app

# Run as non-root
RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
