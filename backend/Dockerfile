# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents (including requirements.txt) into the container
COPY . /app

# Step 4: Install dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose port 5000 to communicate with the outside world
EXPOSE 5001

# Step 6: Define environment variables (if needed)
ENV FLASK_APP=app.py
ENV FLASK_ENV=testing

# Step 7: Run the application when the container starts
CMD ["python", "app.py"]
