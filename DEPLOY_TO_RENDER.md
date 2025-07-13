# 🚀 Deploy to Render - Step by Step Guide

Your AI Agent system is now ready for production deployment on Render!

## 📋 **Pre-Deployment Checklist**

✅ **Files Created for Render:**
- `Procfile` - Tells Render how to start your app
- `runtime.txt` - Specifies Python version
- `render.yaml` - Render configuration (optional)
- `.env.production` - Production environment template

✅ **Code Updated:**
- Environment-aware CORS settings
- Production-ready configurations
- Health check endpoint available
- Clean package.json scripts

## 🌐 **Step 1: Prepare Your Repository**

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "feat: Add Render deployment configuration"
   git push origin main
   ```

2. **Make sure your repo is public or connect Render to your GitHub**

## 🔧 **Step 2: Create Render Service**

1. **Go to [Render Dashboard](https://dashboard.render.com)**

2. **Click "New" → "Web Service"**

3. **Connect your GitHub repository:**
   - Repository: `aaryyang/agentic-ai`
   - Branch: `main`

4. **Configure the service:**
   ```
   Name: agentic-ai-crm
   Runtime: Python 3
   Build Command: pip install --upgrade pip setuptools wheel && pip install --only-binary=:all: --prefer-binary -r requirements.txt
   Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```

## 🔑 **Step 3: Set Environment Variables**

In Render Dashboard → Environment, add these variables:

### **Required Variables:**
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
SECRET_KEY=your_production_secret_key_make_it_long_and_secure
```

### **API Security (Optional):**
```
API_KEY=your_secure_api_key_for_crm_integration
REQUIRE_API_KEY=false
```
*Set REQUIRE_API_KEY=true if you want to secure the API endpoints*

### **Production Settings:**
```
DEBUG=false
DEVELOPMENT_MODE=false
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-deployed-app.onrender.com
```

### **Optional Integrations:**
```
TELEGRAM_BOT_TOKEN=your_telegram_token_here
WHATSAPP_API_TOKEN=your_whatsapp_token_here
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
```

## 🚀 **Step 4: Deploy**

1. **Click "Create Web Service"**
2. **Render will automatically:**
   - Install dependencies from `requirements.txt`
   - Start your app using the `Procfile`
   - Assign a URL: `https://your-app-name.onrender.com`

## ✅ **Step 5: Verify Deployment**

Once deployed, test these endpoints:

1. **Health Check:**
   ```
   GET https://your-app-name.onrender.com/health
   ```

2. **Landing Page:**
   ```
   GET https://your-app-name.onrender.com/
   ```

3. **API Documentation:**
   ```
   GET https://your-app-name.onrender.com/docs
   ```

4. **AI Agent Chat:**
   ```
   POST https://your-app-name.onrender.com/agent/chat
   {
     "message": "Hello, can you help me?",
     "user_id": "test_user"
   }
   ```

## 🔗 **Step 6: CRM Integration**

Once deployed, your CRM can connect to:

**Base URL:** `https://your-app-name.onrender.com`

**Key Endpoints:**
- `POST /agent/chat` - Direct agent interaction
- `POST /agent/delegate` - Specialist agent tasks
- `POST /webhooks/crm` - CRM webhook receiver

**Example Integration:**
```javascript
// From your CRM workflow
fetch('https://your-app-name.onrender.com/agent/delegate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    agent_type: 'sales',
    task: 'Qualify this lead: John Doe from Acme Corp',
    context: {lead_id: '12345', source: 'hubspot'}
  })
})
```

## 🔒 **Security Best Practices**

1. **Use strong SECRET_KEY** (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

2. **Set proper CORS_ORIGINS** to your actual domains only

3. **Store sensitive data** in Render environment variables, never in code

4. **Enable HTTPS** (Render provides this automatically)

## 📊 **Monitoring & Logs**

- **View logs:** Render Dashboard → Your Service → Logs
- **Monitor health:** Use the `/health` endpoint
- **Check metrics:** Available in Render Dashboard

## 🔄 **Auto-Deploy**

Render will automatically redeploy when you push to your main branch:

```bash
git add .
git commit -m "Update: feature improvement"
git push origin main
# 🚀 Render automatically deploys!
```

## 🎯 **Your Live AI Agent System**

After deployment, you'll have:
- ✅ **Live API** accessible worldwide
- ✅ **Web dashboard** for testing
- ✅ **CRM integration ready** endpoints
- ✅ **WhatsApp/Telegram** webhook support
- ✅ **Automatic deployments** on code changes
- ✅ **Professional URLs** for integration

**Your AI Agent system is now production-ready!** 🎉

## 🆘 **Troubleshooting**

**Build fails with dependency conflicts?**
- Quick fix: Use minimal requirements
  ```bash
  git mv requirements.txt requirements-full.txt
  git mv requirements-production.txt requirements.txt
  git commit -m "fix: use minimal requirements for Render"
  git push origin main
  ```

**Build fails?**
- Check `requirements.txt` for any problematic packages
- Ensure Python version matches `runtime.txt`

**App crashes?**
- Check Render logs for error details
- Verify all required environment variables are set
- Test locally with production settings first

**Can't connect?**
- Verify CORS_ORIGINS includes your domain
- Check firewall/network settings
- Ensure health endpoint returns 200

Need help? Check Render documentation or contact support!
