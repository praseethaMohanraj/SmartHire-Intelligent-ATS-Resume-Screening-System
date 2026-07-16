<p align="center">
  <img src="Screenshot/banner.png" alt="SmartHire Banner" width="100%">
</p>

<h1 align="center">🚀 SmartHire – Intelligent ATS Resume Screening System</h1>

<p align="center">
A web-based Applicant Tracking System (ATS) that streamlines resume screening by matching candidate skills with job requirements and generating ATS scores to support efficient candidate shortlisting.
</p

An AI-powered Applicant Tracking System (ATS) that automates resume screening by matching candidate skills against job requirements and generating intelligent ranking scores. Built using Python, Streamlit, SQLite, HTML/CSS, and JSON.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

## 📑 Table of Contents

- Overview
- Problem Statement
- Solution
- Features
- Technology Stack
- System Architecture
- Project Screenshots
- Installation
- Usage
- Folder Structure
- Future Enhancements
- License

## 📖 Overview

Recruitment teams often spend considerable time manually reviewing resumes, making the hiring process slow and inconsistent. SmartHire automates this process by analyzing resumes, extracting candidate skills, comparing them with job-specific requirements, and generating ATS scores to identify the most suitable candidates.

The application provides an intuitive web interface that allows recruiters to upload multiple resumes, select a target job role, view ranked results, manage uploaded resumes, and generate reports. The system significantly reduces manual effort while improving consistency and transparency in candidate evaluation.

## 🎯 Problem Statement

Organizations receive hundreds of resumes for every job opening, making manual screening inefficient and time-consuming.

Challenges include:

- Manual resume evaluation is slow.
- Human bias can affect candidate selection.
- Important candidates may be overlooked.
- Lack of standardized evaluation criteria.
- Difficulty in handling large volumes of applications.

## 💡 Solution

SmartHire provides an intelligent ATS platform that:

- Extracts text from uploaded PDF resumes.
- Identifies technical skills.
- Matches extracted skills with predefined job-role requirements.
- Calculates an ATS compatibility score.
- Ranks candidates based on their scores.
- Stores resume information in a local database.
- Provides recruiter-friendly dashboards for managing resumes.

## ✨ Key Features

- 📄 Upload multiple PDF resumes
- 🎯 Job-role specific skill matching
- 🧠 Intelligent ATS scoring
- 📊 Resume ranking based on compatibility
- 🗂 Resume database management
- 🗑 Delete stored resumes
- 📈 Reports dashboard
- 💻 Responsive Streamlit interface
- ⚡ Fast resume processing
- 🔒 Local SQLite database storage

  ## 🛠 Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend development |
| Streamlit | User Interface |
| SQLite | Database |
| HTML/CSS | UI Styling |
| JSON | Skill datasets |
| Git | Version Control |
| GitHub | Repository Hosting |

## 🏗️ System Architecture

                   +----------------------+
                   |     Recruiter        |
                   +----------+-----------+
                              |
                              v
                    Streamlit Web Interface
                              |
        +---------------------+----------------------+
        |                     |                      |
        v                     v                      v
 Resume Upload         Job Role Selection     Admin Dashboard
        |                     |                      |
        +---------------------+----------------------+
                              |
                              v
                  Resume Parsing & Skill Extraction
                              |
                              v
                  ATS Skill Matching Algorithm
                              |
                              v
                 Candidate Score Calculation
                              |
                              v
              SQLite Database & JSON Storage
                              |
                              v
          Ranked Candidates & Reports Dashboard


## 📸 Project Screenshots

### 🏠 Home Page

<p align="center">
<img src="Screenshot/home.png" width="900">
</p>

---

### 📊 Admin Dashboard

<p align="center">
<img src="Screenshot/dashboard.png" width="900">
</p>

---

### 📈 Reports

<p align="center">
<img src="Screenshot/reports.png" width="900">
</p>

---

### 🗑 Delete Resume

<p align="center">
<img src="Screenshot/delete.png" width="900">
</p>
