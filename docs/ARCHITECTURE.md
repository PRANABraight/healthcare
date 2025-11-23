# 🏗️ System Architecture

## Overview

The Clinical Decision Support System (CDSS) is built using a modular, layered architecture that separates concerns and enables scalability, maintainability, and testability.

## High-Level Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[Streamlit Dashboard]
        B[FastAPI REST API]
    end
    
    subgraph "Business Logic Layer"
        C[Controllers]
        D[Analytics Engine]
        E[ML Models]
        F[Text Processing]
    end
    
    subgraph "Data Layer"
        G[Data Pipeline]
        H[Database Manager]
        I[Feature Engineering]
    end
    
    subgraph "Storage Layer"
        J[(SQLite/PostgreSQL)]
        K[CSV Files]
        L[Model Artifacts]
    end
    
    A --> C
    A --> D
    B --> C
    B --> E
    C --> G
    C --> H
    D --> E
    D --> I
    E --> L
    F --> D
    G --> J
    G --> K
    H --> J
    I --> G
```

## Component Descriptions

### 1. Presentation Layer

#### Streamlit Dashboard (`app_final.py`)
- **Purpose**: Interactive web interface for clinicians
- **Features**:
  - Real-time data visualization
  - Drug interaction checking
  - Patient risk assessment
  - Clinical text analysis
  - Analytics dashboards
- **Technology**: Streamlit, Plotly
- **Port**: 8501 (default)

#### FastAPI REST API (`api/main.py`)
- **Purpose**: Programmatic access to ML models and analytics
- **Endpoints**:
  - `/predict` - Patient risk prediction
  - `/interactions` - Drug interaction checking
  - `/analyze` - Text analysis
  - `/cohort` - Cohort analytics
- **Technology**: FastAPI, Pydantic
- **Port**: 8000 (default)
- **Documentation**: Auto-generated Swagger UI at `/docs`

### 2. Business Logic Layer

#### Controllers (`src/controllers/`)
- **Purpose**: Orchestrate business logic and data flow
- **Responsibilities**:
  - Request validation
  - Business rule enforcement
  - Error handling
  - Response formatting

#### Analytics Engine (`src/models/analytics_engine.py`)
- **Purpose**: Core analytics and ML functionality
- **Features**:
  - Model training and evaluation
  - Prediction generation
  - Performance monitoring
  - Feature importance calculation

#### ML Models (`src/models/`)
- **Purpose**: Machine learning model implementations
- **Models**:
  - Random Forest (primary)
  - XGBoost (high performance)
  - Logistic Regression (baseline)
- **Artifacts**: Serialized models in `.pkl` format

#### Text Processing (`src/utils/`)
- **Purpose**: NLP and text analysis
- **Features**:
  - Medical entity extraction
  - Sentiment analysis
  - ICD-10 code suggestion
  - Text cleaning and normalization

### 3. Data Layer

#### Data Pipeline (`src/models/data_pipeline.py`)
- **Purpose**: ETL (Extract, Transform, Load) operations
- **Responsibilities**:
  - Data ingestion from multiple sources
  - Data cleaning and validation
  - Data transformation
  - Feature engineering

#### Database Manager (`src/database/db_manager.py`)
- **Purpose**: Database operations and connection management
- **Features**:
  - Connection pooling
  - Query execution
  - Transaction management
  - Error handling

#### Feature Engineering (`src/models/data_pipeline.py`)
- **Purpose**: Create derived features for ML models
- **Features**:
  - Clinical risk scores
  - Polypharmacy indicators
  - Temporal features
  - Interaction features

### 4. Storage Layer

#### Database (SQLite/PostgreSQL)
- **Purpose**: Structured data storage
- **Schema**:
  - `patients` - Patient demographics and clinical data
  - `outcomes` - Clinical outcomes and events
  - `drugs` - Drug information
  - `interactions` - Drug-drug interactions
  - `transcriptions` - Medical text data

#### CSV Files (`data/`)
- **Purpose**: Raw data storage and backup
- **Files**:
  - Clinical cohort data
  - Drug interactions database
  - Drug reviews
  - Medical transcriptions

#### Model Artifacts (`src/models/`)
- **Purpose**: Serialized ML models
- **Format**: Pickle (`.pkl`)
- **Versioning**: Timestamped filenames

## Data Flow

### 1. Training Pipeline

```mermaid
sequenceDiagram
    participant CSV as CSV Files
    participant DP as Data Pipeline
    participant FE as Feature Engineering
    participant ML as ML Models
    participant DB as Database
    
    CSV->>DP: Load raw data
    DP->>DP: Clean & validate
    DP->>FE: Transform data
    FE->>FE: Create features
    FE->>ML: Training dataset
    ML->>ML: Train models
    ML->>ML: Evaluate performance
    ML->>DB: Save metrics
    ML->>ML: Serialize model
