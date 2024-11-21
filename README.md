# Find-Doc Backend

**Find-Doc** is a backend system developed with a microservices architecture to manage healthcare appointments. This repository contains the core code for four primary services: `user-service`, `provider-service`, `healthbot-service`, and `api-gateway-service`. Each service handles distinct responsibilities, including user authentication and bookings, provider information, a chatbot for user assistance, and centralized API management. The system is designed for scalability and modularity, enabling efficient healthcare appointment management.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Microservices](#microservices)
- [Getting Started](#getting-started)
- [Technologies Used](#technologies-used)

## Overview

This backend codebase provides functionality for a healthcare appointment system that enables users to:

- Search and book appointments with healthcare providers.
- View provider details, including user-submitted reviews.
- Access chatbot support to assist in appointment booking and provider discovery.
- Utilize an API Gateway for centralized access to all services.

## Architecture

This system uses a **microservices architecture** to separate each core function into distinct services:

- **User-Service**: Manages user authentication, booking appointments, and user profiles.
- **Provider-Service**: Maintains provider profiles, including specialties, locations, and reviews.
- **Healthbot-Service**: Provides a chatbot interface that assists users in finding providers based on symptoms and common inquiries.
- **API Gateway Service**: Centralizes API requests, simplifying client interactions by providing a single access point to all services.

Each service operates independently, facilitating easier maintenance, scalability, and modular deployment.

## Microservices

### 1. User-Service

- Handles user registration, login, and authentication.
- Allows users to book appointments and view their booking history.
- Manages user profiles and settings.

### 2. Provider-Service

- Manages healthcare provider profiles, including bios, locations, specialties, and reviews.
- Allows users to view provider details and read user-submitted reviews.

### 3. Healthbot-Service

- Provides a chatbot that guides users through the process of finding suitable healthcare providers.
- Assists users based on symptom queries and other common healthcare inquiries.
- Integrated to streamline the booking experience by directing users to relevant providers.

### 4. API Gateway Service

- Centralizes requests from clients, forwarding them to the appropriate microservices.
- Simplifies client interaction with the backend, ensuring requests are routed efficiently.
- Enhances security by managing access control and request validation for each service.
  This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Features

- [x] Register/Login/Logout
- [x] Hashed passwords
- [x] CSRF protection
- [x] Search providers by location
- [x] Search providers by specialty
- [x] Search providers by insurance
- [x] Book appointments
- [x] Cancel appointments
- [x] home.html
- [ ] login.html
- [x] search.html
- [ ] results.html
- [ ] book.html
- [ ] profile.html
- [ ] Chatbot

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Dataset Used:

September 2024 Data Dissemination From cms.gov

The dataset is updated weekly and a new version is released each month with all the weekly changes made. The most-up-to-date version can be found at the following [link](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination).

## Geocoding Services Used:

Nominatim's free [open-source geocoding](https://nominatim.org/) was used along with data from OpenStreetMap data. Instead of using their rate limited online API, install the database on your local machine.

Installation instructions can be found at this [link](https://nominatim.org/release-docs/latest/admin/Installation/)

Various options are available. Ubuntu 24.04.1 and Postgres 16 were chosen to create the local database for this project. This process may take 24+ hours depending on your system speed. Additionally, only the data necessary to generate accurate addresses was added to the local database. How to filter out data can be found at this [link](https://nominatim.org/release-docs/latest/admin/Import/). The time is based on system specifications listed below this section.

OpenStreetMap data can be downloaded by going to the downloads link at [geofabrik's website](https://www.geofabrik.de/). The dataset used was of the entire United States, us-latest.osm.pbf, and is roughly 9.9 GB. The file must be converted to .csv format before using preprocess.py or filter.py. The process of converting to a .csv and creating a local database takes a lot of storage, it is recommended to have at least 200 GB free on your SSD.

Using default Postgres settings and 11 threads in geocoding.py, 1000 addresses could be geocoded every 3 minutes and 19 seconds.

## System Specifications

CPU: Ryzen 5 3600

RAM: 16 GB DDR4 3200 Mhz

SSD: Corsair Force MP510
