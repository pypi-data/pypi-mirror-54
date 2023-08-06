import numpy as np
import liquepy as lq

from tests.conftest import TEST_DATA_DIR


def calculate_fos():
    cpt = lq.field.load_mpa_cpt_file(TEST_DATA_DIR + "standard_1.csv")
    bi2014 = lq.trigger.run_bi2014(cpt, pga=0.25, m_w=7.5)
    factor_safety_values = bi2014.factor_of_safety

    expected_fos_at_40 = 2.0
    expected_fos_at_500 = 0.541205215
    assert factor_safety_values[40] == expected_fos_at_40
    assert np.isclose(factor_safety_values[500], expected_fos_at_500, rtol=0.0001)


def compare_fos():
    cpt = lq.field.load_mpa_cpt_file(TEST_DATA_DIR + "standard_1.csv")
    bi2014 = lq.trigger.BoulangerIdriss2014(cpt.depth, cpt.q_c, cpt.f_s, cpt.u_2, gwl=cpt.gwl, pga=0.25, m_w=7.5,
                               a_ratio=cpt.a_ratio)
    factor_safety_values = bi2014.factor_of_safety

    fos_expected = np.loadtxt(TEST_DATA_DIR + "standard_1_fos_lq0p1p6.csv")
    assert np.isclose(fos_expected, factor_safety_values).all()


if __name__ == '__main__':
    calculate_fos()
    compare_fos()
