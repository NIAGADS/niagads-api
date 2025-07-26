# Use the official Node.js 18 image as the base image for building
FROM node:18 AS builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the application code
COPY . .
COPY .env.local .env.local

# Build the Next.js application
RUN npm run build

# Use a lightweight Node.js image for the production environment
# FROM node:18-alpine AS runner

# Set the working directory in the container
#WORKDIR /app

# Copy the built application from the builder stage
#COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/public ./public
#COPY --from=builder /app/package.json ./package.json
#COPY --from=builder /app/.env.local ./.env.local

# Install only production dependencies
#RUN npm install --production --legacy-peer-deps

# Expose the port the app runs on
EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]
