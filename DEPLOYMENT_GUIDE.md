# Aedis AI - Deployment Guide

**Version**: 2.0 (WatsonX Integration)  
**Last Updated**: 2026-05-03  
**Status**: ✅ Production Ready

---

## 🚀 Quick Start

### Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] IBM Cloud account created
- [ ] IBM WatsonX project created
- [ ] IBM API Key generated
- [ ] Git installed (for cloning)

---

## 📋 Step-by-Step Deployment

### Step 1: Get IBM WatsonX Credentials

1. **Sign up for IBM Cloud**
   - Go to [IBM Cloud](https://cloud.ibm.com/)
   - Create a free account or log in

2. **Create a WatsonX Project**
   - Navigate to WatsonX.ai service
   - Create a new project
   - Note your **Project ID** (found in project settings)

3. **Generate API Key**
   - Go to IBM Cloud Console → Manage → Access (IAM)
   - Create an API key
   - **IMPORTANT**: Save this key securely - you won't see it again!

4. **Note Your Region URL**
   - Default: `https://us-south.ml.cloud.ibm.com`
   - Other regions: Check IBM Cloud documentation

---

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd Aedis

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3: Configure Environment Variables

**Option A: Using .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env file with your credentials
# Use any text editor (notepad, vim, nano, etc.)
```

Edit `.env` file:
```bash
IBM_API_KEY=your_actual_api_key_here
IBM_PROJECT_ID=your_actual_project_id_here
IBM_URL=https://us-south.ml.cloud.ibm.com
```

**Option B: Using System Environment Variables**

Windows (PowerShell):
```powershell
$env:IBM_API_KEY="your_actual_api_key_here"
$env:IBM_PROJECT_ID="your_actual_project_id_here"
$env:IBM_URL="https://us-south.ml.cloud.ibm.com"
```

macOS/Linux (Bash):
```bash
export IBM_API_KEY="your_actual_api_key_here"
export IBM_PROJECT_ID="your_actual_project_id_here"
export IBM_URL="https://us-south.ml.cloud.ibm.com"
```

---

### Step 4: Generate Sample Data

```bash
# Generate the sample financial database
python data/generate_data.py
```

This creates `data/finance.db` with sample financial data.

---

### Step 5: Verify Installation

```bash
# Run service checker
python -c "from utils.service_checker import ServiceChecker; print(ServiceChecker.get_service_report())"
```

Expected output:
```
Service Availability Report
==================================================
WATSONX_API: ✓ AVAILABLE
  → WatsonX API is accessible
DATABASE: ✓ AVAILABLE
  → Database accessible with X table(s)
DOCUMENTS: ✓ AVAILABLE
  → Documents directory accessible with X file(s)
==================================================
All services are available ✓
```

---

### Step 6: Launch Application

```bash
# Start the Streamlit UI
streamlit run app/main.py
```

The application will:
1. Validate all services
2. Initialize agents
3. Launch the web interface at `http://localhost:8501`

---

## 🔧 Configuration Options

### app/config.py

```python
class Config:
    # Database configuration
    DB_PATH = "data/finance.db"
    
    # Reasoning loop configuration
    MAX_LOOPS = 2                    # Maximum reasoning iterations
    CONFIDENCE_THRESHOLD = 0.8       # Stop when confidence reaches this
    
    # Autonomous mode configuration
    AUTONOMOUS_MODE = True           # Enable/disable autonomous execution
    MAX_ACTIONS_PER_RUN = 2         # Maximum actions per workflow run
    ALLOWED_ACTIONS = ["notify", "report", "simulate"]  # Permitted actions
```

**Customization Tips**:
- Increase `MAX_LOOPS` for more thorough analysis (slower)
- Adjust `CONFIDENCE_THRESHOLD` for quality vs speed tradeoff
- Modify `ALLOWED_ACTIONS` to control what the system can do

---

## 🐛 Troubleshooting

### Issue: "IBM_API_KEY environment variable is not set"

**Solution**:
1. Verify `.env` file exists and contains your credentials
2. If using system variables, ensure they're set in current session
3. Restart your terminal/IDE after setting variables

### Issue: "WatsonX API check failed"

**Possible Causes**:
1. **Invalid API Key**: Regenerate in IBM Cloud Console
2. **Wrong Project ID**: Verify in WatsonX project settings
3. **Insufficient Quota**: Check your IBM Cloud billing/quota
4. **Network Issues**: Check internet connection and firewall

**Debug Steps**:
```bash
# Test API key manually
python -c "import os; print('API Key:', os.getenv('IBM_API_KEY')[:10] + '...')"

# Test project ID
python -c "import os; print('Project ID:', os.getenv('IBM_PROJECT_ID'))"
```

### Issue: "Database file not found"

**Solution**:
```bash
# Regenerate database
python data/generate_data.py
```

### Issue: "ModuleNotFoundError: No module named 'ibm_watsonx_ai'"

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specifically
pip install ibm-watsonx-ai>=0.2.0
```

### Issue: Application crashes on startup

**Debug Steps**:
1. Check Python version: `python --version` (must be 3.8+)
2. Verify all dependencies: `pip list`
3. Check service status: Run service checker (Step 5)
4. Review error logs in terminal

---

## 🔒 Security Best Practices

### ✅ DO:
- Use `.env` file for local development
- Use environment variables in production
- Rotate API keys regularly
- Keep dependencies updated
- Review logs for suspicious activity

### ❌ DON'T:
- Commit `.env` file to version control
- Share API keys in chat/email
- Use production keys in development
- Hardcode credentials in code
- Expose API keys in logs

---

## 📊 Performance Optimization

### For Better Response Times:
1. **Use faster model** (if available in WatsonX)
2. **Reduce MAX_LOOPS** in config
3. **Lower CONFIDENCE_THRESHOLD** slightly
4. **Cache frequent queries** (future enhancement)

### For Better Quality:
1. **Increase MAX_LOOPS** to 3-4
2. **Raise CONFIDENCE_THRESHOLD** to 0.9
3. **Use larger model** (e.g., granite-20b if available)

---

## 🌐 Production Deployment

### Recommended Setup:

1. **Use Docker** (optional but recommended)
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["streamlit", "run", "app/main.py"]
   ```

2. **Use Process Manager**
   ```bash
   # Install PM2 (Node.js required)
   npm install -g pm2
   
   # Start application
   pm2 start "streamlit run app/main.py" --name aedis-ai
   ```

3. **Set Up Reverse Proxy** (Nginx example)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

4. **Enable HTTPS** (Let's Encrypt)
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

---

## 📈 Monitoring

### Key Metrics to Track:
- API response times
- Token usage (for cost management)
- Error rates
- User query patterns
- System resource usage

### Logging:
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.INFO)
```

---

## 💰 Cost Management

### WatsonX Pricing Considerations:
- Charged per token (input + output)
- Granite-13B: ~$X per 1K tokens (check IBM pricing)
- Monitor usage in IBM Cloud Console

### Cost Optimization Tips:
1. Set `max_new_tokens` appropriately (currently 300)
2. Use caching for repeated queries
3. Implement rate limiting
4. Monitor token usage regularly
5. Use smaller models for simple queries

---

## 🔄 Updates and Maintenance

### Updating Dependencies:
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade ibm-watsonx-ai
```

### Backup Strategy:
```bash
# Backup database
cp data/finance.db data/finance.db.backup

# Backup memory store
cp memory_store.json memory_store.json.backup
```

---

## 📞 Support

### Getting Help:
1. Check this deployment guide
2. Review WATSONX_MIGRATION_REVIEW.md
3. Check IBM WatsonX documentation
4. Review application logs
5. Contact IBM support (for API issues)

### Useful Links:
- [IBM WatsonX Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Cloud Console](https://cloud.ibm.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## ✅ Post-Deployment Checklist

- [ ] All services validated successfully
- [ ] Sample query executed successfully
- [ ] Autonomous mode tested
- [ ] Error handling verified
- [ ] Logs reviewed for issues
- [ ] Performance acceptable
- [ ] Security measures in place
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Documentation reviewed

---

## 🎉 Success!

If you've completed all steps and the checklist, your Aedis AI system is now:
- ✅ Fully deployed
- ✅ Production ready
- ✅ Secure
- ✅ Monitored

**Next Steps**:
1. Try sample queries
2. Explore autonomous mode
3. Review generated insights
4. Customize for your use case

---

**Deployment Guide Version**: 2.0  
**Last Updated**: 2026-05-03  
**Maintained By**: Aedis AI Team