# Use an official Node.js runtime as a parent image
FROM node:14-alpine

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Expose port 80 (or any other port you want to use)
EXPOSE 80

# Serve the static files with a simple HTTP server
CMD ["npx", "serve", "-s", "build", "-l", "80"]

