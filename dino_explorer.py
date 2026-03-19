import requests
import random
import textwrap
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
import os

from colorama import Fore, Style, init
init(autoreset=True, strip=False, convert=True)

def print_section(title):
    print(Fore.CYAN + "\n" + "═"*60)
    print(Fore.YELLOW + f"{title.center(60)}")
    print(Fore.CYAN + "═"*60)
    
DINO_LIST = [
    "Tyrannosaurus", "Triceratops", "Stegosaurus", "Velociraptor",
    "Brachiosaurus", "Spinosaurus", "Allosaurus", "Ankylosaurus",
    "Diplodocus", "Parasaurolophus", "Pachycephalosaurus", "Carnotaurus",
    "Deinonychus", "Utahraptor", "Giganotosaurus", "Carcharodontosaurus",
    "Iguanodon", "Edmontosaurus", "Corythosaurus", "Lambeosaurus", 
    "Apatosaurus", "Argentinosaurus", "Camarasaurus", "Therizinosaurus",
    "Oviraptor", "Dilophosaurus", "Microraptor"
]

# Core biological data (stable taxonomy)
DINO_CORE_DATA = {
    "Tyrannosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Triceratops": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Stegosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Velociraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Brachiosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Spinosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Allosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Ankylosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Diplodocus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Parasaurolophus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Pachycephalosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Carnotaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Deinonychus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Utahraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Giganotosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Carcharodontosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Iguanodon": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Edmontosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Corythosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Lambeosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Apatosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Argentinosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Camarasaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Therizinosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Oviraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Omnivore"},
    "Dilophosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Microraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"}
}

