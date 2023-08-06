from nnql import Executor, use
from nnql.tests.just_add_tfe import just_add_tfe
from nnql.tools import op_count_naive
from nnql.tools.op_count import OpCount


def test_op_count_naive():
    with Executor():
        op_count = op_count_naive.OpCount()
        use(op_count)
        just_add_tfe()
        assert op_count.count == 6


def test_op_count():
    with Executor():
        op_count = OpCount()
        use(op_count)
        just_add_tfe()
        assert op_count.count == 6


def test_op_count_both():
    with Executor():
        op_count = OpCount()
        op_count_naive_ = op_count_naive.OpCount()
        use(op_count)
        use(op_count_naive_)
        just_add_tfe()
        assert op_count.count == 6
        assert op_count_naive_.count == 6
