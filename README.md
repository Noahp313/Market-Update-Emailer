# Market Update Emailerr

Sends an email each day at 5:00 pm containing key developments in the stock market and economy during the day. Email contains a 3-5 paragraph summary of key articles, top gainers, top losers, major indicies, upcoming earnings events, and past earnings events.

## Project Signature

```text
Market-Update-Emailer/
|
|-- email_updater.py # main
|-- gainers_and_losers.py # helper functions
|-- market_text.py # helper functions
|-- requirements.txt
|-- .gitignore
|-- README.md
|-- .env.example
|-- .env # ignored
|-- .venv/ # ignored
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/Noahp313/Market-Update-Emailer.git
cd Market-Update-Emailer
```

2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environmental Variables

Create a `.env` file in the project root. Use `.env.example` for required variables.

```
Required APIs/Accounts:
- Gemini API
- AlphaVantage API
- Earnings API
- Sender Email and App Password
- Receiver Email
- SMTP Server and Port
```

## Usage

Run the application in the venv

```bash
venv\Scripts\python email_updater.py
```

## Scheduling

(Optional) This program can be scheduled to automatically run in your computer's task schedule:

### Windows (Task Scheduler)

1. Open **Task Scheduler**
2. Click **Create Task**
3. **Trigger** for when you want email to send
4. Under **Actions**, choose:
   **Program/script:**
   ```
   "C:\path\to\my-project\venv\Scripts\python.exe"
   ```
   **Add arguments:**
   ```
   "C:\path\to\my-project\email_updater.py"
   ```
   **Start in:**
   ```
   C:\path\to\my-project
   ```

### MacOS / Linux

Edit your crontab. Change the second number to change the hour at which the program is run (executes at 07:00 AM in this example). Use absolute paths:

```bash
crontab -e
0 7 * * * /path/to/my-project/venv/bin/python /path/to/my-project/email_updater.py >> /path/to/my-project/log.txt 2>&1
```
