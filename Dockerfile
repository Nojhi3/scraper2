FROM node:18 AS frontend-build
WORKDIR /app/frontend

RUN mkdir -p /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .  
RUN npm run build

FROM python:3.12 AS backend
WORKDIR /app 

COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uvicorn  # ✅ Explicitly install Uvicorn

COPY backend/ /app/

FROM python:3.12
WORKDIR /app

COPY --from=backend /app /app
COPY --from=frontend-build /app/frontend/dist /app/frontend/build

ENV TOGETHER_API_KEY="8b283a377efef633e1ca5ab57de868d6ac25b1af08c8ecd7a2b41a79ede116ef"

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir fastapi uvicorn

EXPOSE 80 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & python -m http.server 80 --directory /app/frontend/build"]