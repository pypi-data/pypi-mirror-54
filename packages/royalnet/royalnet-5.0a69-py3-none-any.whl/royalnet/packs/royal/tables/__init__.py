# Imports go here!
from royalnet.packs.common.tables import User
from royalnet.packs.common.tables import Telegram
from royalnet.packs.common.tables import Discord

from .diario import Diario
from .aliases import Alias
from .activekvgroups import ActiveKvGroup
from .keyvalues import Keyvalue
from .keygroups import Keygroup
from .wikipages import WikiPage
from .wikirevisions import WikiRevision
from .bios import Bio
from .reminders import Reminder
from .triviascores import TriviaScore
from .mmdecisions import MMDecision
from .mmevents import MMEvent
from .mmresponse import MMResponse

# Enter the tables of your Pack here!
available_tables = [
    User,
    Telegram,
    Discord,
    Diario,
    Alias,
    ActiveKvGroup,
    Keyvalue,
    Keygroup,
    WikiPage,
    WikiRevision,
    Bio,
    Reminder,
    TriviaScore,
    MMDecision,
    MMEvent,
    MMResponse,
]

# Don't change this, it should automatically generate __all__
__all__ = [table.__class__.__qualname__ for table in available_tables]
