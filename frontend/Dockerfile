FROM node:20-alpine

COPY . /app
WORKDIR /app
RUN npm ci

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]