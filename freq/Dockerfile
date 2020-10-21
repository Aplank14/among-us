FROM maven:3.6.3-jdk-8 as build
COPY . .
RUN mvn clean compile package

FROM openjdk:8 as final
WORKDIR /app
COPY --from=build target/freq-*-jar-with-dependencies.jar .
CMD ["/bin/sh", "-c", "java -jar freq-*-jar-with-dependencies.jar"]
