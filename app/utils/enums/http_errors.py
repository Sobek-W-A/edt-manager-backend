"""
This file provides Enums to use as standards to send error details to the Frontend app.
"""
import enum

class CommonErrorMessages(enum.StrEnum):
    """
    Enumeration to provide the commonly used error messages inside the API.
    """
    # User errors
    PASSWORDS_DONT_MATCH     = "The passwords provided don't match."
    PASSWORD_NOT_SECURE      = "The password provided is not secure enough."
    LOGIN_ALREADY_USED       = "This login has already been used."
    MAIL_ALREADY_USED        = "This mail address has already been used."
    MAIL_INVALID             = "Invalid mail address."
    NAME_INVALID             = "Invalid name (name should only contain alphabetic characters and spaces)"
    LOGIN_INVALID            = "Invalid login (login should only contain alphabetic characters, digits and spaces)"
    PROFILE_NOT_FOUND           = "User was not found."
    PROFILE_NOT_ENABLED         = "This user is not enabled."
    PASSWORD_OR_PASSCONFIRM_NOT_SPECIFIED = "Both 'password' and 'password_confirm' must be specified together or not at all."
    # Credentials Errors
    INVALID_CREDENTIALS      = "Invalid credentials."
    INCORRECT_LOGIN_PASSWORD = "Incorrect login or password."
    # Token Errors
    TOKEN_REVOKED            = "The token has been revoked."
    TOKEN_INVALID            = "The token is invalid."
    TOKEN_EXPIRED            = "The token has expired."
    # Permission Errors
    FORBIDDEN_ACTION         = "You don't have the permission to perform this operation."
