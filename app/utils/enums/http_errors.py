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
    PROFILE_NOT_FOUND        = "User was not found."
    PROFILE_NOT_ENABLED      = "This user is not enabled."
    ACCOUNT_NOT_FOUND        = "Account was not found."
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
    # Folder Errors
    FOLDER_AND_UE_NOT_ENABLED= "You can't have a folder with a folder and an UE"
    # UE Errors
    UE_NOT_FOUND             = "UE was not found"
    UE_ALREADY_EXIST         = "UE already exists"
    #Course Errors
    COURSE_NOT_FOUND         = "Course was not found"
    COURSE_ALREADY_EXIST     = "Course already exists"
    # Role Errors
    ROLE_NOT_FOUND           = "Role was not found"
    ROLE_ALREADY_EXIST       = "Role already exists"
    # Permission Errors
    PERMISSION_NOT_FOUND     = "Permission was not found"