```

### 2. Prediction Pipeline

```mermaid
sequenceDiagram
    participant User as User/API
    participant App as Streamlit/FastAPI
    participant Ctrl as Controllers
    participant ML as ML Models
    participant DB as Database
    
    User->>App: Request prediction
    App->>Ctrl: Validate input
    Ctrl->>DB: Fetch patient data
    DB->>Ctrl: Return data
    Ctrl->>ML: Prepare features
    ML->>ML: Generate prediction
    ML->>Ctrl: Return prediction + SHAP
    Ctrl->>App: Format response
    App->>User: Display results
```

### 3. Analytics Pipeline

```mermaid
sequenceDiagram
    participant User as Clinician
    participant Dash as Dashboard
    participant Eng as Analytics Engine
    participant DB as Database
    participant Viz as Visualizations
    
    User->>Dash: Select analysis
    Dash->>Eng: Request analytics
    Eng->>DB: Query data
    DB->>Eng: Return results
    Eng->>Eng: Compute statistics
    Eng->>Viz: Generate plots
    Viz->>Dash: Render charts
    Dash->>User: Display insights
```

## Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **XGBoost** - Gradient boosting
- **SHAP** - Model interpretability

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **Matplotlib/Seaborn** - Statistical plots

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production database (recommended)

### API
- **FastAPI** - REST API framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### NLP
- **NLTK** - Natural language toolkit
- **spaCy** - Advanced NLP
- **Regex** - Pattern matching

### Testing
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **unittest.mock** - Mocking

### DevOps
- **Git** - Version control
- **GitHub Actions** - CI/CD
- **Docker** - Containerization

## Deployment Architecture

### Development Environment

```
Local Machine
├── Python Virtual Environment
├── SQLite Database
├── Streamlit Dev Server (port 8501)
└── FastAPI Dev Server (port 8000)
```

### Production Environment (Recommended)

```mermaid
graph LR
    A[Load Balancer] --> B[Web Server 1]
    A --> C[Web Server 2]
    B --> D[Application Server]
    C --> D
    D --> E[(PostgreSQL)]
    D --> F[Redis Cache]
    D --> G[Model Storage]
```

**Components:**
- **Load Balancer**: Nginx or AWS ALB
- **Web Servers**: Gunicorn + Uvicorn workers
- **Application**: Streamlit + FastAPI
- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis for session management
- **Storage**: S3 or local filesystem for models

## Security Considerations

### Data Security
- ✅ All patient data de-identified (HIPAA compliant)
- ✅ Encrypted database connections (SSL/TLS)
- ✅ Secure credential management (environment variables)
- ✅ Input validation and sanitization

### API Security
- 🔄 Authentication (JWT tokens) - *In Progress*
- 🔄 Rate limiting - *Planned*
- ✅ CORS configuration
- ✅ Request validation (Pydantic)

### Application Security
- ✅ No SQL injection (parameterized queries)
- ✅ XSS prevention (Streamlit built-in)
- ✅ CSRF protection
- ✅ Secure file handling

## Scalability Considerations

### Current Capacity
- **Users**: 10-50 concurrent users
- **Data**: 1M+ patient records
- **Predictions**: 1000+ per minute

### Scaling Strategies

**Horizontal Scaling:**
- Add more application servers
- Load balancing across instances
- Stateless application design

**Vertical Scaling:**
- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching

**Database Scaling:**
- Read replicas for analytics
- Partitioning by date/region
- Connection pooling

**Model Serving:**
- Model caching in memory
- Batch prediction endpoints
- Asynchronous processing queue

## Monitoring & Observability

### Logging
- **Application Logs**: Python logging module
- **Access Logs**: Web server logs
- **Error Logs**: Centralized error tracking

### Metrics
- **Performance**: Response times, throughput
- **Model**: Prediction accuracy, drift detection
- **System**: CPU, memory, disk usage

### Alerting
- **Critical**: System failures, data corruption
- **Warning**: Performance degradation, high error rates
- **Info**: Deployment notifications, scheduled tasks

## Future Architecture Enhancements

### Short-Term
- [ ] Implement Redis caching layer
- [ ] Add API authentication (JWT)
- [ ] Set up monitoring dashboard (Grafana)
- [ ] Implement rate limiting

### Medium-Term
- [ ] Microservices architecture
- [ ] Message queue (RabbitMQ/Kafka)
- [ ] Real-time model updates
- [ ] Multi-region deployment

### Long-Term
- [ ] Kubernetes orchestration
- [ ] Service mesh (Istio)
- [ ] Federated learning infrastructure
- [ ] Edge computing for mobile apps

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Maintained By:** Engineering Team
