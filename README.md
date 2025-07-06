# Resume Parser Platform

A modern web application that allows users to upload their resume in PDF format and get instant insights and context about their professional profile.

## Features

- 📄 PDF Resume Upload
- 🔍 Automatic Text Extraction
- 📧 Contact Information Detection
- 🛠️ Skills Recognition
- 📝 Summary Generation
- 🎨 Modern, Responsive UI

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React.js
- **PDF Processing:** PyPDF2
- **Styling:** CSS3 with modern gradients

## Quick Start

### Option 1: Docker (Recommended)

1. **Prerequisites:**
   - Docker and Docker Compose installed

2. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Option 2: Local Development

**Prerequisites:**
- Python 3.8+
- Node.js 16+
- npm or yarn

**Backend Setup:**
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   python main.py
   ```

The backend will be running at `http://localhost:8000`

**Frontend Setup:**
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

The frontend will be running at `http://localhost:3000`

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Click "Choose PDF file" to select your resume
3. Click "Parse Resume" to process the file
4. View the extracted information including:
   - Contact details
   - Key skills
   - Summary
   - Raw text preview

## API Endpoints

- `POST /api/upload-resume` - Upload and parse a PDF resume
- `GET /` - Health check endpoint
- `GET /health` - Health check endpoint (for Railway)

## Project Structure

```
interview-platform/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend Docker configuration
├── frontend/
│   ├── public/
│   │   └── index.html      # Main HTML file
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styles
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend Docker configuration
│   └── nginx.conf          # Nginx configuration
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Root Dockerfile for Railway
├── railway.json            # Railway deployment configuration
└── README.md
```

## Deployment

### Railway Deployment

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize Railway project:**
   ```bash
   railway init
   ```

4. **Deploy to Railway:**
   ```bash
   railway up
   ```

5. **Get your deployment URL:**
   ```bash
   railway domain
   ```

### Docker Commands

- **Build and run locally:**
  ```bash
  docker-compose up --build
  ```

- **Stop services:**
  ```bash
  docker-compose down
  ```

- **View logs:**
  ```bash
  docker-compose logs -f
  ```

## Future Enhancements

- [ ] Experience timeline extraction
- [ ] Education details parsing
- [ ] Project portfolio analysis
- [ ] Skills gap analysis
- [ ] Resume scoring and suggestions
- [ ] Export to different formats
- [ ] AI-powered insights

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License 