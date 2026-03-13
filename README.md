# 🦖 DinoExplorer

**A Python terminal application for exploring paleontological data in real-time.**

DinoExplorer was created to experiment with integrating different data sources into a single tool. The program combines a local database (for stable facts) with the Wikipedia and PaleoBioDB APIs (for dynamic data), organizing everything into a colorful, easy-to-read scientific dossier.

## Key Features
- **Smart Search:** Search for a specific dinosaur or get a random selection for a surprise discovery.
- **Hybrid Data:** Cross-references local taxonomic data with geographical locations and geological periods fetched from the web.
- **Visual Dossiers:** Retrieves official descriptions and specimen images directly from Wikipedia.

## Tech Stack
- **Language:** Python
- **Data Sources:** [PaleoBioDB](https://paleobiodb.org/) and [Wikipedia API](https://en.wikipedia.org/api/rest_v1/).
- **Libraries:** `requests`, `Pillow`, `colorama`.

## How to Run
1. Ensure you have Python installed.
2. Install the required libraries:
   ```bash
   pip install requests Pillow colorama
