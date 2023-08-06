from nnql import Executor, use
from nnql.tests.just_add_tfe import just_add_tfe
from nnql.tools.dumb import Dumb


def test_dumb():
    with Executor():
        dumb = Dumb()
        use(dumb)
        just_add_tfe()
