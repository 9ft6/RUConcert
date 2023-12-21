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
    id: str = Field(..., alias="id")
    region: Region = Field(..., alias="region")
    name: str = Field(..., alias="name")
    image: str = Field(..., alias="image")
    description: str = Field(..., alias="description")
    url: str = Field(..., alias="url")
    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    location: dict = Field(..., alias="location")
    offers: dict = Field(..., alias="offers")
