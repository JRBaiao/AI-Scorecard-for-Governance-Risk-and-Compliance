# AI Procurement Scorecard – GRC Platform

## Overview

The **AI Procurement Scorecard** is a Governance, Risk, and Compliance (GRC) web application designed to support organizations in evaluating AI vendors and AI systems against regulatory and compliance requirements. The platform streamlines the procurement assessment process by guiding evaluators through a structured workflow based on AI risk classification and compliance verification.

The application focuses on helping procurement teams, compliance officers, and risk managers assess whether an AI system aligns with governance standards and procurement policies before deployment.

---

## Key Features

### Vendor Information Collection

The platform allows evaluators to register detailed vendor and AI system information, including:

* Vendor name and headquarters country
* Vendor contact information
* AI system or product name
* Version and release details
* System description
* Procurement sector classification

### AI Risk Classification

The application incorporates an AI risk classification workflow inspired by modern AI governance frameworks. Evaluators can classify systems into categories such as:

* Prohibited Risk
* High Risk
* Limited Risk
* Minimal Risk

This helps organizations determine the level of scrutiny and compliance requirements needed for each AI solution.

### Compliance Assessment Engine

The platform provides a structured questionnaire system for evaluating AI systems across multiple governance domains, including:

* Risk Management System
* Data & Data Governance
* Technical Documentation
* Record-Keeping & Logging
* Transparency & Information

Each assessment item supports:

* Yes / Partial / No / N/A responses
* Evidence and notes fields
* Procurement guidance references

### Automated Compliance Scoring

At the end of the evaluation workflow, the platform generates:

* Overall compliance percentage
* Category-by-category performance breakdown
* AI risk classification summary
* Procurement recommendation

The results page provides a centralized view of the AI system’s compliance posture.

### Step-by-Step Evaluation Workflow

The application uses a guided 4-step process:

1. Vendor Information
2. Risk Classification
3. Compliance Assessment
4. Scorecard & Results

This wizard-style approach improves usability and ensures evaluators follow a consistent assessment methodology.

---

## Purpose of the Project

This project was created to demonstrate how AI governance and procurement processes can be digitized into a structured compliance workflow. The platform aims to:

* Improve transparency in AI procurement
* Support regulatory readiness
* Standardize vendor evaluation processes
* Reduce procurement risk
* Assist organizations in documenting compliance decisions

---

## Technologies Used

Depending on your implementation, update this section accordingly.

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Django / Flask *(update if necessary)*

### Database

* SQLite / PostgreSQL *(update if necessary)*

### Additional Concepts

* Governance, Risk & Compliance (GRC)
* AI Risk Assessment
* Procurement Governance
* Regulatory Compliance Workflows

---

## Example Workflow

### Step 1 – Vendor Registration

The evaluator enters vendor details and AI system information.

### Step 2 – Risk Classification

The AI solution is categorized based on potential risk level.

### Step 3 – Compliance Assessment

The evaluator answers governance and compliance questions while attaching evidence and notes.

### Step 4 – Results Generation

The system generates a final compliance scorecard and procurement recommendation.

---

## Future Improvements

Potential enhancements for the platform include:

* User authentication and role-based access control
* Exportable PDF compliance reports
* Dashboard analytics and visualization
* Integration with regulatory databases
* AI-assisted compliance recommendations
* Audit trail and activity logging
* Multi-language support
* API integration for procurement systems

---

## Screenshots
```md
```[Scorecard – Microsoft – EU AI Act.pdf](https://github.com/user-attachments/files/27751248/Scorecard.Microsoft.EU.AI.Act.pdf)
---

## Installation

```bash
# Clone the repository
git clone https://github.com/JRBaiao/AI-Scorecard-for-Governance, Risk, and Compliance.git

# Navigate into the project folder
cd AI-Scorecard-for-Governance, Risk, and Compliance

# Install dependencies
pip install -r requirements.txt

# Run the application
python manage.py runserver
```

---

## Project Structure

```bash
project/
│
├── frontend/
├── backend/
├── templates/
├── static/
├── database/
├── requirements.txt
└── README.md
```

---

## Use Cases

This platform can be used by:

* Government procurement departments
* Compliance and governance teams
* Risk management professionals
* AI auditing teams
* Organizations implementing AI governance frameworks
* Public-sector procurement evaluators

