# Automated Bug Triage System

A machine learning-powered system that automatically assigns incoming bug reports to the appropriate developer or team based on the bug's title and description.

## Features

- **Machine Learning Pipeline**: Uses TF-IDF vectorization and Naive Bayes/Logistic Regression for classification
- **Text Preprocessing**: Includes lowercasing, stopword removal, and tokenization
- **Priority Prediction**: Automatically predicts bug priority levels
- **Duplicate Detection**: Identifies potential duplicate bug reports using cosine similarity
- **REST API**: FastAPI backend with prediction endpoints
- **Database Storage**: SQLite database for storing bug reports and predictions
- **Retraining Capability**: Ability to retrain the model with new data

## Project Structure

```
bug_triage/
├── app/
│   ├── main.py          # FastAPI application
│   └── database.py      # Database models and connection
├── model/
│   └── bug_triage_model.py  # ML model implementation
├── data/
│   └── bug_reports.csv  # Sample dataset
├── scripts/             # Additional scripts (if needed)
├── deploy.sh            # Automated deployment script
├── docker-compose.yml   # Docker service orchestration
├── Dockerfile           # Multi-stage Docker build
├── .env.example         # Environment variable example
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

### Option 1: Local Development

1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:

```bash
python main.py install
```

### Option 2: Docker Deployment (Recommended)

1. Clone the repository
2. Navigate to the project directory
3. Run the deployment script:

```bash
chmod +x deploy.sh
./deploy.sh
```

Or manually:

```bash
docker-compose up -d
```

## Setup

### Local Development

1. Create the database tables:

```bash
python main.py db
```

2. Train the machine learning model:

```bash
python main.py train
```

3. Start the FastAPI server:

```bash
python main.py run
```

### Docker Deployment

The deployment script handles all setup automatically. The API will be available at `http://localhost:8000`

## Running the Application

The API will be available at `http://localhost:8000`

### Available Endpoints

- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `POST /predict` - Predict bug assignment and priority
- `GET /reports` - View all bug reports
- `POST /retrain` - Retrain the model with new data

## Deployment

### Docker Deployment

The application includes Docker configuration for easy deployment:

- **Dockerfile**: Multi-stage build for production
- **docker-compose.yml**: Complete service orchestration
- **deploy.sh**: Automated deployment script

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key environment variables:
- `DATABASE_URL`: Database connection string
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `MODEL_PATH`: Path to trained model file

### Production Deployment

For production deployment:

1. Use PostgreSQL instead of SQLite
2. Configure proper logging
3. Set up reverse proxy (nginx)
4. Enable HTTPS
5. Configure monitoring

Example with PostgreSQL:

```yaml
# docker-compose.yml
services:
  bug-triage-api:
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/bug_triage
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: bug_triage
      POSTGRES_USER: bug_triage_user
      POSTGRES_PASSWORD: your_password
```

## API Endpoints

### POST /predict
Predict assignment and priority for a bug report.

**Request Body:**
```json
{
  "title": "Login button not working",
  "description": "User cannot click the login button on the homepage"
}
```

**Response:**
```json
{
  "assigned_to": "frontend_team",
  "assignment_confidence": 0.85,
  "priority": "high",
  "priority_confidence": 0.72,
  "is_duplicate": false,
  "duplicate_info": null
}
```

### GET /health
Health check endpoint.

### GET /reports
Get list of stored bug reports.

### POST /retrain
Retrain the model with data from the database.

## Sample Test

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Database connection fails",
       "description": "The application cannot connect to the database server"
     }'
```

Expected output:
```json
{
  "assigned_to": "backend_team",
  "assignment_confidence": 0.91,
  "priority": "high",
  "priority_confidence": 0.78,
  "is_duplicate": false,
  "duplicate_info": null
}
```

## How It Works

1. **Data Preprocessing**: Text is cleaned, tokenized, and stopwords are removed
2. **Feature Extraction**: TF-IDF vectorization converts text to numerical features
3. **Model Training**: Naive Bayes for team assignment, Logistic Regression for priority
4. **Prediction**: New bug reports are processed and classified
5. **Duplicate Detection**: Cosine similarity checks for similar existing reports
6. **Storage**: All predictions are stored in the database

## Technologies Used

- **Python**: Core programming language
- **FastAPI**: Web framework for the API
- **scikit-learn**: Machine learning library
- **NLTK**: Natural language processing
- **SQLAlchemy**: Database ORM
- **SQLite**: Database engine
- **pandas**: Data manipulation

## Future Improvements

- Implement more advanced NLP techniques (BERT, transformers)
- Add user authentication and authorization
- Implement real-time model updates
- Add more detailed analytics and reporting
- Integrate with issue tracking systems (Jira, GitHub Issues)
- Add support for multiple languages
- Implement A/B testing for model versions
- Add automated model performance monitoring