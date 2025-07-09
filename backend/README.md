# Pollution Prediction System

A robust Django backend system for real-time pollution and weather data analysis with machine learning capabilities.

## Features

- JWT and session-based authentication with admin and regular user roles
- Kafka pipeline for real-time data collection and processing from OpenAQ and OpenWeather
- Machine learning model management with local storage, prediction API, and automatic fine-tuning
- Structured data storage in PostgreSQL for raw data, predictions, and user information
- Email notification system for authentication and pollution threshold alerts using Resend
- Containerized deployment with Docker and CI/CD through GitHub Actions

## Setup

### Prerequisites

- Docker and Docker Compose
- API keys for OpenWeather and OpenAQ
- Resend API key for email notifications

### Environment Variables

Copy the `.env.example` file to `.env` and fill in your configuration:

```bash
cp .env .env
```

### Running with Docker

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Zookeeper
- Kafka broker
- Django web server
- Kafka producer (collecting data)
- Kafka processor (transforming data)
- Kafka consumer (making predictions)
- Nginx for serving the API

### Running Without Docker (Development)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Start the development server:
```bash
python manage.py runserver
```

5. In separate terminals, run:
```bash
python manage.py run_kafka_producer
python manage.py run_kafka_processor
python manage.py run_kafka_consumer
```

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login user

### User Management
- `GET /api/users/me/` - Get current user details
- `PUT /api/users/me/` - Update current user
- `POST /api/users/password-reset/` - Request password reset
- `POST /api/users/password-reset/confirm/` - Confirm password reset
- `PUT /api/users/threshold/` - Update personal pollution threshold

### Data Endpoints
- `GET /api/data/raw/` - Get raw data
- `GET /api/data/processed/` - Get processed data
- `GET /api/data/latest/` - Get latest data for a location
- `GET /api/data/locations/` - List locations
- `GET /api/data/statistics/` - Get data statistics

### Prediction Endpoints
- `GET /api/predictions/models/` - List prediction models
- `GET /api/predictions/models/active/` - Get active model
- `GET /api/predictions/list/` - List predictions
- `POST /api/predictions/get/` - Get prediction for a location
- `POST /api/predictions/custom/` - Make a custom prediction
- `GET /api/predictions/training/history/` - Get model training history
- `GET /api/predictions/evaluation/` - Get model evaluation metrics

### Admin Endpoints
- `GET /api/users/list/` - List all users (admin only)
- `PUT /api/users/threshold/default/` - Update default threshold (admin only)
- `POST /api/data/purge/` - Purge old data (admin only)
- `POST /api/predictions/training/manual/` - Manually train model (admin only)
- `POST /api/predictions/models/update-remote/` - Update remote model (admin only)
- `POST /api/predictions/models/download-remote/` - Download remote model (admin only)

## Project Structure

```
├── data_collection/      # Data collection from external APIs
│   ├── kafka/            # Kafka producer and processor
│   ├── management/       # Management commands
│   └── models.py         # Data models
├── predictions/          # ML model management and predictions
│   ├── kafka/            # Kafka consumer
│   ├── management/       # Management commands
│   └── services.py       # Model services
├── users/                # User authentication and management
└── pollution_prediction/ # Main Django project
```

## Testing

Run tests with pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License.