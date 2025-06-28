# 🕷️ Burp Suite Sitemap Dumper

> **Easily extract and save all files (JS, HTML, images, etc.) from a Burp Suite sitemap export to your local machine.**

Have you ever exported the sitemap from Burp Suite and wished you could instantly save all the files — like JavaScript, HTML, stylesheets, images — directly to your filesystem for offline analysis, debugging, or static analysis?

This tool automates exactly that.

---

## 📸 Example: Exporting Sitemap from Burp Suite

Right-click the domain or folder in Burp Suite's Site Map panel and select:

**`Save selected items`**

![image](https://github.com/user-attachments/assets/19e2b456-17b4-4daa-8fa7-b94593d4e531)

Save the result as an **XML file**, and you're ready to go.

---

## ⚙️ Features

✅ Extracts base64-encoded responses

✅ Reconstructs full folder/URL structure

✅ Strips HTTP headers from responses

✅ Infers missing file extensions via `<mimetype>`

✅ Supports CLI flags via `argparse`

✅ Cross-platform (Python 3.6+)

---

## 🚀 Usage

```bash
python3 burpsuite-sitemap-dumper.py -i all_requests.xml -o output_folder
```

### Flags

| Flag           | Description                                   |
| -------------- | --------------------------------------------- |
| `-i, --input`  | Path to Burp XML file (required)              |
| `-o, --output` | Output directory (default: `extracted_files`) |

You can also view the help menu:

```bash
python3 burpsuite-sitemap-dumper.py --help
```

---

## 🧠 How It Works

* Parses the Burp Suite XML export
* For each item with a base64-encoded `<response>`:

  * Decodes the body and strips headers
  * Reconstructs the path from the URL
  * Deduces the file extension:

    * From the URL (if present)
    * Else from `<mimetype>`
    * Else `.bin`
  * Saves the file locally in the appropriate subfolder

---

## 🧩 Example Output Structure

```
extracted_files/
└── example.com/
    ├── index.html
    ├── assets/
    │   └── app.js
    └── images/
        └── logo.png
```

---

## 🔧 Requirements

* Python 3.6+
* No dependencies (pure standard library)

---

## 🧪 Tip

If you want to enhance this further:

* Add magic file type detection via `python-magic`
* Add logging instead of print statements
* Dump a manifest CSV with metadata for auditing

---

## 📄 License

MIT — do whatever you want, just don’t blame us when you dump 10,000 files to disk 😄

---

Let me know if you’d like:

* A logo badge
* Packaging as a PyPI tool (`pip install burpsuite-sitemap-dumper`)
* Prettier table of contents / anchors
