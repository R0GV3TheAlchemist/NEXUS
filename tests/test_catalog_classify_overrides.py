from nexus.catalog.classify import classify_text


def test_life_force_conversion_requires_human_review():
    result = classify_text("Life-Force Conversion", "Converts life energy into another form of matter or energy.")

    assert result.primary == "needs_human"
    assert result.tags == ("needs_human",)
    assert result.reasons == ("manual_contextual_conversion",)


def test_metamorphic_conversion_is_map_ok():
    result = classify_text("Metamorphic Conversion", "Uses elements from one's own being to manipulate subjects.")

    assert result.primary == "map_ok"
    assert result.tags == ("map_ok",)
    assert result.reasons == ("manual_self_sourced_conversion",)