# Encyclopedia information
LOCAL_DINO_DATA = {

    "Tyrannosaurus": {
        "meaning": "Tyrant lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "8–9 tons",
        "fun_fact": "One of the terrestrial predators with the most powerful bite force ever recorded."
    },

    "Triceratops": {
        "meaning": "Three-horned face",
        "length": "8–9 m",
        "height": "3 m",
        "weight": "6–12 tons",
        "fun_fact": "The large neck frill likely served for defense and species recognition."
    },

    "Stegosaurus": {
        "meaning": "Roofed lizard",
        "length": "9 m",
        "height": "4 m",
        "weight": "5 tons",
        "fun_fact": "The dorsal plates may have been used for thermoregulation or display."
    },

    "Velociraptor": {
        "meaning": "Swift thief",
        "length": "2 m",
        "height": "0.5 m",
        "weight": "15 kg",
        "fun_fact": "Fossil evidence shows it had feathers and was much smaller than depicted in films."
    },

    "Brachiosaurus": {
        "meaning": "Arm lizard",
        "length": "22–26 m",
        "height": "12–13 m",
        "weight": "35–50 tons",
        "fun_fact": "Its front legs were longer than its hind legs, producing a giraffe-like posture."
    },

    "Spinosaurus": {
        "meaning": "Spine lizard",
        "length": "14–16 m",
        "height": "5–7 m",
        "weight": "7–10 tons",
        "fun_fact": "Likely semi-aquatic and possibly the largest known carnivorous dinosaur."
    },

    "Allosaurus": {
        "meaning": "Different lizard",
        "length": "8–10 m",
        "height": "3–4 m",
        "weight": "2–3 tons",
        "fun_fact": "One of the dominant predators of the Late Jurassic ecosystems in North America."
    },

    "Ankylosaurus": {
        "meaning": "Fused lizard",
        "length": "6–8 m",
        "height": "1.7 m",
        "weight": "6–8 tons",
        "fun_fact": "Possessed heavy armor and a massive tail club used for defense."
    },

    "Diplodocus": {
        "meaning": "Double beam",
        "length": "24–27 m",
        "height": "4–5 m",
        "weight": "12–16 tons",
        "fun_fact": "Its extremely long tail may have functioned like a whip."
    },

    "Parasaurolophus": {
        "meaning": "Near crested lizard",
        "length": "9–10 m",
        "height": "4 m",
        "weight": "2.5–3 tons",
        "fun_fact": "The hollow crest likely acted as a resonating chamber for sound."
    },

    "Pachycephalosaurus": {
        "meaning": "Thick-headed lizard",
        "length": "4–5 m",
        "height": "1.5–2 m",
        "weight": "400–500 kg",
        "fun_fact": "Its skull dome may have been used for head-butting behavior."
    },

    "Carnotaurus": {
        "meaning": "Meat-eating bull",
        "length": "7–9 m",
        "height": "3 m",
        "weight": "1.3–2 tons",
        "fun_fact": "Recognizable by the horns above its eyes and extremely reduced forelimbs."
    },
    
      "Deinonychus": {
        "meaning": "Terrible claw",
        "length": "3–3.5 m",
        "height": "1.5 m",
        "weight": "70–100 kg",
        "fun_fact": "Its large sickle-shaped claw inspired the modern image of agile raptor dinosaurs."
    },

    "Utahraptor": {
        "meaning": "Utah predator",
        "length": "6–7 m",
        "height": "2 m",
        "weight": "500–700 kg",
        "fun_fact": "The largest known dromaeosaurid, much bigger than Velociraptor."
    },

    "Giganotosaurus": {
        "meaning": "Giant southern lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "6–8 tons",
        "fun_fact": "One of the largest carnivorous dinosaurs ever discovered."
    },

    "Carcharodontosaurus": {
        "meaning": "Shark-toothed lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "6–7 tons",
        "fun_fact": "Named for its blade-like teeth resembling those of sharks."
    },

    "Iguanodon": {
        "meaning": "Iguana tooth",
        "length": "9–11 m",
        "height": "5 m",
        "weight": "3–5 tons",
        "fun_fact": "One of the first dinosaurs ever scientifically described in the 19th century."
    },

    "Edmontosaurus": {
        "meaning": "Edmonton lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "4 tons",
        "fun_fact": "Many fossils preserve impressions of skin, revealing a scaly texture."
    },

    "Corythosaurus": {
        "meaning": "Helmet lizard",
        "length": "9–10 m",
        "height": "4 m",
        "weight": "3 tons",
        "fun_fact": "Its tall crest may have been used for visual display and sound resonance."
    },

    "Lambeosaurus": {
        "meaning": "Lambe's lizard",
        "length": "9–10 m",
        "height": "4 m",
        "weight": "2.5–3 tons",
        "fun_fact": "Its hollow crest likely amplified vocal calls within the herd."
    },

    "Apatosaurus": {
        "meaning": "Deceptive lizard",
        "length": "21–23 m",
        "height": "4–5 m",
        "weight": "20–25 tons",
        "fun_fact": "Previously confused with the dinosaur Brontosaurus in early classifications."
    },

    "Argentinosaurus": {
        "meaning": "Argentina lizard",
        "length": "30–35 m",
        "height": "15 m",
        "weight": "60–80 tons",
        "fun_fact": "One of the largest land animals known to have ever existed."
    },

    "Camarasaurus": {
        "meaning": "Chambered lizard",
        "length": "18–20 m",
        "height": "7 m",
        "weight": "20 tons",
        "fun_fact": "Its vertebrae contained hollow chambers that reduced body weight."
    },

    "Therizinosaurus": {
        "meaning": "Scythe lizard",
        "length": "9–10 m",
        "height": "5 m",
        "weight": "5 tons",
        "fun_fact": "Famous for its enormous claws that could exceed one meter in length."
    },

    "Oviraptor": {
        "meaning": "Egg thief",
        "length": "1.5–2 m",
        "height": "1 m",
        "weight": "20–30 kg",
        "fun_fact": "Originally thought to steal eggs, later fossils showed it was actually protecting its own nest."
    },

    "Dilophosaurus": {
        "meaning": "Two-crested lizard",
        "length": "6–7 m",
        "height": "2 m",
        "weight": "400 kg",
        "fun_fact": "Recognizable by the pair of crests on its skull."
    },

    "Microraptor": {
        "meaning": "Small thief",
        "length": "0.8–1 m",
        "height": "0.4 m",
        "weight": "1 kg",
        "fun_fact": "Had feathers on both arms and legs, allowing it to glide between trees."
    }

}

#  DATA FETCHING

def fetch_paleodb(name):
    """Returns (location, era_range) from PaleoBioDB."""
    try:
        url = f"https://paleobiodb.org/data1.2/occs/list.json?base_name={name}&show=full"
        r = requests.get(url, timeout=5).json()
        if r.get("records"):
            f = r["records"][0]
            location = f"{f.get('st', 'Unknown area')} ({f.get('cc', '??')})"
            start_age = f.get("lag")
            end_age = f.get("eag")
            if start_age and end_age:
                era_range = f"{start_age} – {end_age} Ma"
            elif end_age:
                era_range = f"{end_age} Ma"
            else:
                era_range = "Unknown"
            return location, era_range
    except requests.exceptions.RequestException:
        pass
    return "Unknown location", "Unknown"


