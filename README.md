# Coop-Scoop

> **The inside scoop on your next co-op.**

Coop-Scoop is a centralized co-op tracking platform built for Northeastern University students, recruiters, advisors, and administrators. It replaces the fragmented workflow of cross-referencing LinkedIn and NUWorks with a single hub for browsing listings, tracking applications, reading verified peer reviews, and connecting with former co-ops.

---

## Team ISBA

| Name | Email |
|------|-------|
| Isha Nair | nair.i@northeastern.edu |
| Sara Moshirzadeh | moshirzadeh.s@northeastern.edu |
| Branden Smith | smith.brande@northeastern.edu |
| Abigail Oliver | oliver.ab@northeastern.edu |

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [Database Setup](#database-setup)
- [API Overview](#api-overview)

---

## Features

- **Students** — Browse and filter co-op listings, track applications and deadlines, compare offers side-by-side, read verified peer reviews, and access interview question history.
- **Recruiters** — Post listings, manage applicant pipelines, schedule interviews, and view hiring analytics dashboards.
- **Advisors** — Monitor student rosters, flag students who need outreach, write meeting notes, and view cohort-wide placement stats.
- **Admins** — Moderate reviews, manage user accounts, monitor data integrity, and archive completed co-op cycles.

---

## Tech Stack

- **Database**: MySQL
- **Backend**: Python / Flask
- **Frontend**: Python / Streamlit
- **Containerization**: Docker & Docker Compose
- **DB Management**: DataGrip

---

## Project Structure

```
26S-ISBA-CoopScoop/
├── api/                  # Flask REST API
├── app/                  # Streamlit frontend
├── database-files/       # SQL DDL and seed data scripts
├── datasets/             # Datasets used by the application
├── docs/                 # Project documentation
├── ml-src/               # ML model development (notebooks, training scripts)
├── docker-compose.yaml   # Container orchestration
├── sandbox.yaml          # Alternative compose config for personal testing
└── README.md
```

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git
- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)

Create a Python 3.11 environment and install dependencies:

```bash
conda create -n db-proj python=3.11
cd api
pip install -r requirements.txt
cd ../app/src
pip install -r requirements.txt
```

### Clone the Repository

```bash
git clone https://github.com/abbieoliverr/26S-ISBA-CoopScoop.git
cd 26S-ISBA-CoopScoop
```

---

## Environment Variables

Before starting the containers, create a `.env` file inside the `api/` folder based on the provided template:

```bash
cp api/.env.template api/.env
```

Open `api/.env` and set a password on the last line. **Do not reuse passwords from other services.**

> **Note:** The `.env` file is listed in `.gitignore` and must never be committed to version control.

---

## Running with Docker

Once the `.env` file is in place, start all services with:

```bash
docker compose up -d
```

This will spin up a MySQL container, a Flask API container, and a Streamlit app container.

To stop and remove containers:

```bash
docker compose down
```

To restart only a specific service (e.g., the API):

```bash
docker compose up api -d
```

**Personal sandbox testing:** Use `sandbox.yaml` to run containers independently without affecting the shared team repo:

```bash
docker compose -f sandbox.yaml up -d
docker compose -f sandbox.yaml down
```

---

## Database Setup

The database schema and seed data are located in `database-files/`. SQL files in that folder are executed **in alphabetical order** the first time the MySQL container is created.

### Resetting the Database

If you update any `.sql` files, you must recreate the MySQL container — restarting it alone will not re-run the scripts:

```bash
docker compose down db -v && docker compose up db -d
```

This tears down the database container and its volume, then rebuilds it cleanly.

### Schema Highlights

| Table | Description |
|-------|-------------|
| `Users` | Base authentication record for all user types |
| `Students` | Student profiles linked to a co-op cycle and advisor |
| `Advisors` | Co-op advisors with college affiliation |
| `Recruiters` | Recruiters associated with a company |
| `Admins` | Platform administrators |
| `Companies` | Employer records |
| `Listings` | Co-op job postings per company and cycle |
| `Applications` | Student applications to listings |
| `Interviews` | Scheduled interview records |
| `Offers` | Offer outcomes from applications |
| `Reviews` | Peer reviews with moderation approval status |
| `COOPCycle` | Semester cycles (e.g., Spring 2026) |
| `Notes` | Private student application notes |
| `AdvisorNotes` | Advisor-written notes on student profiles |
| `InterviewHistory` | Crowdsourced interview questions by company |

To connect directly via DataGrip or another SQL client, use the credentials set in your `api/.env` file. The default database name is `Coop-Scoop`.

---

## API Overview

The REST API is organized by persona.

| Prefix | Persona |
|--------|---------|
| `/students/...` | Fawn Font — Student |
| `/recruiters/...` | Thiago Goat — Recruiter |
| `/advisors/...` | Dingleford McThunderfunk — Advisor |
| `/admins/...` | Cooper Employ — System Admin |

**Example endpoints:**

```
GET  /students/{id}/applications           # View applications with deadlines
GET  /students/companies/{id}/reviews      # Browse verified peer reviews
POST /recruiters/listings                  # Post a new co-op listing
PUT  /recruiters/applications/{id}/status  # Advance a candidate
GET  /advisors/{id}/students               # View full student roster
PUT  /admins/reviews/{id}/approval         # Approve or reject a review
```
