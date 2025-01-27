# FastAPI DDD Boilerplate

A boilerplate project for building scalable and maintainable applications using FastAPI with a Domain-Driven Design (DDD) approach. This template provides a solid foundation to structure your code and manage dependencies effectively.

## Features

- **FastAPI Framework**: High-performance and easy-to-use web framework for building APIs.
- **Domain-Driven Design (DDD)**: Organized folder structure for separating concerns.
- **Async Support**: Built-in support for asynchronous operations.
- **Environment Configuration**: Centralized `.env` for easy environment variable management.
- **Dependency Injection**: Simplified DI setup for managing dependencies.

## Folder Structure

```
fastapi-ddd-boilerplate/
├── app/
│   ├── bootstrap/        # Dependency injection setup
│   ├── domain/           # Domain entities, value objects, aggregates
│   ├── infrastructure/   # Database, caching, external services
│   ├── presentation/     # API endpoints and related logic
│   └── application/      # Application services, use cases
├── tests/                # Unit and integration tests
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── uv.py                 # Entry point for the application
└── README.md             # Project documentation
```

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/username/uv) as the package manager

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/fastapi-ddd-boilerplate.git
   cd fastapi-ddd-boilerplate
   ```

2. **Install Dependencies**:
   ```bash
   uv install
   ```

3. **Setup Environment Variables**:
   Create a `.env` file in the root directory and configure the required settings.

4. **Run Database Migrations** (if applicable):
   ```bash
   uv migrate
   ```

5. **Start the Server**:
   ```bash
   uv run
   ```
   The application will be accessible at `http://127.0.0.1:8000`.

## Scripts

- `uv install`: Install dependencies
- `uv run`: Start the FastAPI server
- `uv test`: Run the test suite
- `uv lint`: Check for code quality issues

## Testing

Run the test suite using:
```bash
uv test
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
