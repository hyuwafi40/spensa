from .index import (
    IndexRedirectView,
    DeveloperDashboardView,
    AdministratorDashboardView,
    TeacherDashboardView,
    StudentDashboardView,
)
from .account import (
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    AccountResetPasswordView,
)
from .year import (
    YearListView,
    YearCreateView,
    YearUpdateView,
    YearDeleteView,
)
from .term import (
    TermListView,
    TermCreateView,
    TermUpdateView,
    TermDeleteView,
)
from .subject import (
    SubjectListView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView,
)
from .classroom import (
    ClassroomListView,
    ClassroomCreateView,
    ClassroomUpdateView,
    ClassroomDeleteView,
)
from .activeyear import (
    ActiveYearListView,
    ActiveYearCreateView,
    ActiveYearUpdateView,
    ActiveYearDeleteView,
    ActiveYearToggleActiveView,
)
from .activesubject import (
    ActiveSubjectListView,
    ActiveSubjectCreateView,
    ActiveSubjectUpdateView,
    ActiveSubjectDeleteView,
)
from .activeclassroom import (
    ActiveClassroomListView,
    ActiveClassroomCreateView,
    ActiveClassroomUpdateView,
    ActiveClassroomDeleteView,
    ActiveStudentListView,
    ActiveStudentCreateView,
    ActiveStudentUpdateView,
    ActiveStudentDeleteView,
)

__all__ = [
    "IndexRedirectView",
    "DeveloperDashboardView",
    "AdministratorDashboardView",
    "TeacherDashboardView",
    "StudentDashboardView",
    "AccountListView",
    "AccountCreateView",
    "AccountUpdateView",
    "AccountDeleteView",
    "AccountResetPasswordView",
    "YearListView",
    "YearCreateView",
    "YearUpdateView",
    "YearDeleteView",
    "TermListView",
    "TermCreateView",
    "TermUpdateView",
    "TermDeleteView",
    "SubjectListView",
    "SubjectCreateView",
    "SubjectUpdateView",
    "SubjectDeleteView",
    "ClassroomListView",
    "ClassroomCreateView",
    "ClassroomUpdateView",
    "ClassroomDeleteView",
    "ActiveYearListView",
    "ActiveYearCreateView",
    "ActiveYearUpdateView",
    "ActiveYearDeleteView",
    "ActiveYearToggleActiveView",
    "ActiveSubjectListView",
    "ActiveSubjectCreateView",
    "ActiveSubjectUpdateView",
    "ActiveSubjectDeleteView",
    "ActiveClassroomListView",
    "ActiveClassroomCreateView",
    "ActiveClassroomUpdateView",
    "ActiveClassroomDeleteView",
    "ActiveStudentListView",
    "ActiveStudentCreateView",
    "ActiveStudentUpdateView",
    "ActiveStudentDeleteView",
]
