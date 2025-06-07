# Mangaba.AI

Framework for developing intelligent autonomous agents.

## Project Structure

```
mangaba_ai/
├── .github/                    # GitHub configurations
├── docs/                       # Documentation
│   ├── api/                   # API documentation
│   ├── guides/                # Usage guides
│   └── examples/              # Documented examples
├── src/                       # Source code
│   ├── core/                  # Framework core
│   │   ├── agents/           # Agent implementations
│   │   ├── models/           # Data models
│   │   ├── protocols/        # Protocols and interfaces
│   │   └── tools/            # Base tools
│   ├── integrations/         # Optional integrations
│   └── utils/                # General utilities
├── tests/                     # Tests
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── examples/                  # Examples
│   ├── basic/                # Basic examples
│   └── advanced/             # Advanced examples
└── scripts/                   # Utility scripts
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/mangaba_ai.git
cd mangaba_ai
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit the .env file with your settings
```

## Basic Usage

```python
from mangaba_ai import MangabaAI

# Initialize the framework
ai = MangabaAI()

# Create an agent
agent = ai.create_agent(
    name="my_agent",
    role="Analyst",
    goal="Analyze data and generate insights"
)

# Create a task
task = ai.create_task(
    description="Analyze sales data",
    agent=agent
)

# Execute the task
result = await ai.execute([task])
```

## Documentation

- [Quick Start Guide](docs/guides/quickstart.md)
- [API Documentation](docs/api/README.md)
- [Examples](docs/examples/README.md)

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Configure pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest
```

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
