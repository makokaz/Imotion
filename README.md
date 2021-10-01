# Imotion

Imotion is a project created during UTokyo Research Hackathon 2021.

## Using docker image to run this project

0. First, clone this project by

    ```bash
    git clone --recurse-submodules https://github.com/leavez529/Imotion.git
    ```

1. Create docker image

    ```bash
    docker build -t imotion .
    ```

2. Run docker image

    ```bash
    docker run -dp 5000:5000 imotion
    ```

3. Open website on your localhost: <http://localhost:5000>
