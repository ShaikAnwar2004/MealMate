# MealMate - Food Delivery App

A Django-based food delivery application with restaurant management, menu browsing, and order processing features.

## Features

- Restaurant management system
- Menu item management
- Customer ordering system
- Shopping cart functionality
- Order processing and tracking
- Payment integration (Razorpay)

## Live Demo

🌐 **Live Application**: [https://web-production-2cb0f.up.railway.app](https://web-production-2cb0f.up.railway.app)

## Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Payment**: Razorpay integration
- **Deployment**: Railway

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ShaikAnwar2004/MealMate.git
cd MealMate
```

2. Navigate to the Django project:
```bash
cd meal_mate
```

3. Create a virtual environment:
```bash
python -m venv env
```

4. Activate the virtual environment:
```bash
# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Start the development server:
```bash
python manage.py runserver
```

9. Open your browser and visit `http://127.0.0.1:8000`

## Project Structure

```
MealMate/
├── meal_mate/                 # Django project directory
│   ├── delivery/             # Main app
│   │   ├── models.py         # Database models
│   │   ├── views.py          # View functions
│   │   ├── urls.py           # URL patterns
│   │   └── templates/        # HTML templates
│   ├── meal_mate/            # Project settings
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py           # Main URL configuration
│   │   └── wsgi.py           # WSGI configuration
│   └── manage.py             # Django management script
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment configuration
└── README.md                 # This file
```

## Deployment

This application is deployed on Railway. The deployment configuration includes:

- **Procfile**: Defines the web process
- **Build Path**: `meal_mate`
- **Environment Variables**: Configured for production

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **Developer**: Shaik Anwar Basha
- **GitHub**: [@ShaikAnwar2004](https://github.com/ShaikAnwar2004)
- **Live App**: [https://web-production-2cb0f.up.railway.app](https://web-production-2cb0f.up.railway.app)
