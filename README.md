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
