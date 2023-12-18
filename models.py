from pydantic import BaseModel, ConfigDict, Field, validator


class ConfiguredModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class Region(ConfiguredModel):
    name: str = Field(..., alias="region_name")
    id: str = Field(..., alias="data-js-dd-item")

    @validator("id")
    def validate_id(cls, value: str):
        return value.replace("changesd", "").replace("/", "")


class Concert(ConfiguredModel):
    region: Region
