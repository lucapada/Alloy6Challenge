# Alloy Challenge Solutions Processing

## Instructions

### Generate .als Files from .xlsx (Microsoft Forms)
1. Ensure `docker` is installed, then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Run `generate_als.py` from the terminal:
    ```bash
    python generate_als.py
    ```

### Validate .als Model
1. Initialize Alloy4Fun as a git submodule:
    ```bash
    git submodule update --init --recursive
    ```
2. Apply the provided `Dockerfile` patch in the `Alloy4Fun/api` directory.
3. Navigate to the `Alloy4Fun/api` directory and build the Alloy4Fun API Docker image:
    ```bash
    docker build -t alloy4fun-api .
    ```
4. Start the Docker container:
    ```bash
    docker run -it --rm -p 8080:8080 alloy4fun-api
    ```
5. Wait for the following output:
    ```
    INFO  [org.wildfly.swarm] (main) THORN99999: Thorntail is Ready
    ```
6. Return to the main directory and either:
    - Run `python validate_als_demo.py` to check if the endpoint is working properly.
    - Run `python validate_als.py` to validate all the .als files.