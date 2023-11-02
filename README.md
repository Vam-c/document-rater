# Document-Rater | Assignment-Evaluator
Rate/Evaluate documents based on labelled data using TF-IDF Vectorization and Cosine Similarity. Normalize the data using Collaborative Filtering based system learned as part of my curriculum in Big Data Analytics.

### Tech Stack  
- Server   -- FastAPI
- FrontEnd -- Jinja (SSR)
- Model    -- Python script

### Running the application
- Create a virtual environment
  - `python -m venv venv`
  - `source venv/Script/activate` - for Windows
  - `source venv/bin/activate`    - for Linux
   
- Install dependencies from requirements.py
  - `pip install -r requirements.py`
    
- Run server
  - `uvicorn server:app`
