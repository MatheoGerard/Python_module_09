from pydantic import BaseModel, ValidationError, Field, model_validator
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class ContactRapport(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_rules(self) -> "ContactRapport":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact id must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact must be verified")
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    rapport: ContactRapport | None = None
    try:
        rapport = ContactRapport(
            contact_id="AC_2024_001",
            timestamp=datetime(2025, 6, 28, 11, 34, 5),
            contact_type=ContactType.RADIO,
            location="rea 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )
        print(f"ID: {rapport.contact_id}")
        print(f"Type: {rapport.contact_type.value}")
        print(f"Location: {rapport.location}")
        print(f"Signal: {rapport.signal_strength}/10")
        print(f"Duration: {rapport.duration_minutes} minutes")
        print(f"Witnesses: {rapport.witness_count}")
        print(f"Message: {rapport.message_received}\n")
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)
    print("======================================")
    print("Expected validation error:")
    try:
        rapport = ContactRapport(
            contact_id="AC_2024_001",
            timestamp=datetime(2025, 6, 28, 11, 34, 5),
            contact_type=ContactType.TELEPATHIC,
            location="rea 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli",
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
