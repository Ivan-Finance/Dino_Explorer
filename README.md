# 🦕 Dino Explorer

A terminal-based dinosaur encyclopedia built in Python.  
Search for dinosaurs, compare them, explore random picks, and export detailed PDF dossiers, all from the command line.

---

## Features

- **Search** a specific dinosaur by name and get a full paleontological dossier
- **Random mode**: let the program pick a random dinosaur for you
- **Compare** two dinosaurs side by side (diet, size, era, fossil sites)
- **Export to PDF**: generates a formatted dossier with image, taxonomy, physical data, and description
- **Interactive menu** with a loop — keeps running until you decide to exit

---

## Data Sources

Each dinosaur dossier pulls from two external APIs:

- **Wikipedia REST API**: description and image
- **PaleoBioDB API**: fossil site location and geological time range

Core data (taxonomy, physical characteristics, name meanings, fun facts) is stored locally for reliability and speed.

---

## Installation

```bash
pip install requests pillow colorama reportlab
```

---

## Usage

```bash
python dino_explorer.py
```

You will be shown a menu:

```
══════════════════════════════════════════════════════════
                   🦕  DINO EXPLORER  🦕
══════════════════════════════════════════════════════════
  [1]  Search a dinosaur
  [2]  Random dinosaur
  [3]  Compare two dinosaurs
  [4]  Export dossier to PDF
  [0]  Exit
══════════════════════════════════════════════════════════
```

---

## Available Dinosaurs

27 dinosaurs are currently supported:

Tyrannosaurus, Triceratops, Stegosaurus, Velociraptor, Brachiosaurus, Spinosaurus, Allosaurus, Ankylosaurus, Diplodocus, Parasaurolophus, Pachycephalosaurus, Carnotaurus, Deinonychus, Utahraptor, Giganotosaurus, Carcharodontosaurus, Iguanodon, Edmontosaurus, Corythosaurus, Lambeosaurus, Apatosaurus, Argentinosaurus, Camarasaurus, Therizinosaurus, Oviraptor, Dilophosaurus, Microraptor

---

## Requirements

| Library | Purpose |
|---|---|
| `requests` | API calls |
| `Pillow` | Image display in terminal |
| `colorama` | Colored terminal output |
| `reportlab` | PDF generation |
