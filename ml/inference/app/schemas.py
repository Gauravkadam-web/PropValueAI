"""
Pydantic Request and Response Schemas for the PropValueAI ML Inference Service.

Enforces strict input validation, rejects target leakage ('price'), validates
numeric finiteness, and provides clear structured responses adhering to docs/api-contracts.md.
"""

import math
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator


from ml.common.transformers import parse_sqft_value


class PropertyPredictRequest(BaseModel):
    """
    Input schema for single property price prediction.
    Features map directly to the fitted scikit-learn PropertyFeatureTransformer.
    """

    total_sqft: Union[float, int, str] = Field(
        ...,
        description="Total property area. Can be numeric (e.g. 1200), range string ('2100 - 2850'), or unit string ('1000Sq. Meter', '1Acres').",
        examples=[1056.0, "2100 - 2850", "1000Sq. Meter"],
    )
    size: Optional[Union[str, int, float]] = Field(
        default=None,
        description="Bedroom count specification (e.g. '2 BHK', '3 Bedroom', '1 RK', 2).",
        examples=["2 BHK", 3],
    )
    bhk: Optional[Union[int, float]] = Field(
        default=None,
        description="Alternative direct numeric bedroom count. If both 'size' and 'bhk' are omitted, median will be imputed.",
        examples=[2],
    )
    bath: Optional[float] = Field(
        default=None,
        description="Number of bathrooms. If omitted, median will be imputed.",
        examples=[2.0],
    )
    balcony: Optional[float] = Field(
        default=None,
        description="Number of balconies. If omitted, median will be imputed.",
        examples=[1.0],
    )
    area_type: Optional[str] = Field(
        default=None,
        description="Property area type category (e.g. 'Super built-up  Area', 'Plot  Area', 'Built-up  Area', 'Carpet  Area').",
        examples=["Super built-up  Area"],
    )

    @model_validator(mode="before")
    @classmethod
    def reject_target_and_validate_structure(cls, data: Any) -> Any:
        """Prevent target leakage and validate that input is a dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Property request payload must be a JSON object.")
        if "price" in data:
            raise ValueError("Target variable 'price' cannot be supplied as an input prediction feature.")
        return data

    @field_validator("total_sqft")
    @classmethod
    def validate_total_sqft(cls, v: Union[float, int, str]) -> Union[float, int, str]:
        """Validate that total_sqft is positive, finite, and non-empty."""
        if isinstance(v, (int, float)):
            if math.isnan(v) or math.isinf(v):
                raise ValueError("total_sqft cannot be NaN or infinite.")
            if v <= 0:
                raise ValueError("total_sqft must be strictly greater than 0.")
            return float(v)
        if isinstance(v, str):
            clean = v.strip()
            if not clean:
                raise ValueError("total_sqft string cannot be empty or whitespace only.")
            parsed = parse_sqft_value(clean)
            if math.isnan(parsed) or parsed <= 0:
                raise ValueError(f"total_sqft string '{clean}' cannot be parsed to a positive area.")
            return clean
        raise ValueError("total_sqft must be a positive number or valid area string.")

    @field_validator("bath")
    @classmethod
    def validate_bath(cls, v: Optional[float]) -> Optional[float]:
        """Validate bathroom count is non-negative and finite."""
        if v is not None:
            if math.isnan(v) or math.isinf(v):
                raise ValueError("bath cannot be NaN or infinite.")
            if v < 0:
                raise ValueError("bath cannot be negative.")
            if v > 20:
                raise ValueError("bath exceeds realistic residential upper bound of 20.")
            return float(v)
        return v

    @field_validator("balcony")
    @classmethod
    def validate_balcony(cls, v: Optional[float]) -> Optional[float]:
        """Validate balcony count is non-negative and finite."""
        if v is not None:
            if math.isnan(v) or math.isinf(v):
                raise ValueError("balcony cannot be NaN or infinite.")
            if v < 0:
                raise ValueError("balcony cannot be negative.")
            if v > 10:
                raise ValueError("balcony exceeds realistic residential upper bound of 10.")
            return float(v)
        return v

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: Optional[Union[str, int, float]]) -> Optional[Union[str, int, float]]:
        """Validate bedroom size string or number."""
        if v is not None:
            if isinstance(v, (int, float)):
                if math.isnan(v) or math.isinf(v):
                    raise ValueError("size numeric value cannot be NaN or infinite.")
                if v <= 0:
                    raise ValueError("size bedroom count must be strictly greater than 0.")
                return v
            if isinstance(v, str):
                clean = v.strip()
                if not clean:
                    raise ValueError("size string cannot be empty.")
                return clean
        return v

    @field_validator("bhk")
    @classmethod
    def validate_bhk(cls, v: Optional[Union[int, float]]) -> Optional[Union[int, float]]:
        """Validate direct bhk input."""
        if v is not None:
            if math.isnan(v) or math.isinf(v):
                raise ValueError("bhk cannot be NaN or infinite.")
            if v <= 0:
                raise ValueError("bhk bedroom count must be strictly greater than 0.")
            return v
        return v

    def to_feature_dict(self) -> Dict[str, Any]:
        """Converts validated schema into dictionary format expected by PropertyFeatureTransformer."""
        data: Dict[str, Any] = {
            "total_sqft": self.total_sqft,
            "bath": self.bath,
            "balcony": self.balcony,
            "area_type": self.area_type,
        }
        if self.size is not None:
            data["size"] = self.size
        elif self.bhk is not None:
            data["size"] = f"{self.bhk} BHK"
        else:
            data["size"] = None
        return data


class PropertyBatchPredictRequest(BaseModel):
    """Batch input schema supporting up to 100 properties per request."""

    properties: List[PropertyPredictRequest] = Field(
        ...,
        min_length=1,
        description="List of property requests for batch inference (1 to 100 items).",
    )


class PropertyPredictResponse(BaseModel):
    """Standardized single prediction response."""

    prediction_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this prediction query.",
    )
    predicted_price: float = Field(
        ...,
        description="Estimated property price.",
    )
    target_unit: str = Field(
        default="Lakhs INR",
        description="Unit of measurement for the predicted price (1 Lakh = ₹100,000).",
    )
    model_name: str = Field(
        ...,
        description="Name of the fitted machine learning model.",
    )
    model_version: str = Field(
        ...,
        description="Semantic version of the model artifact.",
    )
    disclaimer: str = Field(
        ...,
        description="Mandatory educational limitation notice.",
    )


class PropertyBatchPredictResponse(BaseModel):
    """Standardized batch prediction response."""

    predictions: List[PropertyPredictResponse] = Field(
        ...,
        description="Ordered list of prediction responses matching input order.",
    )
    count: int = Field(
        ...,
        description="Total number of evaluated properties.",
    )
    model_name: str = Field(
        ...,
        description="Model name used for batch inference.",
    )
    model_version: str = Field(
        ...,
        description="Model version used for batch inference.",
    )
    disclaimer: str = Field(
        ...,
        description="Mandatory educational limitation notice.",
    )


class HealthLiveResponse(BaseModel):
    """Liveness probe response."""

    status: str = Field("alive", description="Process liveness indicator.")
    service: str = Field(..., description="Service identifier.")


class HealthReadyResponse(BaseModel):
    """Readiness probe response indicating model loading status."""

    status: str = Field(..., description="Readiness state ('ready' or 'not_ready').")
    model_loaded: bool = Field(..., description="True if fitted pipeline is active.")
    model_name: Optional[str] = Field(None, description="Name of loaded model.")
    model_version: Optional[str] = Field(None, description="Version of loaded model.")
    target_unit: Optional[str] = Field(None, description="Target currency unit.")
    details: Optional[str] = Field(None, description="Informational message or error details.")


class ModelInfoResponse(BaseModel):
    """Safe model metadata and architectural specifications."""

    model_name: str
    model_version: str
    target_variable: str
    target_unit: str
    feature_schema: Dict[str, Any]
    evaluation_metrics: Dict[str, Any]
    limitations: str