def fetch_wikipedia(name):
    """Returns (description, image_url) from Wikipedia."""
    headers = {'User-Agent': 'DinoExplorerBot/1.0'}
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
        r = requests.get(url, headers=headers, timeout=5).json()
        desc = r.get("extract", "No information found.")
        img_url = (
            r.get("originalimage", {}).get("source")
            or r.get("thumbnail", {}).get("source")
        )
        return desc, img_url
    except requests.exceptions.RequestException:
        return "No information found.", None


def build_dino_data(name):
    """Assembles all data for a dinosaur into a single dict."""
    location, era_range = fetch_paleodb(name)
    desc, img_url = fetch_wikipedia(name)
    core = DINO_CORE_DATA.get(name, {})
    info = LOCAL_DINO_DATA.get(name, {})
    return {
        "name": name,
        "class": core.get("class", "Unknown"),
        "order": core.get("order", "Unknown"),
        "diet": core.get("diet", "Unknown"),
        "meaning": info.get("meaning", "Unknown"),
        "length": info.get("length", "Unknown"),
        "height": info.get("height", "Unknown"),
        "weight": info.get("weight", "Unknown"),
        "location": location,
        "era_range": era_range,
        "description": desc,
        "fun_fact": info.get("fun_fact", "No recorded trivia."),
        "img_url": img_url,
    }

#  DISPLAY

def display_dino(d):
    print("\n" + "="*60)
    print(f"      PALEONTOLOGICAL DOSSIER: {d['name'].upper()}")
    print("="*60)

    print_section("TAXONOMY")
    print(Fore.GREEN + "Class        : " + Style.RESET_ALL + d["class"])
    print(Fore.GREEN + "Order        : " + Style.RESET_ALL + d["order"])
    print(Fore.GREEN + "Diet         : " + Style.RESET_ALL + d["diet"])
    print(Fore.GREEN + "Name Meaning : " + Style.RESET_ALL + d["meaning"])

    print_section("PHYSICAL CHARACTERISTICS")
    print(Fore.MAGENTA + "Length       : " + Style.RESET_ALL + d["length"])
    print(Fore.MAGENTA + "Height       : " + Style.RESET_ALL + d["height"])
    print(Fore.MAGENTA + "Weight       : " + Style.RESET_ALL + d["weight"])

    print_section("PALEONTOLOGY")
    print(Fore.BLUE + "Fossil Sites : " + Style.RESET_ALL + d["location"])
    print(Fore.BLUE + "Time Range   : " + Style.RESET_ALL + d["era_range"])

    print_section("DESCRIPTION")
    print(textwrap.fill(d["description"], width=60))

    print_section("SCIENTIFIC NOTE")
    print(textwrap.fill(d["fun_fact"], width=60))

    if d["img_url"]:
        try:
            headers = {'User-Agent': 'DinoExplorerBot/1.0'}
            r = requests.get(d["img_url"], headers=headers, timeout=10)
            img = Image.open(BytesIO(r.content))
            print(Fore.CYAN + "\nDisplaying specimen reconstruction...")
            img.show()
        except Exception:
            print(Fore.RED + "Image rendering failed.")
    else:
        print(Fore.YELLOW + "\nNo visual record found.")

    print("="*60 + "\n")


def display_comparison(d1, d2):
    """Prints a side-by-side comparison of two dinosaurs."""
    col = 28

    def row(label, v1, v2):
        print(
            Fore.GREEN + f"{label:<14}" + Style.RESET_ALL +
            f"{str(v1):<{col}}" +
            f"{str(v2):<{col}}"
        )

    print("\n" + "="*70)
    print(f"  {'COMPARISON':^66}")
    print("="*70)
    print(
        Fore.YELLOW + f"{'':14}" +
        f"{d1['name'].upper():<{col}}" +
        f"{d2['name'].upper():<{col}}" + Style.RESET_ALL
    )
    print("-"*70)
    row("Diet",       d1["diet"],      d2["diet"])
    row("Length",     d1["length"],    d2["length"])
    row("Height",     d1["height"],    d2["height"])
    row("Weight",     d1["weight"],    d2["weight"])
    row("Order",      d1["order"],     d2["order"])
    row("Era",        d1["era_range"], d2["era_range"])
    row("Fossil site",d1["location"],  d2["location"])
    print("="*70 + "\n")

#  PDF EXPORT

def sanitize(text):
    return text.encode("latin-1", errors = "replace").decode("latin-1")
    
