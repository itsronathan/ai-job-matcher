# Quick Start Guide - AI Job Matcher

A super simple guide to get up and running in 5 minutes!

## What Does This Do?

This tool compares your **resume** with a **job description** and tells you:
- How well you match the job (as a percentage)
- What skills you have that the job wants ✓
- What skills you're missing ✗

## Step 1: Get the Project

Copy this link into your browser:
```
https://github.com/itsronathan/ai-job-matcher
```

Click the green **"Code"** button, then click **"Download ZIP"**

Unzip the folder anywhere on your computer (like your Desktop or Documents folder).

## Step 2: Open Command Prompt in the Folder

**Easiest way:**
1. Open the unzipped `ai-job-matcher` folder
2. Right-click in the empty space (not on a file or folder)
3. Select **"Open in Terminal"** (or **"Open Command Prompt here"**)

A black command window should pop up.

**Alternative if that doesn't work:**
1. Left-click on the folder path shown at the top of the window
2. Type `cmd` and press Enter
3. A black window should appear

## Step 3: Install (One-time Setup)

In the command prompt, copy and paste this and press Enter:

```
python -m pip install scikit-learn --only-binary :all:
python -m pip install nltk
```

Wait for it to finish (it might take a minute or two).

**If you see an error about "Visual C++"**, that's normal on Windows! The commands above will work around it by installing pre-built versions.

## Step 4: Try It Out With Sample Files

Copy and paste this into the command prompt and press Enter:

```
python run_sample.py
```

You should see the results! It shows:
- Match Score (as a %)
- Skills you have that match
- Skills you're missing

## Step 5: Use It With Your Own Files

### Option A: Create Your Files (Easy)
1. Open Notepad
2. Paste your resume text
3. Save as `my_resume.txt` in the `ai-job-matcher` folder
4. Do the same for the job description, save as `my_job.txt`

### Option B: Use the Interactive Mode
In the command prompt, type:
```
python job_matcher.py
```

When it asks for file paths, type the location of your files. Example:
```
Enter the path to your resume file: my_resume.txt
Enter the path to the job description file: my_job.txt
```

## Troubleshooting

### "Python is not recognized"
You need to install Python first from: https://www.python.org/downloads/

When installing, **check the box that says "Add Python to PATH"**

### "Microsoft Visual C++ error"
Copy and paste this:
```
pip install scikit-learn --only-binary :all:
pip install nltk
```

### "File not found"
Make sure your text files are in the `ai-job-matcher` folder, or use the full path to the file like:
```
C:\Users\YourName\Desktop\my_resume.txt
```

## That's It!

You now have a tool to quickly check if you match a job before applying. Good luck! 🚀

---

**Need help?** Check the main `README.md` file for more details.
