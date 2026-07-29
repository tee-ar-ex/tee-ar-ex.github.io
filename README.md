# tee-ar-ex.github.io

A website for the TRX file format.

## Building the documentation locally

To build the Sphinx documentation locally, you will need Python installed. We recommend using a virtual environment.

1. Clone the repository and navigate to it:
   ```bash
   git clone https://github.com/tee-ar-ex/tee-ar-ex.github.io.git
   cd tee-ar-ex.github.io
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the HTML documentation:
   ```bash
   make html
   ```

The built pages will be available in the `_build/html` directory. You can open `_build/html/index.html` in your web browser to view the site.