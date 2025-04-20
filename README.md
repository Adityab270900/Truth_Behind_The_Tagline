# Truth Behind the Tagline (TBT)

An AI-powered system that analyzes marketing claims and taglines to determine their truthfulness through fact-checking against verifiable data, specifically focused on the Indian market context.

## Project Overview

Truth Behind the Tagline (TBT) is an NLP-powered system using Retrieval Augmented Generation (RAG) to analyze marketing claims from Indian brands and determine their truthfulness based on available evidence. The system is designed to:

1. Process and analyze marketing claims made by Indian brands
2. Retrieve relevant evidence from a curated knowledge base
3. Assess claims based on regulatory standards and factual information
4. Provide a verdict (Substantiated, Partially True, or Misleading) with explanations

## Features

- Input form for brand name, tagline, and specific marketing claim
- Sample claims from popular Indian brands for easy testing
- Evidence retrieval using RAG (Retrieval Augmented Generation)
- Claim analysis against multiple evidence sources
- Detailed results page with:
  - Verdict and confidence score
  - Supporting and contradicting evidence
  - Regulatory context based on Indian standards
  - Explanation of the analysis

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy with SQLite (configurable for PostgreSQL)
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **NLP Components**:
  - Custom text preprocessing pipeline
  - Keyword-based RAG engine with inverted index
  - Rule-based claim analyzer with negation detection
  - Indian language support for mixed language content

## Project Structure

```
├── app.py             # Main Flask application with routes
├── main.py            # Entry point that imports app
├── models.py          # Database models (claims, evidence, feedback)
├── data/              # Sample data files
│   ├── evidence_database.json     # Curated evidence for claims
│   ├── indian_brands.json         # List of Indian brands with taglines
│   └── regulatory_standards.json  # Regulatory standards by industry
├── static/            # Static assets
├── templates/         # HTML templates
└── utils/             # Utility modules
    ├── claim_analyzer.py        # Analyzes claims against evidence
    ├── nlp_processor.py         # Text preprocessing functionality
    └── rag_engine.py            # Retrieval-augmented generation engine
```

## Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/Adityab270900/Project_TBT.git
   cd Project_TBT
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

4. Access the application at: http://localhost:5000

## Example Claims

The system comes with several pre-loaded sample claims from popular Indian brands:

- "Amul milk contains no preservatives or additives" (Amul)
- "Divya Coronil Kit cures COVID-19 in 7 days" (Patanjali)
- "Dabur Chyawanprash increases immunity by 3 times" (Dabur)
- "Scientifically proven to deliver fairness in 4 weeks" (Fair & Lovely)

## Indian Market Focus

This application is specifically designed for the Indian context, with:

- Indian regulatory standards (FSSAI, ASCI, Ministry of AYUSH)
- Support for mixed language content (English + Indic languages)
- Evidence from Indian research institutions and authorities
- Focus on Indian brands and their common marketing claims

## Future Enhancements

- Integration with larger language models for more nuanced analysis
- User accounts to track claim verification history
- API for third-party fact-checking integration
- Mobile application for on-the-go claim verification
- Expanded evidence database with real-time information sources

## License

This project is open source, available under the [MIT License](LICENSE).

## Acknowledgments

- Built using Flask and Bootstrap
- Sample data curated from publicly available sources
- Inspired by the need for transparent marketing in the Indian market