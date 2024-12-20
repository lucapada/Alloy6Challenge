# Alloy Challenge Solutions Processing

## How to
### Generate .als files from .xlsx (Microsoft Forms)
1. Install all the required packages by running:
    ```bash
    pip install -r requirements.txt
    ```
2. Run `xlsx_to_als.py` via terminal:
    ```bash
    python xlsx_to_als.py
    ```

### Validate .als model
1. Move into the `Alloy4Fun/api` directory.
2. Build the Alloy4Fun api's image with:
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