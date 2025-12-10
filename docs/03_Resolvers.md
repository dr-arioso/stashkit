# Resolvers

Resolvers orchestrate Skills to turn raw inputs into structured entities.

Typical responsibilities:

- Accept a request (e.g., text, image path, barcode data)
- Select a chain of Skills to apply
- Consult a Dex via LexiDex when classification is needed
- Decide when an entity is "resolved enough" to return

Example sketch:

```python
class BottleResolver(Resolver):
    def resolve(self, request, dex):
        entity = {}
        entity.update(self.run_skill(BarcodeSkill, request))
        entity.update(self.run_skill(LabelOCRSkill, request))
        entity.update(self.run_skill(SpiritsClassifierSkill, entity, dex))
        return entity
```

Resolvers **do not own** Dex objects; instead they receive a Dex instance from
the calling code or from `use_booster_pack()`.
