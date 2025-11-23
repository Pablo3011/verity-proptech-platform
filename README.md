# VERITY - AI-Powered GCC Real Estate Platform

 Production-ready PropTech platform with AI valuations, property listings, and market analytics.

## 🚀 Features

- **AI Valuation Engine**: ML-powered property valuations
- **Multi-Country Support**: UAE, Saudi Arabia, Qatar, Egypt
- **Real-time Search**: Advanced property filtering
- **Developer Dashboard**: Property management
- **Market Analytics**: GCC market insights
- **Space-Efficient Ad Banners**: Revenue-generating ads

## 🛠 Tech Stack

**Backend:**
- FastAPI (Python 3.11)
- Pydantic for data validation
- Uvicorn ASGI server
- Docker containerization

**Frontend:**
- Pure HTML5/CSS3/JavaScript
- Modern responsive design
- No framework dependencies

## 📦 Deployment

### Railway Deployment (Recommended)

1. **Connect to Railway:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Link to your project
   railway link
   ```

2. **Deploy Backend:**
   ```bash
   # Railway will automatically detect Dockerfile
   railway up
   
   # Get your deployment URL
   railway domain
   ```

3. **Environment Variables:**
   Set these in Railway dashboard:
   ```
   PORT=8000
   ```

### Docker Deployment

```bash
# Build the image
docker build -t verity-backend .

# Run the container
docker run -p 8000:8000 verity-backend
```

### Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the server
python main.py
```

Backend will be available at `http://localhost:8000`

## 🌐 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/properties` - List all properties
- `GET /api/properties/{id}` - Get specific property
- `GET /api/properties/search/{query}` - Search properties
- `POST /api/properties` - Create new property
- `POST /api/valuations` - Get AI valuation
- `GET /api/stats` - Platform statistics
- `GET /api/developers` - List developers

## 📱 Frontend Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Netlify

Drag and drop the `public/` folder to Netlify dashboard

## 🔧 Configuration

Update the backend URL in frontend files:

```javascript
// In public/app.js
const API_URL = 'https://your-railway-url.up.railway.app';
```

## 📊 Sample Data

The backend includes sample properties from:
- 🇦🇪 UAE (Dubai, Abu Dhabi)
- 🇶🇦 Qatar (Doha)
- 🇸🇦 Saudi Arabia (Riyadh, Jeddah)
- 🇪🇬 Egypt (Cairo, North Coast)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Links

- **Live Demo**: Coming soon
- **API Docs**: `your-url/docs`
- **GitHub**: https://github.com/Pablo3011/verity-proptech-platform

## 📞 Support

For support, email: support@verity-platform.com

---

**Built with ❤️ for the GCC Real Estate Market**