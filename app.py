def generate_rule_based_copy(
    product_name: str,
    product_desc: str,
    audience: str,
    tone: str,
    benefits_list: List[str],
    cta: str,
    awareness: str,
    master_style: str,
    niche: str,
) -> Tuple[List[str], str]:
    """
    Rule-based copy generator with human-style flow and master personality.
    """

    # --- Defaults ---
    if not audience.strip():
        niche_aud, _ = choose_niche_defaults(niche)
        audience = niche_aud
    if not benefits_list:
        _, niche_benefits = choose_niche_defaults(niche)
        benefits_list = niche_benefits

    base_benefit = benefits_list[0]
    audience_short = normalize_audience(audience)

    style_flavor = MASTER_FLAVORS.get(master_style, "direct-response style tuned for conversions")
    awareness_angle = AWARENESS_ANGLE.get(awareness, "meet them where they are and lead them step-by-step to a decision")

    # --- Headline Ideas ---
    headlines = [
        f"Finally: {product_name} That Helps You {base_benefit.capitalize()} Without The Struggle",
        f"How {audience_short.capitalize()} Can {base_benefit.capitalize()} with {product_name}",
        f"Breakthrough {niche} Secret: {product_name} Helps You {base_benefit.capitalize()} Starting Today",
        f"Do You Make These Mistakes When Trying to {base_benefit.capitalize()}?",
        f"The Hidden Shortcut to {base_benefit.capitalize()} No One Told You About",
    ]

    if len(benefits_list) > 1:
        headlines.append(f"Turn '{benefits_list[1].capitalize()}' Into Your Edge With {product_name}")

    # --- CTA Tone Map ---
    cta_map = {
        "Natural / Alternative Healing": "Take your first step toward true natural health.",
        "Relationships": "Because love doesn’t fix itself — it starts with action.",
        "Money & Business": "Your future profits are waiting. Act while others hesitate.",
        "General Interest & Survival": "Because being prepared means never feeling helpless again.",
    }
    cta_phrase = cta_map.get(niche, "Take action now before the moment passes.")

    # --- Sales Copy ---
    bullets = "\n".join([f"- {b}" for b in benefits_list])
    emotion_intro = {
        "Gary Halbert": "Let’s cut through the noise for a second.",
        "David Ogilvy": "Here’s a fact few advertisers ever admit.",
        "Dan Kennedy": "I’ll be blunt — most people get this part completely wrong.",
        "Joe Sugarman": "Let me tell you a quick story that changed everything.",
        "Eugene Schwartz": "The key is not desire — it’s understanding where it already exists.",
    }.get(master_style, "Here’s the real story behind this.")

    sales_copy = textwrap.dedent(
        f"""
        [{master_style}-inspired angle – {style_flavor}]

        ATTENTION

        {emotion_intro}

        If you're {audience_short}, you’ve probably tried to {base_benefit.lower()} before —
        but no matter what you’ve done, something always felt off. There’s a good chance
        the problem isn’t you... it’s the message you’ve been fed.

        INTEREST

        **{product_name}** is built to fix that.

        {product_desc.strip()}

        It works because it speaks directly to what your market already cares about most.
        You don’t have to “educate” or convince — you just meet them at their strongest emotion,
        then guide them naturally toward saying yes.

        DESIRE

        Imagine this working for you:

        {bullets}

        Instead of chasing shiny tactics, you’ll finally have a system that makes people *want* what you offer.

        ACTION

        If you're serious about {base_benefit.lower()} and ready to use copy that finally matches
        the real value you deliver — this is your move.

        👉 {cta.strip().rstrip('.')}

        {cta_phrase}
        """
    ).strip()

    return headlines, sales_copy
