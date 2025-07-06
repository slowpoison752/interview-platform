from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import PyPDF2
import io
import re
from typing import Dict, Any
import json
import os

app = FastAPI(title="Resume Parser API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Railway deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files if they exist (but not for API routes)
if os.path.exists("/app/static"):
    app.mount("/static", StaticFiles(directory="/app/static"), name="static")

@app.get("/", response_class=FileResponse)
async def serve_index():
    """Serve the main HTML page"""
    if os.path.exists("/app/static/index.html"):
        return FileResponse("/app/static/index.html")
    return {"message": "Resume Parser Platform is running!"}

def extract_text_from_pdf(pdf_file: bytes) -> str:
    """Extract text from PDF bytes"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def parse_resume_sections(text: str) -> Dict[str, Any]:
    """Parse resume text into structured sections"""
    sections = {
        "contact_info": {},
        "summary": "",
        "experience": [],
        "education": [],
        "skills": [],
        "projects": []
    }
    
    # Extract contact information (basic patterns)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    if emails:
        sections["contact_info"]["email"] = emails[0]
    if phones:
        sections["contact_info"]["phone"] = ''.join(phones[0])
    
    # Extract skills (common tech skills)
    skill_keywords = [
        "Python", "Java", "JavaScript", "React", "Node.js", "SQL", "MongoDB", 
        "AWS", "Docker", "Kubernetes", "Git", "Machine Learning", "Data Science",
        "Apache Spark", "Hadoop", "Kafka", "Redis", "PostgreSQL", "MySQL",
        "FastAPI", "Django", "Flask", "TypeScript", "Angular", "Vue.js",
        "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib"
    ]
    
    found_skills = []
    for skill in skill_keywords:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    
    sections["skills"] = found_skills
    
    # Generate summary
    lines = text.split('\n')
    summary_lines = []
    for line in lines[:10]:  # First 10 lines often contain summary
        if len(line.strip()) > 20 and len(line.strip()) < 200:
            summary_lines.append(line.strip())
    
    sections["summary"] = " ".join(summary_lines[:3])  # First 3 meaningful lines
    
    return sections

def generate_context_summary(sections: Dict[str, Any]) -> str:
    """Generate a human-readable context summary"""
    summary_parts = []
    
    if sections["contact_info"].get("email"):
        summary_parts.append(f"Contact: {sections['contact_info']['email']}")
    
    if sections["skills"]:
        summary_parts.append(f"Key Skills: {', '.join(sections['skills'][:10])}")
    
    if sections["summary"]:
        summary_parts.append(f"Summary: {sections['summary']}")
    
    return "\n\n".join(summary_parts)

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume PDF"""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read file content
        content = await file.read()
        
        # Extract text from PDF
        text = extract_text_from_pdf(content)
        
        # Parse sections
        sections = parse_resume_sections(text)
        
        # Generate context summary
        context_summary = generate_context_summary(sections)
        
        return JSONResponse(content={
            "filename": file.filename,
            "raw_text": text[:500] + "..." if len(text) > 500 else text,  # Truncated for response
            "sections": sections,
            "context_summary": context_summary,
            "message": "Resume parsed successfully!"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Resume Parser Platform is running!"}

@app.get("/api")
async def api_root():
    return {"message": "Resume Parser API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy", 
        "message": "Resume Parser API is running!",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def api_health_check():
    """API health check endpoint"""
    return {
        "status": "healthy", 
        "message": "Resume Parser API is running!",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "status": "ready",
        "message": "Application is ready to accept requests",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 