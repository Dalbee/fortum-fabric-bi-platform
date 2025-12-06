## CI/CD Integration for Project 2

This document defines the DevOps workflow for delivering Fabric assets through GitHub and Deployment Pipelines.

---

## 1. Purpose

To provide:

- Automated version control  
- Deployment orchestration  
- Environment separation (Dev → Test → Prod)  
- Quality checks before promotion  
- Safe, audit-ready change management  

---

## 2. Git Integration Workflow

1. Developer works in Fabric Development Workspace  
2. Assets automatically sync to GitHub via Git integration  
3. Pull Requests validate notebook syntax, JSON structure, and YAML configs  
4. Merged changes trigger GitHub Actions workflow  
5. Workflow validates deployment artifacts  
6. Fabric Deployment Pipelines move assets to Test → Prod  

---

## 3. GitHub Repository Structure

project2-fabric-pipeline/
  notebooks/
  pipelines/
  lakehouse/
  docs/
  .github/workflows/


---

## 4. GitHub Actions Template

This workflow validates JSON, YAML, and Python notebook files.

---

## 5. Deployment Pipeline Steps (Fabric)

Each promotion step includes:

1. Notebook validation  
2. Schema comparison  
3. Data quality checks  
4. Approval gate  
5. Promotion to next workspace  

This demonstrates Tech Lead–level governance.
