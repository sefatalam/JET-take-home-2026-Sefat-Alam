
# Just Eat Restaurant Finder

A small command-line application that takes a UK postcode, queries the Just Eat discovery API, and displays the first 10 restaurants with their name, cuisines, rating, and address.

## Quick start
Note: Requires Python 3.9 or higher to run. (Developed and tested on Python 3.13.7)
Dependencies: `requests`, `rich`
Dev dependencies:` pytest`

### (Recommended) Create and activate a virtual environment in the working directory

Windows:
```bash
#Create the virtual environment (In working directory):
python -m venv .venv

#Activate the environment (Open the file found at):
.venv\Scripts\activate.bat
```
macOS/Linux:
```bash
#Create the virtual environment (In working directory):
python -m venv .venv

#Activate the environment (Open the file found at):
source .venv/bin/activate
```
To disable the virtual environment either close the terminal or enter `deactivate` into the terminal.

### Running the Program
```bash
# Install dependencies
pip install -r requirements.txt

# Run with a postcode as an argument
python main.py EC4M 7RF

# Or run it without arguments and enter one interactively
python main.py
```
### Running the tests
```bash
#Install dev dependencies
pip install -r requirements-dev.txt

#Run the test suite:
python -m pytest

#Alternative: more verbose output
python -m pytest -v
```
## Project Structure
The code was intentionally kept modular so that it is easy to swap modules out (swapping the CLI interface with a web interface for example) and to test each module in isolation.
```
.
  ├── main.py                  # CLI entry point
  ├── api.py                   # Handles the Just Eat API request
  ├── models.py                # Restaurant dataclass and API response parsing
  ├── display.py               # Formatted terminal output using rich
  ├── conftest.py              # pytest configuration (adds project root to sys.path)
  ├── requirements.txt         # Runtime dependencies
  ├── requirements-dev.txt     # Development dependencies (pytest)
  ├── .gitignore
  ├── README.md
  └── tests/
      ├── test_api.py          # Tests for the API module
      ├── test_display.py      # Tests for the display module
      └── test_models.py       # Tests for the Restaurant model
```

## Design Decisions

### Language Choice
For this project I decided to use solely Python. Since the main steps of the task can be summarized as 'Call a JSON API -> Shape the response data -> Output it (CLI in this case)', many languages can do the job, so I chose Python since I am the most comfortable on it. As Python has a large amount of libraries, the workflow is also very straightforward; use `requests` to handle the API calls, Python dataclasses for the models, `rich` for clean terminal outputs, and `pytest` for comprehensive testing.

### Interface
For the interface I went with a console application. While a web frontend would be more visually expressive, it would require much more code to serve the data points. Since the main purpose of the task is to just meaningfully represent the specified data, a console interface seemed to be the most simple option.

To keep the console output readable and presentable, I used `rich` to render each restaurant inside a bordered panel with distinct visual cues like color-coded ratings and clear presentation of each restaurant name.

### API Requests

#### Request headers
Since the API requires a `User-Agent` header, a 403 error is returned when calling it with the default Python `requests` header, presumably to prevent bots from hitting the endpoint. As a small workaround, I manually set the `User-Agent` header to a simple `Mozilla/5.0` to mimic the request header sent from my browser to the endpoint. 

Note: Should the API filtering rules change, the header may need to be adjusted accordingly.

#### Postcode Cleaning
Users might type postcodes inconsistently (`ec4m 7rf`, `EC4M7RF`, `EC4M 7RF`, ...), so I wanted to make sure all of these options are supported by the program. To do this, before building the URL, the postcode is stripped of all whitespaces and upper-cased, This is done in `fetch_restaurants` in `api.py`so that this step is always performed when querying the API endpoint.

#### Safe Parsing
The API response contains a lot of nested fields, and not every restaurant has every field populated. Since the response is returned as a dictionary in Python, it is important to use the dedicated `.get()` method with sensible default values at each step as opposed to accessing by key directly. This is done so that missing/empty fields are still parsed cleanly, as opposed to returning a `KeyError`. 

## Assumptions
- **"First 10 restaurants returned"** - Taken to mean the first 10 restaurants in the order the API returns them, no other actions taken.
- **Rating** - The brief says to return ratings as a "number". Taken to be colloquial speech in the brief, returned as a `float` in the actual program. Missing ratings default do `0.0`
- **Address**- The API splits the address across multiple fields. I joined `firstLine`, `city`, and `postalCode` with commas, skipping any that are empty. This seemed like the most readable single-string representation.
- **Cuisines** — Each cuisine in the API is an object with a `name` and `uniqueName`. I took just the `name` field, since it seems to be more readable. If the list is empty the display shows `N/A`.
- **Target User** - Since the target user/demographic is never specified, I assumed a developer/intermediate user would be using this CLI program for querying, therefore choosing to always display the most readable format for each field (like `name` vs `uniqueName` as outlined above for example).

## Use of AI tools

In line with the guidance in the candidate brief, I used AI assistance for small things like double-checking `rich` styling syntax and sanity-checking a couple of test assertions. The architecture, the module separation, the parsing logic, and the test cases are my own work, and I verified anything AI-suggested by running it and reading through it rather than pasting blind.

## Future Improvements
- **A proper GUI** - Although the terminal output is clean and fulfills the task, a simple web interface would allow for more details to be shown for a restaurant in the future like images and hyperlinks for example. Since the scope of the task was concrete a terminal app is sufficient although for a real-world project, a web interface would allow for greater possibilities both functionally and visually.
- **Terminal-aware styling** - Since I personally use third party terminals like Ghostty, it would be a great option to display different outputs depending on the terminal being used. For more capable third party terminals, more complex and visually appealing design could be used, allowing to use more of `rich`'s capabilities, while reserving a simpler layout for default terminals.
- **Configurable output** - The brief explicitly stated for the output to contain the first 10 restaurants, but I kept the function signatures extensible on purpose so that in the future the app could be more flexible in terms of quantity output.
- **Retry and timeout handling** - Currently, if the network on either side were to be disrupted, an error would be raised before terminating or hang indefinitely. Instead, a short retry window with a back-off and an explicit timeout per request, would make the app more robust for poor connections.
- **Extended Functionality** - The current app is barebones in terms of functionality, only being able to display basic information about restaurants. For the future more features like sorting or a filter functionality could be added to make the application more capable.
- **Error Handling** - Currently, the app has meaningful error messages for the user inputs and API responses, but not for the actual network errors. Ideally, I would be able to add more detailed network errors, distinguishing between different error codes with tailored messages for each.


