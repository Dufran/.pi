---
name: audit-model
description: Audit a selected Django model class and its corresponding Factory Boy factory for model quality, indexes, metadata, string representation, and Pyrefly-friendly type checking. Use when asked to review or improve a Django model.
---

# Audit Model

Use this skill when the user asks to audit, review, or improve a Django model class.

## Model Review

For the selected Django model class in context, suggest improvements to the model.

Check for:

- Missing `help_text` on fields, and propose useful `help_text` values.
- Fields that are likely to be queried and may benefit from indexes.
- Missing or incomplete `Meta` class.
- Missing `verbose_name`, `verbose_name_plural`, or `ordering` in `Meta`.
- Missing `__str__` method.

When recommending indexes, prefer fields likely to be filtered, sorted, joined, or looked up frequently. Avoid suggesting indexes blindly for every field.

## Factory Review

Search the codebase for a corresponding Factory Boy factory named `{ModelName}Factory`.

If the factory exists, audit it for completeness and maintainability. If it does not exist, suggest creating one.

When reviewing a factory:

1. Inspect `Meta.model` to identify the underlying Django model.
2. Compare Factory Boy fields with model fields:
   - Identify missing fields.
   - For each missing field, suggest the most appropriate Factory Boy declaration based on the model field type.
3. Evaluate existing factory fields for the most suitable Factory Boy method, such as:
   - `factory.Faker`
   - `factory.SubFactory`
   - `factory.LazyAttribute`
   - `factory.Sequence`
   - `factory.Iterator`
4. For `CharField` fields with choices, suggest `factory.Iterator` over the enum or choices class used by the model field.
5. Ensure foreign keys and related fields use `SubFactory` or another appropriate strategy.
6. Suggest improvements for fields with defaults, unique constraints, or choices.
7. Prefer realistic generated values over hardcoded values.
8. Optimize fixture readability and maintainability.

Reference Factory Boy docs when needed: <https://factoryboy.readthedocs.io/en/stable/reference.html>

## Type Checking Review

Review the model with static type checking in mind. The project uses Pyrefly.

Suggest:

- Return type annotations for all custom model methods.
- Parameter annotations for custom methods.
- Typed custom managers and querysets where applicable.
- `typing.Self` for queryset methods when appropriate.
- `ClassVar` for class-level constants and managers.
- Typed properties using `@property`.
- Avoiding untyped dynamic attributes.
- Avoiding unnecessary `# type: ignore` comments.

Do not blindly annotate Django model fields unless the project's Django typing setup supports it. Prefer typing behavior, methods, managers, querysets, and properties.

## Example Target Shape

```python
class RejectionReason(models.Model):
    """
    Rejection reason model.
    """

    value = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Rejection reason",
        help_text="Short code/value for internal use",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Description to show to the user",
    )

    objects: ClassVar[RejectionReasonManager] = RejectionReasonManager()

    class Meta:
        ordering = ["-pk"]
        db_table = "rejection_reasons"
        verbose_name = _("Rejection Reason")
        verbose_name_plural = _("Rejection Reasons")
        indexes = [
            models.Index(fields=["value"]),
        ]

    def __str__(self) -> str:
        return self.value
```
