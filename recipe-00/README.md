## Recipe 00
The recipe demonstrates how to use Ray to evaluate AI agents at scale. 

## Part 00
This part of the recipe outlines the setup for this project. 

**Step 1.** Create a Python virtual environment. 
```bash
python -m venv .venv
```

**Step 2.** Activate the Python virtual environment you just created. 
```bash
source .venv/bin/activate
```

**Step 3.** Create a file called `requirements.txt` and add the content below to it. The file will be used to identify this project's Python dependencies. 
```bash
ray
```

**Step 4.** Install this project's Python dependencies. 
```bash
python -m pip install -r requirements.txt
```

**Step 5.** If you are using VS Code as your code editor, now would be a good time to select the Python interpreter within your virtual environment as your default Python interpreter. This will make it easier to write and debug your code as you follow along with this recipe. 

## Part 01
This part of the recipe will confirm your local development is setup correctly. 

**Step 1.** Create a file called `main.py` and add the content below to it. 
```python
import ray

ray.init()
```

**Step 2.** Use the Python interpreter to run your code. 
```bash
python main.py
```