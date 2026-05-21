# Argos - Web Scraping & News Aggregation System

Argos is a FastAPI-based web scraping and news aggregation system designed to collect, process, and manage news articles from multiple sources. It provides a modern, asynchronous architecture for running scraping jobs with support for filtering, logging, and persistent storage.

## 🎯 Project Overview

Argos enables users to:

- **Create scraping jobs** targeting specific keywords across multiple news sources
- **Monitor job progress** in real-time with status tracking
- **Retrieve aggregated news** from various sources (Caraguatatuba, Ubatuba, São Sebastião, Periódicos CAPES)
- **Filter results** by keywords and publication year
- **Persist job history** for future reference

## 🏗️ Architecture

### Core Components

#### **Core Module** (`core/`)

- **config.py**: Configuration constants
  - `STORAGE_FILE`: Persistent storage location for job history
  - `MAX_SIMULTANEOUS_JOBS`: Controls concurrent job execution (default: 2)
- **state.py**: Global application state management
  - Task tracking and synchronization
  - Background task management
  - Semaphore-based concurrency control

#### **Models** (`models/`)

- **job.py**: Data models for job requests and responses
  - `JobRequest`: Defines scraping parameters (title, sites, depth)
  - `JobResponse`: Returns job details with results
- **noticia.py**: News article data model
  - Represents scraped news with title, date, year, link, summary, and source

#### **Routes** (`routes/`)

- **jobs.py**: Job management API endpoints
  - `POST /jobs/` - Create a new scraping job
  - `GET /jobs/` - Retrieve all jobs
  - `GET /jobs/{id}` - Get specific job details
- **status.py**: Job status monitoring endpoints
  - `GET /status/{id}` - Get job status
  - `GET /status/completed/{id}` - Check if job is completed

#### **Services** (`services/`)

##### Job Management

- **job_service.py**: Core job execution logic
  - `run_job()`: Executes scraping with semaphore control
  - `update_job()`: Updates job status with thread-safe locking
  - `persist_tasks()`: Saves job state to storage
- **task_storage.py**: Persistent storage operations
  - `load_tasks()`: Loads job history from file
  - `save_tasks_snapshot()`: Saves job state with atomic operations

##### Scraping System (`services/scrapers/`)

- **scraper_service.py**: Main service orchestrating multiple scrapers
  - Strategy pattern implementation for extensible scraper support
  - Supports 4 built-in scraper sources:
    - `CaraguatatubaScraper`: Caraguatatuba local news
    - `UbatubaScraper`: Ubatuba local news
    - `SaoSebastiaoScraper`: São Sebastião local news
    - `PeriodicosCapesScraper`: Academic journals (CAPES Periodicals)
- **scraper_base.py**: Abstract base class for scraper implementations
- Individual scrapers: `caraguatatuba.py`, `ubatuba.py`, `sao_sebastiao.py`, `periodicos_capes.py`

##### Filtering System (`services/filters/`)

- **filter_service.py**: Multi-strategy filtering engine
  - Chainable filters for flexible result processing
  - Logs filter matches and exclusions
- **filters_base.py**: Abstract base class for filter strategies
- **keyword_filter.py**: Filters news by keyword matches
- **year_filter.py**: Filters news by publication year

##### Logging System (`services/logging/`)

- **logger_service.py**: Centralized logging configuration
  - File and console output
  - Structured logging with timestamps
  - Configurable log levels

#### **Frontend** (`templates/` & `static/`)

- **index.html**: Main web interface
  - Job creation form
  - Job list and status display
  - Real-time job monitoring
