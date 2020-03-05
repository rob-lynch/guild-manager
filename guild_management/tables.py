import django_tables2 as tables
from .models import Character

class CharacterTable(tables.Table):
    class Meta:
        model = Character
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "guild_join_date",
            "raid_eligibility_date",
            "rank",
            "playable_class",
            "number_of_eligible_raids",
            "number_or_raids_attended",
            "attendence_percentage",
        )