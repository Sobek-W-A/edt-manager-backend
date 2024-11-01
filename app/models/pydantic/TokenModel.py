"""
This module provides model-checkes for the pydantic tokens.
"""

from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.services.Tokens import TokenAttributes, Token, TokenPair, AvailableTokenModels


# -------- pydantic models -------- #
class PydanticTokenExporter(ABC, BaseModel):
    """
    This class provides an abstract method that forces us to define an abstract method that exports
    the current pydantic model to a Tortoise one.
    """
    @abstractmethod
    def export_pydantic_to_model(self,
                                 attributes: TokenAttributes) -> AvailableTokenModels:
        """
        This method exports the current pydantic model
        """


class PydanticToken(PydanticTokenExporter):
    """
    This class is a pydantic model for a signle Token.
    """
    value:      str
    token_type: str = "bearer"

    def export_pydantic_to_model(self, attributes: TokenAttributes) -> Token:
        return Token(attributes=attributes, value=self.value)

class PydanticTokenPair(PydanticTokenExporter):
    """
    This class is a pydantic model for a pair of Tokens.
    """
    access_token:   str
    refresh_token:  str
    token_type:     str = "bearer"

    def export_pydantic_to_model(self, attributes: TokenAttributes | None = None) -> TokenPair:
        return TokenPair(access_token=self.access_token, refresh_token=self.refresh_token)
