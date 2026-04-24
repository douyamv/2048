# ---- Build stage ----
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /build

# Cache deps
COPY backend/pom.xml backend/pom.xml
RUN cd backend && mvn -B -q -DskipTests dependency:go-offline || true

# Build
COPY backend backend
RUN cd backend && mvn -B -q -DskipTests package

# ---- Runtime stage ----
FROM eclipse-temurin:17-jre
WORKDIR /app

COPY --from=build /build/backend/target/music-website-1.0.0.jar /app/app.jar
COPY frontend /app/frontend

EXPOSE 8080

# Free-tier friendly JVM tuning
ENV JAVA_OPTS="-Xmx400m -XX:+UseSerialGC -XX:MaxRAMPercentage=75"

CMD ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
