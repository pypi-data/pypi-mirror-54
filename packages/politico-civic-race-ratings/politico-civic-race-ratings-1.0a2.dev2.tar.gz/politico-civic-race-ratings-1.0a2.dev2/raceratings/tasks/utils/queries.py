# Imports from Django.
from django.db.models import Prefetch


# Imports from other dependencies.
from election.models import CandidateElection
from election.models import Election
from election.models import ElectionType
from election.models import Race


# Imports from race_ratings.
from raceratings.models import RaceRating


def filter_races(required_args, extra_constraints={}):
    election_year, include_special_elections = required_args

    race_query = {"cycle__slug": election_year, **extra_constraints}

    if not include_special_elections:
        race_query["special"] = False

    races = (
        Race.objects.prefetch_related(
            Prefetch(
                "ratings",
                queryset=RaceRating.objects.select_related(
                    "race", "category"
                ).order_by("created", "pk"),
            ),
            Prefetch(
                "elections",
                queryset=Election.objects.prefetch_related(
                    Prefetch(
                        "candidate_elections",
                        queryset=CandidateElection.objects.select_related(
                            "election",
                            "candidate",
                            "candidate__party",
                            "candidate__person",
                        ),
                    )
                )
                .select_related("race", "election_type")
                .filter(election_type__slug=ElectionType.GENERAL)
                .order_by("race_id", "election_type__slug"),
            ),
        )
        .select_related(
            "cycle",
            "division",
            "division__level",
            "division__parent",
            "office",
            "office__body",
            "office__body__organization",
            "office__division",
            "office__division__level",
            "office__division__parent",
        )
        .filter(**race_query)
    )

    return races
