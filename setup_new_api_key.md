# Setting Up a New YouTube API Key

## Step 1: Create a New Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Give it a name (e.g., "YouTube Analytics v2")
4. Click "Create"

## Step 2: Enable YouTube Data API v3
1. In your new project, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and press "Enable"

## Step 3: Create API Key
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Copy the new API key

## Step 4: Set Environment Variable
```bash
export YOUTUBE_API_KEY="your_new_api_key_here"
```

## Step 5: Test the New Key
```bash
python test_youtube_api.py
```

## Alternative: Use Multiple API Keys
You can also rotate between multiple API keys by modifying the code to use different keys for different requests. 