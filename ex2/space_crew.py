from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum


class Rank(Enum):
    CADETS = "cadets"
    OFFICIER = "officier"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


def rank_check(members: list[CrewMember]) -> bool:
    for member in members:
        if member.rank.value == "commander" or member.rank.value == "captain":
            return True
    return False


def exp_check(members: list[CrewMember], duration_days: int) -> bool:
    count: int = 0
    for member in members:
        if member.years_experience >= 5:
            count += 1
    if (duration_days > 365) and ((len(members) / 2) > count):
        return False
    return True


def activity_check(members: list[CrewMember]) -> bool:
    for member in members:
        if not member.is_active:
            return False
    return True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not rank_check(self.crew):
            raise ValueError("Must have at least one Commander or Captain")
        if not exp_check(self.crew, self.duration_days):
            raise ValueError(
                "Long missions (> 365 days) need 50% "
                "experienced crew (5+ years)"
            )
        if not activity_check(self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    try:
        crew_list: list[CrewMember] = [
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=42,
                specialization="Mission Command",
                years_experience=19,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=36,
                specialization="Navigation",
                years_experience=15,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICIER,
                age=28,
                specialization="Engineering",
                years_experience=8,
            ),
        ]
        mission_valid: SpaceMission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2025, 6, 28, 11, 34, 5),
            duration_days=900,
            crew=crew_list,
            budget_millions=2500.0,
        )
        print(f"Mission: {mission_valid.mission_name}")
        print(f"ID: {mission_valid.mission_id}")
        print(f"Destination: {mission_valid.destination}")
        print(f"Duration: {mission_valid.duration_days} days")
        print(f"Duration: ${mission_valid.budget_millions}M")
        print(f"Crew size: {len(mission_valid.crew)}")
        print("Crew members:")
        for member in mission_valid.crew:
            print(
                f"- {member.name} ({member.rank.value}) - {member.specialization}"
            )
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)
    print("=========================================")
    print("Expected validation error:")
    try:
        crew_list_2: list[CrewMember] = [
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.CAPTAIN,
                age=34,
                specialization="Mission Command",
                years_experience=19,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.CADETS,
                age=36,
                specialization="Navigation",
                years_experience=15,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICIER,
                age=28,
                specialization="Engineering",
                years_experience=8,
            ),
        ]
        mission_invalid: SpaceMission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2025, 6, 28, 11, 34, 5),
            duration_days=900,
            crew=crew_list_2,
            budget_millions=2500.0,
        )
        print(f"Mission: {mission_invalid.mission_name}")
        print(f"ID: {mission_invalid.mission_id}")
        print(f"Destination: {mission_invalid.destination}")
        print(f"Duration: {mission_invalid.duration_days} days")
        print(f"Duration: ${mission_invalid.budget_millions}M")
        print(f"Crew size: {len(mission_invalid.crew)}")
        print("Crew members:")
        for member in mission_invalid.crew:
            print(
                f"- {member.name} ({member.rank.value})"
                f" - {member.specialization}"
            )
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
