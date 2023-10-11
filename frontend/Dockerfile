FROM node:latest

WORKDIR /app

COPY package*.json .

RUN npm install
RUN npm update npm -g
RUN npm install -g ember-cli

COPY . .

WORKDIR /app/students_app

EXPOSE 4200

# Define the command to start the Ember.js app
CMD ["ember", "serve"]