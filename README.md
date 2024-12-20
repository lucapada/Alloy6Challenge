# Alloy Challenge Solutions Processing

## How to
### Generate .als files from .xlsx (Microsoft Forms)
1. Install all the required packages by running:
    ```bash
    pip install -r requirements.txt
    ```
2. Run `generate_als.py` via terminal:
    ```bash
    python generate_als.py
    ```

### Validate .als model
1. Patch the `Dockerfile` within the `Alloy4Fun/api` directory with the one you find in this directory.
2. Move into the `Alloy4Fun/api` directory, then build the Alloy4Fun api's docker image with:
    ```bash
    docker build -t alloy4fun-api .
    ```
3. Run the docker container with:
    ```bash
    docker run -it --rm -p 8080:8080 alloy4fun-api
    ```
4. Wait for the following output: 
    ```
    INFO  [org.wildfly.swarm] (main) THORN99999: Thorntail is Ready
    ```
5. Move back to the main directory and either:
    - run `python validate_als_demo.py` to check if the endpoint is working properly
    - run `python validate_als.py` to validate all the .als files