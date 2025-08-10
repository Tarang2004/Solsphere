# Solsphere: Cross-Platform System Utility + Admin Dashboard

## 🎯 Overview

Solsphere is a comprehensive system monitoring solution that includes:

- **System Utility**: Cross-platform client that collects system health data
- **Backend API**: FastAPI server that stores and manages system data
- **Admin Dashboard**: Vue.js web interface for monitoring and reporting

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   System        │    │   Backend       │    │   Frontend      │
│   Utility       │───▶│   API Server    │◀───│   Dashboard     │
│   (Client)      │    │   (FastAPI)     │    │   (Vue.js)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/solsphere.git
cd solsphere
```

### 2. Start the Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Start the Frontend

```bash
# In a new terminal
npm install
npm run dev
```

The dashboard will be available at `http://localhost:3000`

### 4. Install and Run the System Utility

```bash
cd system_utility
pip install -r requirements.txt

# Run a single health check
python main.py --single-check

# Or run as a background daemon
python main.py --daemon --check-interval 30
```

## 📦 Detailed Setup

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=sqlite:///./solsphere.db
   SECRET_KEY=your-secret-key-change-in-production
   ```

3. **Run the Server**
   ```bash
   python main.py
   ```

4. **API Documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Development Mode**
   ```bash
   npm run dev
   ```

3. **Production Build**
   ```bash
   npm run build
   npm run serve
   ```

### System Utility Setup

1. **Install Dependencies**
   ```bash
   cd system_utility
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Set `SOLSPHERE_API_ENDPOINT` environment variable if needed
   - Default endpoint: `http://localhost:8000`

3. **Usage Options**
   ```bash
   # Single health check
   python main.py --single-check
   
   # Background daemon (30-minute intervals)
   python main.py --daemon --check-interval 30
   
   # Custom API endpoint
   python main.py --api-endpoint https://your-api.com
   ```

## 🔧 Configuration

### Backend Configuration

The backend can be configured via environment variables:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `CHECK_INTERVAL_MINUTES`: Default check interval

### Frontend Configuration

The frontend connects to the backend API. Update the API endpoint in the store files if needed.

### System Utility Configuration

- `SOLSPHERE_API_ENDPOINT`: API server URL
- `SOLSPHERE_CHECK_INTERVAL`: Check interval in minutes

## 📊 Features

### System Health Checks

- **Disk Encryption**: BitLocker (Windows), FileVault (macOS), LUKS (Linux)
- **OS Updates**: Windows Update, macOS Software Update, Linux package updates
- **Antivirus**: Windows Security Center, common AV tools detection
- **Sleep Settings**: Power management configuration validation
- **System Metrics**: CPU, memory, disk usage monitoring

### Admin Dashboard

- **Real-time Monitoring**: Live system status updates
- **Compliance Reporting**: Automated compliance checking
- **Issue Management**: Centralized issue tracking and resolution
- **Export Functionality**: CSV and JSON data export
- **Filtering & Search**: Advanced machine and issue filtering

### API Endpoints

- `POST /api/machines`: Register/update machine health data
- `GET /api/machines`: List all machines with filtering
- `GET /api/dashboard/stats`: Dashboard statistics
- `GET /api/dashboard/compliance`: Compliance overview
- `GET /api/export/machines`: Export machine data as CSV

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
npm run test
```

### System Utility Tests

```bash
cd system_utility
pytest
```

## 📁 Project Structure

```
solsphere/
├── backend/                 # FastAPI backend server
│   ├── main.py            # Main application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── auth.py            # Authentication
│   ├── config.py          # Configuration
│   └── database.py        # Database setup
├── src/                    # Vue.js frontend
│   ├── views/             # Page components
│   ├── stores/            # Pinia stores
│   ├── router/            # Vue Router
│   └── App.vue            # Main app component
├── system_utility/         # Cross-platform client
│   ├── main.py            # Main utility script
│   ├── requirements.txt    # Python dependencies
│   └── setup.py           # Installation script
├── package.json            # Frontend dependencies
├── requirements.txt        # Backend dependencies
└── README.md              # This file
```

## 🚀 Deployment

### Production Considerations

1. **Security**
   - Use HTTPS in production
   - Change default secret keys
   - Implement proper authentication
   - Use environment variables for sensitive data

2. **Database**
   - Use PostgreSQL or MySQL for production
   - Implement database migrations
   - Set up backup procedures

3. **Monitoring**
   - Set up application monitoring
   - Configure logging aggregation
   - Implement health checks

4. **Scaling**
   - Use load balancers for multiple backend instances
   - Implement caching strategies
   - Consider message queues for high-volume deployments

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the docs folder
- **Email**: admin@solsphere.com

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Cross-platform system utility
- FastAPI backend with SQLite database
- Vue.js admin dashboard
- Comprehensive health monitoring
- Background daemon support
- Real-time status updates
- Compliance reporting
- Export functionality

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Vue.js for the reactive frontend framework
- Tailwind CSS for the utility-first CSS framework
- All contributors and supporters


