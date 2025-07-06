# Use docker-compose for multi-service deployment
FROM docker/compose:1.29.2

# Copy docker-compose file
COPY docker-compose.yml .

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Expose ports
EXPOSE 3000 8000

# Start services
CMD ["docker-compose", "up", "-d"] 