def export_pdf(d):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    import urllib.request, ssl, tempfile, os

    filename = f"{d['name'].lower()}_dossier.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    title_style = ParagraphStyle("title", fontSize=18, fontName="Helvetica-Bold",
                                 alignment=1, spaceAfter=14, spaceBefore=4,
                                 textColor=colors.HexColor("#1a1a1a"))

    value_style = ParagraphStyle("value", fontSize=11, fontName="Helvetica",
                                 spaceAfter=5, leading=16)

    body_style = ParagraphStyle("body", fontSize=11, fontName="Helvetica",
                                spaceAfter=6, leading=16)

    def section(title):
        # Table trick: sfondo colorato senza tagliare il testo
        t = Table([[Paragraph(f"<b>  {title}</b>",
                    ParagraphStyle("sh", fontSize=13, fontName="Helvetica-Bold",
                                   textColor=colors.white, leading=20,
                                   spaceAfter=0, spaceBefore=0))]],
                  colWidths=[170*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#444444")),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ]))
        return t

    def field(label, value):
        return Paragraph(f"<b>{label}:</b>  {value}", value_style)

    # ── Image ──
    img_element = None
    if d.get("img_url"):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(d["img_url"],
                                         headers={"User-Agent": "DinoExplorerBot/1.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                img_data = resp.read()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp.write(img_data)
            tmp.close()
            img_element = RLImage(tmp.name, width=80*mm, height=60*mm,
                                  kind="proportional")
        except Exception:
            img_element = None

    story = [
        Paragraph(f"PALEONTOLOGICAL DOSSIER: {d['name'].upper()}", title_style),
    ]

    if img_element:
        story.append(img_element)
        story.append(Spacer(1, 8))

    story += [
        section("TAXONOMY"),
        Spacer(1, 4),
        field("Class",        d["class"]),
        field("Order",        d["order"]),
        field("Diet",         d["diet"]),
        field("Name Meaning", d["meaning"]),
        Spacer(1, 4),

        section("PHYSICAL CHARACTERISTICS"),
        Spacer(1, 4),
        field("Length", d["length"]),
        field("Height", d["height"]),
        field("Weight", d["weight"]),
        Spacer(1, 4),

        section("PALEONTOLOGY"),
        Spacer(1, 4),
        field("Fossil Sites", d["location"]),
        field("Time Range",   d["era_range"]),
        Spacer(1, 4),

        section("DESCRIPTION"),
        Spacer(1, 4),
        Paragraph(d["description"], body_style),
        Spacer(1, 4),

        section("SCIENTIFIC NOTE"),
        Spacer(1, 4),
        Paragraph(d["fun_fact"], body_style),
    ]

    doc.build(story)

    if img_element:
        try:
            os.unlink(tmp.name)
        except Exception:
            pass

    print(Fore.GREEN + f"\n  PDF saved as '{filename}' in the current directory.")

#  INPUT HELPERS

def ask_dino_name(prompt="Enter dinosaur name: "):
    while True:
        raw = input(prompt).strip().capitalize()
        if raw in DINO_LIST:
            return raw
        print(Fore.RED + f"  '{raw}' not recognised. Available dinosaurs:")
        print(Fore.YELLOW + "  " + ", ".join(DINO_LIST))

#  MAIN MENU LOOP

def print_menu():
    print(Fore.CYAN + "\n" + "═"*60)
    print(Fore.YELLOW + "         🦕  DINO EXPLORER  🦕".center(60))
    print(Fore.CYAN + "═"*60)
    print(Fore.WHITE + "  [1]  Search a dinosaur")
    print(Fore.WHITE + "  [2]  Random dinosaur")
    print(Fore.WHITE + "  [3]  Compare two dinosaurs")
    print(Fore.WHITE + "  [4]  Export dossier to PDF")
    print(Fore.WHITE + "  [0]  Exit")
    print(Fore.CYAN + "═"*60)


def main():
    while True:
        print_menu()
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            name = ask_dino_name("  Enter dinosaur name: ")
            data = build_dino_data(name)
            display_dino(data)

        elif choice == "2":
            name = random.choice(DINO_LIST)
            print(Fore.YELLOW + f"\n  Random pick: {name}")
            data = build_dino_data(name)
            display_dino(data)

        elif choice == "3":
            print(Fore.YELLOW + "\n  Choose two dinosaurs to compare.")
            name1 = ask_dino_name("  First dinosaur : ")
            name2 = ask_dino_name("  Second dinosaur: ")
            d1 = build_dino_data(name1)
            d2 = build_dino_data(name2)
            display_comparison(d1, d2)

        elif choice == "4":
            name = ask_dino_name("  Which dinosaur to export? ")
            data = build_dino_data(name)
            export_pdf(data)

        elif choice == "0":
            print(Fore.YELLOW + "\n  Goodbye! 🦖\n")
            break

        else:
            print(Fore.RED + "  Invalid option. Please choose 0–4.")


if __name__ == "__main__":
    main()
