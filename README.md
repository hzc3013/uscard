Below is a sample **README.md** you can place in your repository. Feel free to modify the wording, project name, or any details to match your specific setup.

---

# USCard Forum Automation

This repository contains a Python script (wrapped in a Flask app) that automatically:

1. Logs into [uscardforum.com](https://www.uscardforum.com/).  
2. Visits a random subset of new posts.  
3. Scrolls through them to load content.  
4. Logs the post text to a local file (`posts_log.txt`).  
5. Sends an email summary (or error details) after each run.  

It’s designed to run on **Google Cloud Run**, triggered daily by **Cloud Scheduler**.

---

## Features

- **Automated Forum Login**: Uses Selenium to log in with username/password.  
- **Random Post Visiting**: Shuffles new posts and picks a random number (3–7) to read.  
- **Incremental Scrolling**: Simulates user scrolling in increments, giving time for content to load.  
- **Local File Logging**: Appends post content to `posts_log.txt` (for debugging or record-keeping).  
- **Email Notifications**: Sends a summary email on success or an error message if something fails.

---

## Requirements

1. **Python 3.9+**  
2. **Google Chrome or Chromium** (for Selenium).  
3. **ChromeDriver** (automatically managed by `webdriver_manager`).  
4. **Git** (if you plan to clone/push this repo).  
5. **GCP** account (for Cloud Run / Cloud Scheduler deployment).

---

## Local Setup

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. **Create & Activate a Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables** (optional for local testing):
   - `FORUM_USER` and `FORUM_PASS` if you prefer not to hardcode credentials.
   - `EMAIL_USER`, `EMAIL_PASS`, `EMAIL_TO` for email notifications.

5. **Run Locally**:
   ```bash
   python main.py
   ```
   - The Flask server starts on port `8080`.  
   - Visit <http://127.0.0.1:8080> in your browser or use `curl localhost:8080` to trigger the automation.

---

## Usage & Workflow

1. **Trigger Endpoint**:  
   - A GET request to `/` runs the Selenium script (`run_forum_visit()`).
2. **Script Flow**:
   - Logs into the forum using `FORUM_USER` / `FORUM_PASS`.
   - Navigates to `/new` posts.
   - Selects a random subset of posts to visit.
   - Scrolls each post incrementally.
   - Logs content to `posts_log.txt`.
   - Sends an email (success or error).
3. **Logs**:
   - `posts_log.txt` accumulates post content each run.
   - Cloud Run logs are also visible in GCP’s **Logs Explorer**.

---

## Deploy to Google Cloud Run

1. **Enable APIs**:  
   - In the GCP Console, enable **Cloud Run**, **Cloud Build**, and **Cloud Scheduler** APIs.

2. **Build & Push** (with Dockerfile or via gcloud):
   ```bash
   gcloud run deploy uscard-forum-automation \
       --source . \
       --platform managed \
       --region YOUR_REGION \
       --allow-unauthenticated
   ```
   This command:
   - Builds a container from your code (using `Dockerfile` or buildpacks).
   - Deploys it to Cloud Run.

3. **Set Environment Variables** in Cloud Run:
   - `FORUM_USER`, `FORUM_PASS`
   - `EMAIL_USER`, `EMAIL_PASS`, `EMAIL_TO`
   - Possibly `PYTHONUNBUFFERED=1` for real-time logging.

4. **Test**:  
   - Open the Cloud Run service URL in your browser or use `curl`.  
   - Check logs in the GCP Console if issues arise.

---

## Scheduling with Cloud Scheduler

1. **Create a Cloud Scheduler Job**:
   - **Frequency**: e.g., `0 9 * * *` (daily at 9 AM).  
   - **Target**: HTTP.  
   - **URL**: Your Cloud Run service URL (e.g., `https://uscard-forum-automation-abc123.a.run.app/`).  
   - **HTTP Method**: `GET`.  
   - **Auth**: If your service allows unauthenticated access, pick **Unauthenticated**. Otherwise, use OIDC tokens.

2. **Verify**:
   - Cloud Scheduler triggers the service daily.
   - Check Cloud Run logs for success or error.

---

## Email Configuration

By default, the sample code uses **Gmail SMTP** on port 465. If you have 2FA enabled, create an **App Password** in Gmail’s Security settings. Then set:
- `EMAIL_USER` = your Gmail address  
- `EMAIL_PASS` = your App Password  
- `EMAIL_TO`   = your recipient email

If you use another SMTP provider, adjust the `send_email` function accordingly.

---

## Troubleshooting

- **Timeouts / Element Not Found**:  
  - Increase wait times or verify the forum’s HTML structure hasn’t changed.  
- **No Posts Found**:  
  - Check if `/new` has any content. If not, script exits early with an error.  
- **Email Fails**:  
  - Make sure your SMTP credentials are correct and that less secure apps or app passwords are configured.

---

## Contributing

Feel free to open issues or pull requests for enhancements or bug fixes. All contributions are welcome.

---

## License

[MIT License](LICENSE) – You are free to use, modify, and distribute this code as per the terms of the MIT license.
