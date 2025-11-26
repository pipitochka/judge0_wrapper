FROM openjdk:21-jdk-slim

WORKDIR /app

# Копируем JAR файл
COPY build/libs/gateway-1.0-SNAPSHOT.jar app.jar

# Указываем точку входа
ENTRYPOINT ["java", "-jar", "app.jar"]