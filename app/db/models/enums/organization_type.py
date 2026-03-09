import enum

class OrganizationType(str, enum.Enum):
    # Local structure
    REGION = "region"
    UNIT = "unit"
    SECTION = "section"
    PATROLS = "patrols"
    SIXES = "sixes"

    # Federal structure
    ASSOCIATION = "association"
    FEDERAL_INSTANCE = "federal_instance"
    COMMISSION = "commission"
    WORKING_GROUP = "working_group"
    ER = "ER"
    EU = "EU"
    EFT = "EFT"
    FCT = "FCT"
    COM = "COM"

    # External groups
    PARTNER = "partner"
    SUPPLIER = "supplier"
    AUTHORITY = "authority"
    INSTITUTION = "institution"