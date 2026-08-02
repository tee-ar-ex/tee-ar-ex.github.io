# tee-ar-ex.github.io

A website for the TRX file format, built with Sphinx and the MyST parser.

## Building the documentation

### Prerequisites

- Python 3.9+

### Local build

1. Clone the repository:

   ```bash
   git clone https://github.com/tee-ar-ex/tee-ar-ex.github.io.git
   cd tee-ar-ex.github.io
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Build the documentation:

   ```bash
   make html
   ```

5. Open `_build/html/index.html` in your browser.

### Development workflow

To rebuild automatically while editing:

```bash
sphinx-autobuild source _build/html
```

Note: `sphinx-autobuild` needs to be installed separately
(`pip install sphinx-autobuild`).

### Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions on
pushes to `main`. Pull requests trigger a build to validate changes without
deploying.