- **static/**: Static assets
  - `bootstrap.min.css`: Bootstrap 5 styling
  - Logo and icon assets (`logo.png`, `logo-extended.png`, `icon.png`)

#### **Main Application** (`server.py`)

- FastAPI application setup
- Static file serving
- Template rendering
- Route registration
- Uvicorn development server configuration

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:

   ```bash
   python server.py
   ```

   The server will start on `http://localhost:8000`

### Web Interface

- Navigate to `http://localhost:8000` to access the web interface
- Create a new scraping job by specifying:
  - **Title**: Search keyword/topic
  - **Sites**: Select news sources to scrape
  - **Profundidade** (Depth): Search depth level (default: 3)
- Monitor job progress and retrieve results in real-time

## 📦 Key Dependencies

| Package              | Purpose                       |
| -------------------- | ----------------------------- |
| **FastAPI**          | Web framework for REST API    |
| **Uvicorn**          | ASGI server                   |
| **Pydantic**         | Data validation               |
| **Jinja2**           | Template rendering            |
| **Beautiful Soup 4** | HTML parsing and web scraping |
| **Requests**         | HTTP client                   |
| **lxml**             | XML/HTML processing           |
| **Pandas**           | Data processing               |

## 🔄 Job Processing Flow

1. **Job Creation** → POST `/jobs/` with scraping parameters
2. **Task Storage** → Job stored with UUID and unique ID
3. **Async Execution** → Job queued with semaphore control (max 2 concurrent)
4. **Scraping** → Multiple sources processed in parallel
5. **Filtering** → Results filtered by specified criteria
6. **Persistence** → Results saved to `job_history.json`
7. **Status Updates** → Client monitors via status endpoints

## 📊 Job States

| State        | Description                 |
| ------------ | --------------------------- |
| `created`    | Job created but not started |
| `processing` | Job actively running        |
| `completed`  | Job finished successfully   |
| `failed`     | Job encountered an error    |

## 🔒 Concurrency & Thread Safety

- **Semaphore-based control**: Maximum 2 simultaneous jobs
- **Async locks**: Thread-safe task dictionary operations
- **Background tasks**: Managed via asyncio task set
- **Atomic file operations**: Safe job state persistence

## 📁 Project Structure

```
.
├── core/
│   ├── config.py          # Configuration constants
│   └── state.py           # Global application state
├── models/
│   ├── job.py             # Job data models
│   └── noticia.py         # News article model
├── routes/
│   ├── jobs.py            # Job management endpoints
│   └── status.py          # Status monitoring endpoints
├── services/
│   ├── job_service.py     # Job execution logic
│   ├── task_storage.py    # Persistence operations
│   ├── scrapers/          # Web scraping implementations
│   │   ├── scraper_service.py
│   │   ├── scraper_base.py
│   │   ├── caraguatatuba.py
│   │   ├── ubatuba.py
│   │   ├── sao_sebastiao.py
│   │   └── periodicos_capes.py
│   ├── filters/           # Result filtering logic
│   │   ├── filter_service.py
│   │   ├── filters_base.py
│   │   ├── keyword_filter.py
│   │   └── year_filter.py
│   └── logging/           # Logging configuration
│       └── logger_service.py
├── templates/
│   ├── index.html         # Web interface
│   └── bkpindex.html      # Backup template
├── static/
│   ├── bootstrap.min.css  # Bootstrap styling
│   ├── logo.png
│   ├── logo-extended.png
│   ├── icon.png
│   └── web.png
├── server.py              # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── job_history.json       # Persistent job storage
└── README.md             # This file
```

## 🛠️ API Reference

### Jobs Endpoints

#### Create Job

```http
POST /jobs/
Content-Type: application/json

{
  "title": "Climate change",
  "sites": ["ubatuba", "caraguatatuba"],
  "profundidade": 3
}
```

**Response:**

```json
{
  "status": "created",
  "job_hash": "uuid-string",
  "job_id": 1,
  "data": []
}
```

#### List All Jobs

```http
GET /jobs/
```

#### Get Job Details

```http
GET /jobs/{job_hash}
```

### Status Endpoints

#### Get Job Status

```http
GET /status/{job_hash}
```

**Response:**

```json
{
  "status": "processing",
  "title": "Climate change"
}
```

#### Check if Job Complete

```http
GET /status/completed/{job_hash}
```

**Response:**

```json
{
  "completed": true
}
```

## 🎨 Design Patterns Used

- **Strategy Pattern**: Multiple scraper and filter implementations
- **Singleton Pattern**: Global state management
- **Async/Await**: Non-blocking I/O operations
- **Repository Pattern**: Task storage abstraction
- **Service Layer**: Business logic separation

## 📝 Configuration

Edit `core/config.py` to modify:

- Storage file location
- Maximum concurrent jobs

## 🔍 Logging

Logs are written to `logs/` directory with both file and console output.
Log level can be configured in `services/logging/logger_service.py`.

## 📄 Data Persistence

Job history is persisted to `job_history.json` using atomic file operations:

- Temporary file created during write
- Atomic rename ensures data integrity
- UTF-8 encoding for special characters support

## 🤝 Contributing

To add a new news source:

1. Create a new scraper class in `services/scrapers/`
2. Inherit from `ScraperStrategy` base class
3. Implement the `scrape()` method
4. Register in `ScraperService.__strategies`

To add a new filter:

1. Create a filter class in `services/filters/`
2. Inherit from `FilterStrategy` base class
3. Implement the `filter_match()` method
4. Chain filters in `FilterService`

## 📜 License

[Add license information here]

## 📧 Contact

For questions or support, please reach out to the project maintainer.
