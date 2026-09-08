# script to parse json export from pixelfed into markdown: 1 file for each photo
import json
from pathlib import Path


INPUT_FILE = "pixelfed-statuses.json"
OUTPUT_DIR = Path("markdown_posts")


def extract_posts():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    OUTPUT_DIR.mkdir(exist_ok=True)

    for post in posts:
        if post.get("pf_type", "") != "photo":
            continue

        content_text = post.get("content_text", "")
        created_at = post.get("created_at", "")

        # Estrae l'URL dalla prima media attachment
        media_attachments = post.get("media_attachments", [])

        if media_attachments:
            image_url = media_attachments[0].get("url")
        else:
            image_url = None

        # Estrae tutti i name dei tags
        tags = [
            tag.get("name")
            for tag in post.get("tags", [])
            if tag.get("name")
        ]

        # Costruisce il frontmatter Markdown
        lines = [
            "---",
            f"title: {json.dumps(content_text, ensure_ascii=False)}",
            f"datetime: {json.dumps(created_at, ensure_ascii=False)}",
            f"image: {json.dumps(image_url, ensure_ascii=False)}",
            "tags:",
        ]

        for tag in tags:
            lines.append(f"  - {tag}")

        lines.extend([
            "---",
            "",
            content_text,
            "",
        ])

        # Nome del file usando content_text + ID numerico
        post_id = post.get("id", "post")
        filename = create_filename(content_text, post_id)
        output_file = OUTPUT_DIR / filename

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

        print(f"Creato: {output_file}")

def create_filename(content_text, post_id):
    slug = content_text.strip()
    slug = slug.replace("#", "")
    slug = slug.replace("\n", "_")
    slug = slug.replace("/", "_")
    slug = slug.replace("?", "_")
    slug = slug.replace(",", "_")
    slug = slug.replace(" ", "_")
    return f"{slug}_{post_id}.md"


if __name__ == "__main__":
    extract_posts()
