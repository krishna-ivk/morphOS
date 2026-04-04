FROM python:3.11-slim AS base

WORKDIR /app

COPY pyproject.toml .
COPY skyforce/ skyforce/

RUN pip install --no-cache-dir -e .

FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY skyforce/ skyforce/
COPY scripts/ scripts/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import skyforce; print('healthy')" || exit 1

CMD ["python", "-m", "skyforce"]
