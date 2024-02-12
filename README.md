# Project Healix Backend

## Description:

Project Healix is a compassionate and empowering initiative committed to fostering emotional well-being and mental health awareness. Leveraging the power of FastAPI, this Python server delivers crucial support and knowledge to users seeking guidance and understanding.

## Key Features:

Emotional Support: Provides users with access to various tools and resources tailored to address emotional challenges, fostering a sense of comfort and connection.
Mental Health Knowledge: Offers comprehensive information on a range of mental health topics, presented in a clear, accessible, and destigmatizing manner

## Setup Locally

To set up the Project Healix backend locally, follow these steps:

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.11.x
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DeepeshKalura/HealixServer
    ```

2. Navigate into the project directory:

    ```bash
    cd HealixServer
    ```

3. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

Once you have installed the dependencies, you can start the FastAPI server by running the following command:

```bash
uvicorn main:app --reload
```

This command will start the server, and it will automatically reload whenever you make changes to the code.

You can then access the server at `http://localhost:8000`.

## Contributing

We welcome contributions from the community to make Project Healix even better! If you'd like to contribute, please follow these guidelines:

### Pull Requests

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them with descriptive commit messages.
4. Push your branch to your fork: `git push origin feature-name`.
5. Submit a pull request to the `production` branch of the original repository.

### Issues

If you encounter any bugs or have ideas for new features, please open an issue on GitHub.

### Code Style

Please follow the PEP 8 style guide for Python code. Additionally, make sure to write clear and concise commit messages.

### Testing

Before submitting a pull request, make sure to test your changes locally and ensure they do not introduce any regressions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



