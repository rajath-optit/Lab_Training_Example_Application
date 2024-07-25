# Use the official OpenJDK image for Java 17 as the base image
FROM openjdk:17-alpine

# Set the working directory in the container
WORKDIR /opt/app

# Copy the executable JAR file from the local filesystem to the container
COPY build/libs/optit-lab-service-0.0.1-SNAPSHOT.jar optit-lab-service.jar

# Expose the port your app runs on
EXPOSE 8080

# Define the command to run your application
CMD ["java", "-jar", "optit-lab-service.jar"]
