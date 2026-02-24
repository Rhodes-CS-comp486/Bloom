from django.db import migrations


def seed_habit_templates(apps, schema_editor):
    HabitTemplate = apps.get_model("us16_habit_tracking", "HabitTemplate")

    templates = [
        ("drink-water", "Drink water", "A small steady support for your body.", "Body", 10),
        ("nourishing-meal", "Nourishing meal", "Care, not perfection.", "Body", 20),
        ("gentle-movement", "Gentle movement", "Meet your body where it is today.", "Body", 30),
        ("stretch", "Stretch", "Soften tension in a kind way.", "Body", 40),
        ("step-outside", "Step outside", "A breath of fresh perspective.", "Body", 50),
        ("take-meds", "Take vitamins/meds", "Support your baseline.", "Body", 60),

        ("journal", "Journal", "Let your thoughts land somewhere gentle.", "Mind", 110),
        ("gratitude", "Gratitude note", "Name one small good thing.", "Mind", 120),
        ("breathing-pause", "Breathing pause", "A reset for your nervous system.", "Mind", 130),
        ("brain-dump", "Brain dump", "Empty the mental tabs.", "Mind", 140),

        ("tidy-5", "Tidy for 5 minutes", "A tiny reset counts.", "Home", 210),
        ("prep-tomorrow", "Prep for tomorrow", "Make future-you’s day lighter.", "Home", 220),

        ("text-someone", "Text someone you love", "Connection is care.", "Connection", 310),
        ("ask-for-help", "Ask for help", "You don’t have to do it alone.", "Connection", 320),

        ("earlier-bedtime", "Earlier bedtime", "Rest is a form of growth.", "Rest", 410),
        ("quiet-moment", "Quiet moment", "A pause before the next thing.", "Rest", 420),
        ("warm-shower", "Warm shower/bath", "Comfort is allowed.", "Rest", 430),
        ("phone-free-10", "10 minutes phone-free", "Give your mind room to breathe.", "Rest", 440),
    ]

    for slug, name, intention, category, sort_order in templates:
        HabitTemplate.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "intention": intention,
                "category": category,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


def unseed_habit_templates(apps, schema_editor):
    HabitTemplate = apps.get_model("us16_habit_tracking", "HabitTemplate")
    slugs = [
        "drink-water", "nourishing-meal", "gentle-movement", "stretch", "step-outside", "take-meds",
        "journal", "gratitude", "breathing-pause", "brain-dump",
        "tidy-5", "prep-tomorrow",
        "text-someone", "ask-for-help",
        "earlier-bedtime", "quiet-moment", "warm-shower", "phone-free-10",
    ]
    HabitTemplate.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("us16_habit_tracking", "0002_habittemplate_alter_habit_intention_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_habit_templates, unseed_habit_templates),
    ]