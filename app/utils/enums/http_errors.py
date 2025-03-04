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
    PROFILE_NOT_FOUND        = "Profile was not found."
    PROFILE_NOT_ENABLED      = "This profile is not enabled."
    ACCOUNT_NOT_FOUND        = "Account was not found."
    ACCOUNT_ROLE_NOT_FOUND   = "This account has no role for this academic_year."
    ACCOUNT_ALREADY_LINKED   = "This account is already linked to a profile for the academic year provided."
    PASSWORD_OR_PASSCONFIRM_NOT_SPECIFIED = "Both 'password' and 'password_confirm' must be specified together or not at all."
    COLUMN_DOES_NOT_EXIST     = "This column name does not exists."
    # Credentials Errors
    INVALID_CREDENTIALS       = "Invalid credentials."
    INCORRECT_LOGIN_PASSWORD  = "Incorrect login or password."
    # Status Errors
    STATUS_NOT_FOUND          = "Status was not found."
    # Token Errors
    TOKEN_REVOKED             = "The token has been revoked."
    TOKEN_INVALID             = "The token is invalid."
    TOKEN_EXPIRED             = "The token has expired."
    # Permission Errors
    FORBIDDEN_ACTION          = "You don't have the permission to perform this operation."
    # Folder Errors
    NODE_NOT_FOUND            = "Node was not found"
    PARENT_NODE_NOT_FOUND     = "Parent node was not found"
    ROOT_NODE_NOT_FOUND       = "Root node was not found"
    NODE_CANT_DELETE_CHILDREN = "You can't delete a node with children. Delete the children first."
    FOLDER_AND_UE_NOT_ENABLED = "You can't have a folder that contains a folder and an UE"
    # UE Errors
    UE_NOT_FOUND              = "UE was not found"
    UE_ALREADY_EXIST          = "UE already exists"
    # Course Errors
    COURSE_NOT_FOUND          = "Course was not found"
    COURSE_ALREADY_EXIST      = "Course already exists"
    COURSE_TYPE_NOT_FOUND     = "Course type was not found"
    DURATION_VALUE_INCORRECT  = "The duration can't be negative"
    GROUP_VALUE_INCORRECT     = "The Group count value is invalid"
    # Role Errors
    ROLE_NOT_FOUND            = "Role was not found"
    ROLE_ALREADY_EXIST        = "Role already exists"
    CANNOT_SET_YOUR_OWN_ROLE  = "You can't set your own role"
    CANNOT_DELETE_ADMIN       = "You can't delete the admin role"
    CANNOT_UPDATE_ADMIN       = "You can't update the admin role"
    # Permission Errors
    PERMISSION_NOT_FOUND      = "Permission was not found"
    # Affectation Errors
    AFFECTATION_ACADEMIC_YEAR_MISMATCH   = "The two academic year provided are different. They cannot be linked by the same affectation."
    AFFECTATION_NOT_FOUND                = "Affectation was not found."
    AFFECTATION_GROUP_INVALID            = "Invalid group number. Must be positive and less than the group count of the course."
    # Academic_year Errors
    ACADEMIC_YEAR_NOT_FOUND = "Academic year was not found"
