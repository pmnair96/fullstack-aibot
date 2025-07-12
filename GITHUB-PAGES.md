# 🌐 GitHub Pages Deployment Guide

Deploy your Genie AI Assistant with **frontend on GitHub Pages** and **backend on Railway** - both completely free!

## 🚀 Quick Deployment Steps

### Step 1: Deploy Backend to Railway (Free)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy Backend**:
   ```bash
   ./deploy-backend-railway.sh
   ```

3. **Set Environment Variables** in Railway dashboard:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
   OPENROUTER_SITE_URL=https://pmnair96.github.io/fullstack-aibot
   SECRET_KEY=your-strong-secret-key
   ```

4. **Get your Railway URL** (e.g., `https://your-app-name.railway.app`)

### Step 2: Update Frontend Configuration

1. **Update the API URL** in `frontend/src/environments/environment.prod.ts`:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://your-railway-app.railway.app'  // Your Railway URL
   };
   ```

### Step 3: Enable GitHub Pages

1. **Go to your GitHub repository settings**
2. **Navigate to "Pages" section**
3. **Set Source to "GitHub Actions"**
4. **Push your changes to main branch**

### Step 4: Access Your App

After deployment completes (usually 2-3 minutes):

- 🌐 **Frontend**: https://pmnair96.github.io/fullstack-aibot
- 🔧 **Backend API**: https://your-railway-app.railway.app
- 📚 **API Docs**: https://your-railway-app.railway.app/docs

## 🔧 Alternative Backend Options

### Option A: Railway (Recommended)
- ✅ Free tier with 500 hours/month
- ✅ Easy deployment
- ✅ Auto-scaling
- ✅ Built-in monitoring

### Option B: Render
```bash
# Deploy to Render
git remote add render https://github.com/pmnair96/fullstack-aibot.git
# Follow Render's deployment guide
```

### Option C: Heroku
```bash
# Deploy backend to Heroku
heroku create your-genie-backend
git subtree push --prefix backend heroku main
```

## 🌍 Custom Domain (Optional)

1. **Add CNAME file** to `frontend/src/` with your domain
2. **Configure DNS** to point to `pmnair96.github.io`
3. **Update environment URLs** accordingly

## 🔍 Troubleshooting

### Frontend Issues
- Check browser console for CORS errors
- Verify API URL in environment.prod.ts
- Ensure GitHub Pages is enabled

### Backend Issues
- Check Railway logs: `railway logs`
- Verify environment variables are set
- Test API endpoints directly

## 📊 Monitoring

### GitHub Pages
- Deployment status in Actions tab
- Custom domain status in Settings > Pages

### Railway Backend
- Logs and metrics in Railway dashboard
- Health check: `https://your-app.railway.app/health`

---

**🎉 Your AI Assistant is now live on the web!**
