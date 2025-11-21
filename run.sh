#!/bin/bash
set -e

echo "Preparing Judge0 configuration..."

# Создаем директорию для конфигов
mkdir -p judge0

# Создаем конфиг с пустым JSON-объектом и гарантированным LF
printf "{}\n" > judge0/judge0.conf

echo "Configuration generated at judge0/judge0.conf"
echo "Starting services..."

# Запускаем контейнеры
docker-compose up -d
