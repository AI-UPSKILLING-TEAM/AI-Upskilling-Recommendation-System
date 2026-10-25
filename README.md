# AI-Powered Upskilling Recommendation System

## Project ID
22

## Project Description
The AI-Powered Upskilling Recommendation System is designed to analyze a student's skills, courses, projects, certifications, interests, and career goals. The system identifies skill gaps and provides personalized recommendations for courses, learning resources, projects, and certifications.

## Objectives
- Analyze student skills and career goals.
- Identify skill gaps.
- Provide personalized upskilling recommendations.
- Recommend relevant learning resources and projects.
- Track student progress.
- Help students improve their skills based on their career goals.

## Key Features
- Student Registration and Login
- Student Profile Management
- Skill Management
- Career Goal Selection
- Skill Gap Analysis
- AI-Based Recommendations
- Learning Resource Recommendations
- Progress Tracking
- Student Dashboard
- Notifications
- Administrator Management

## Documentation
The Software Requirements Specification (SRS) document is available in this repository.

## Team Members
1. POOJITHA V - PES2UG24AM113
2. MANASA C - PES2UG25AM803
3. SHANMUGA - PES2UG24AM083
4. MANISH S - PES2UG24AM085

## Working prototype (Part-2 implementation)

The current implementation is proposed on [PR #17](https://github.com/AI-UPSKILLING-TEAM/AI-Upskilling-Recommendation-System/pull/17), not yet merged into `main`.

### Run the application
Requires Python 3.10+ with no third-party runtime packages.

```bash
python app.py
# Open http://127.0.0.1:8000
```

### Run automated checks
```bash
python -m unittest discover -s tests -v
```

### Student features
Register, sign in, edit your name/interests/goal, choose known skills, inspect your skill gaps, view content-ranked learning links, add courses/projects/certifications to your learning portfolio, track practice milestones and opt in to in-app notifications.

### Administrator features
For local demonstration, a server operator first registers an admin account then runs:

```bash
python app.py promote-admin admin@example.com
```

Restart/reload the web app and sign in as that promoted account. Admins can view registered student account metadata, add HTTPS learning resources, edit career-role skill requirements, and inspect an audit history. The admin role cannot be granted through public HTTP endpoints.

### Scope and academic evidence
This is a local educational prototype, not a cloud service and not a trained neural recommendation model. The ranking uses TF-IDF and cosine similarity against a small catalog; it is not validated against real student learning outcomes. Do not enter real credentials or private student data.

See:
- [Actual SRS requirement traceability draft](docs/REQUIREMENTS_TRACEABILITY_DRAFT.md)
- [Current Sprint-2 implementation status](docs/SPRINT2_STATUS.md)
- [Test evidence](docs/TEST_EVIDENCE.md)
- [Recommendations methodology and limitations](docs/RECOMMENDER_METHOD_AND_LIMITS.md)
- [Demo recording guide](docs/DEMO_RECORDING_GUIDE.md)
- [Release checklist](docs/RELEASE_AND_FREEZE_CHECKLIST.md)

**Open acceptance work:** Team review of PR #17, confirmation against original SAD/Test Plan, GitHub Project board linking, and recording/uploading the authentic 1-minute and 2-minute demo videos.
