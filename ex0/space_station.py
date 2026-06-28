from pydantic import BaseModel, Field, ValidationError, field_validator
from datetime import datetime


class Space_station(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)

    def get_operationnal(self) -> str:
        if self.is_operational:
            return "Operational"
        return "Non-operational"

    @field_validator("last_maintenance")
    @classmethod
    def date_in_past(cls, value: datetime) -> datetime:
        if value > datetime.today():
            raise ValueError("Last maintenance cannot be in the future")
        return value


def main() -> None:
    space_station: Space_station = Space_station(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2025, 6, 28, 11, 34, 5),
    )
    print("Valid station created:")
    print(f"ID: {space_station.station_id}")
    print(f"Name: {space_station.name}")
    print(f"Crew: {space_station.crew_size} people")
    print(f"Power: {space_station.power_level}%")
    print(f"Oxygen: {space_station.oxygen_level}%")
    print(f"Status: {space_station.get_operationnal()}\n")
    print("========================================")
    print("Expected validation error:")
    try:
        space_station_invalid: Space_station = Space_station(
            station_id="ISS001",
            name="International Space Station",
            crew_size=56,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2025, 6, 28, 11, 34, 5),
        )
        print("Valid station created:")
        print(f"ID: {space_station_invalid.station_id}")
        print(f"Name: {space_station_invalid.name}")
        print(f"Crew: {space_station_invalid.crew_size} people")
        print(f"Power: {space_station_invalid.power_level}%")
        print(f"Oxygen: {space_station_invalid.oxygen_level}%")
        print(f"Status: {space_station_invalid.get_operationnal()}\n")
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    print("Space Station Data Validation")
    print("========================================")
    main()
