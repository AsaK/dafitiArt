# coding=utf-
"""
    Arquivo para conter as contantes de escolhas do sistema
"""
STATUS_CHOICES = (
    (1, "Active"),
    (2, "In Progress"),
    (3, "In Review"),
    (4, "Returned"),
    (5, "Completed"),
    (6, "Inactive")
)

EVENT_DESCRIPTION = (
    ("ChangeStatus", "Changed the status of this request"),
    ("InsertComment", "Inserted a new comment"),
    ("ChangeResponsible", "Changed the responsible person in the requisition"),
    ("ChangeProgress", "Changed the request progression"),
)
