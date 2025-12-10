# Skills

Skills are the smallest unit of logic in StashKit. Each Skill:

- handles a single concern
- accepts some inputs (request, partial entity, Dex)
- returns proposed updates or annotations

Examples:

- `BarcodeSkill` – read a barcode from an image
- `SpiritsClassifierSkill` – map a product to a `BoozeDex` node
- `CountryNormalizerSkill` – normalize free-text country names

Example shape:

```python
class SpiritsClassifierSkill(Skill):
    def run(self, entity, dex):
        text = entity.get("label_text", "")
        node = dex.classify_from_text(text)
        if node:
            return {"dex_path": node.path}
        return {}
```
