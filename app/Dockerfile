FROM python:3.12-slim AS builder
WORKDIR /app

# Install build dependencies only in builder stage
COPY app/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ----------------------
# Final runtime image
# ----------------------
FROM python:3.12-slim
WORKDIR /app

# Copy installed deps from builder
COPY --from=builder /root/.local /root/.local

# Copy application source
COPY app/src ./src

# Ensure local binaries are on PATH
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

# Security best practice: create non-root user
RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Add HEALTHCHECK for container runtime + Trivy compliance
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI via uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
